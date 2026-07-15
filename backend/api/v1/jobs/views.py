"""
Job Views for API v1
Provides job listing, detail, and filter options endpoints
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from peeldb.models import JobPost, City, Skill, Industry, Qualification, SavedJobs, AppliedJobs
from .serializers import JobListSerializer, JobDetailSerializer
from .filters import JobFilter


class JobPagination(PageNumberPagination):
    """Custom pagination for job listings"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for job listings and details.

    Provides:
    - list: Paginated job listings with advanced filtering
    - retrieve: Detailed job information by ID or slug

    Filters available:
    - search: Search in title, company, description
    - location: Filter by city slugs (multiple)
    - skills: Filter by skill slugs (multiple)
    - industry: Filter by industry slugs (multiple)
    - education: Filter by qualification slugs (multiple)
    - job_type: Filter by job type (full-time, internship, etc.)
    - min_salary, max_salary: Salary range in RUB/month
    - min_experience, max_experience: Experience range in years
    - fresher: Fresher jobs only (boolean)
    - is_remote: Remote jobs only (boolean)
    - posted_after, posted_before: Date range filters

    Ordering:
    - published_on (default: newest first)
    - title
    - min_salary, max_salary
    """
    permission_classes = [AllowAny]
    pagination_class = JobPagination
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'company_name', 'description', 'job_role']
    ordering_fields = ['published_on', 'title', 'min_salary', 'max_salary', 'created_on']
    ordering = ['-published_on']
    lookup_field = 'id'

    def get_queryset(self):
        """
        Optimized queryset: annotate applicant counts, prefetch relations.
        Use distinct() only when M2M filters would otherwise duplicate rows.
        """
        qs = (
            JobPost.objects.filter(status="Live")
            .select_related("company", "country", "major_skill")
            .prefetch_related("location", "skills", "industry", "edu_qualification")
            .annotate(applicants_count_anno=Count("appliedjobs", distinct=True))
        )

        # M2M filters can produce duplicate JobPost rows — distinct only then
        params = self.request.query_params if hasattr(self, "request") else {}
        needs_distinct = any(
            params.get(key)
            for key in ("location", "skills", "industry", "education")
        )
        if needs_distinct:
            qs = qs.distinct()
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.setdefault("saved_job_ids", set())
        context.setdefault("applied_job_ids", set())
        return context

    @extend_schema(summary="List jobs", tags=["Jobs"])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        jobs = page if page is not None else list(queryset)
        job_ids = [j.id for j in jobs]

        context = self.get_serializer_context()
        user = request.user
        if user and user.is_authenticated and job_ids:
            context["saved_job_ids"] = set(
                SavedJobs.objects.filter(user=user, job_post_id__in=job_ids).values_list(
                    "job_post_id", flat=True
                )
            )
            context["applied_job_ids"] = set(
                AppliedJobs.objects.filter(user=user, job_post_id__in=job_ids).values_list(
                    "job_post_id", flat=True
                )
            )
        else:
            context["saved_job_ids"] = set()
            context["applied_job_ids"] = set()

        serializer = self.get_serializer(jobs, many=True, context=context)
        response = (
            self.get_paginated_response(serializer.data)
            if page is not None
            else Response(serializer.data)
        )
        # Short public cache — reduces SSR hammering from Vercel
        response["Cache-Control"] = "public, max-age=30, stale-while-revalidate=60"
        return response

    def get_serializer_class(self):
        """Use detailed serializer for retrieve, lightweight for list"""
        if self.action == 'retrieve':
            return JobDetailSerializer
        return JobListSerializer

    @extend_schema(
        summary="Get job details",
        description="Retrieve detailed information about a specific job by ID or slug",
        tags=['Jobs'],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve job by ID or slug.
        Accepts numeric id, plain slug, or legacy /slug/ form.
        """
        lookup_value = (kwargs.get('id') or '').strip()

        qs = self.get_queryset()
        instance = None

        try:
            if lookup_value.isdigit():
                instance = qs.get(id=int(lookup_value))
            else:
                plain = lookup_value.strip('/')
                candidates = [
                    lookup_value,
                    plain,
                    f'/{plain}/',
                    f'{plain}/',
                    f'/{plain}',
                ]
                # Preserve order, drop empties/dupes
                seen = set()
                for candidate in candidates:
                    if not candidate or candidate in seen:
                        continue
                    seen.add(candidate)
                    instance = qs.filter(slug=candidate).first()
                    if instance:
                        break
                if instance is None:
                    raise JobPost.DoesNotExist()
        except JobPost.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary="Manage saved jobs",
        description="Save, unsave, or get saved jobs (requires authentication)",
        tags=['Jobs'],
    )
    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticated], url_path='saved')
    def saved_jobs(self, request):
        """
        GET: Get all saved jobs for the authenticated user
        POST: Save a job for the authenticated user
        """
        if request.method == 'GET':
            # Get all saved jobs
            saved_jobs = SavedJobs.objects.filter(user=request.user).select_related('job_post')
            jobs = [saved.job_post for saved in saved_jobs if saved.job_post.status == 'Live']
            serializer = JobListSerializer(jobs, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            # Save a job
            job_id = request.data.get('job_id')

            if not job_id:
                return Response(
                    {'error': 'job_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                job = JobPost.objects.get(id=job_id, status='Live')
            except JobPost.DoesNotExist:
                return Response(
                    {'error': 'Job not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if already saved
            if SavedJobs.objects.filter(job_post=job, user=request.user).exists():
                return Response(
                    {'error': 'Job already saved'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save the job
            SavedJobs.objects.create(job_post=job, user=request.user)

            return Response(
                {'message': 'Job saved successfully', 'job_id': job_id},
                status=status.HTTP_201_CREATED
            )

    @extend_schema(
        summary="Unsave job",
        description="Remove a saved/bookmarked job (requires authentication)",
        responses={
            200: {'description': 'Job unsaved successfully'},
            404: {'description': 'Saved job not found'}
        },
        tags=['Jobs'],
    )
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated], url_path='saved')
    def unsave_job(self, request, id=None):
        """Remove a saved job for the authenticated user"""
        try:
            job = JobPost.objects.get(id=id)
        except JobPost.DoesNotExist:
            return Response(
                {'error': 'Job not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            saved_job = SavedJobs.objects.get(job_post=job, user=request.user)
            saved_job.delete()
            return Response(
                {'message': 'Job unsaved successfully'},
                status=status.HTTP_200_OK
            )
        except SavedJobs.DoesNotExist:
            return Response(
                {'error': 'Saved job not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="Apply for job",
        description="Submit an application for a job (requires authentication)",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'remarks': {
                        'type': 'string',
                        'description': 'Optional remarks or cover letter',
                        'nullable': True
                    }
                }
            }
        },
        responses={
            201: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'application_id': {'type': 'integer'}
                }
            },
            400: {'description': 'Already applied or invalid request'},
            404: {'description': 'Job not found'}
        },
        tags=['Jobs'],
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='apply')
    def apply_for_job(self, request, id=None):
        """Apply for a job"""
        try:
            job = JobPost.objects.get(id=id, status='Live')
        except JobPost.DoesNotExist:
            return Response(
                {'error': 'Job not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if job can still accept applications (30-day rule)
        if not job.can_accept_applications():
            return Response(
                {'error': 'This job is no longer accepting applications'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already applied
        if AppliedJobs.objects.filter(job_post=job, user=request.user).exists():
            return Response(
                {'error': 'You have already applied for this job'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get request metadata
        ip_address = request.META.get('REMOTE_ADDR', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        remarks = request.data.get('remarks', '')

        # Create application
        application = AppliedJobs.objects.create(
            job_post=job,
            user=request.user,
            status='Applied',
            remarks=remarks,
            ip_address=ip_address,
            user_agent=user_agent
        )

        return Response(
            {
                'message': 'Application submitted successfully',
                'application_id': application.id
            },
            status=status.HTTP_201_CREATED
        )


class JobFilterOptionsView(APIView):
    """
    API endpoint to get available filter options with job counts.

    Returns all available locations, skills, industries, and education
    options along with the count of live jobs for each option.

    This endpoint is useful for populating filter dropdowns/checkboxes
    with real-time counts.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Get filter options",
        description="Retrieve all available filter options (locations, skills, industries, education) with job counts",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "locations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                                "slug": {"type": "string"},
                                "count": {"type": "integer"}
                            }
                        }
                    },
                    "skills": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                                "slug": {"type": "string"},
                                "count": {"type": "integer"}
                            }
                        }
                    },
                    "industries": {"type": "array"},
                    "education": {"type": "array"},
                    "job_types": {"type": "array"},
                }
            }
        },
        tags=['Jobs'],
    )
    def get(self, request):
        """Get all filter options with job counts (cached ~5 min)."""
        from django.core.cache import cache

        cache_key = "job_filter_options_v2"
        cached = cache.get(cache_key)
        if cached is not None:
            response = Response(cached)
            response["Cache-Control"] = "public, max-age=120, stale-while-revalidate=300"
            response["X-Cache"] = "HIT"
            return response

        live_jobs = JobPost.objects.filter(status="Live")

        locations = list(
            City.objects.filter(locations__status="Live")
            .annotate(count=Count("locations", filter=Q(locations__status="Live"), distinct=True))
            .filter(count__gt=0)
            .order_by("-count", "name")
            .values("id", "name", "slug", "count")[:50]
        )

        skills = list(
            Skill.objects.filter(jobpost__status="Live")
            .annotate(count=Count("jobpost", filter=Q(jobpost__status="Live"), distinct=True))
            .filter(count__gt=0)
            .order_by("-count", "name")
            .values("id", "name", "slug", "count")[:50]
        )

        industries = list(
            Industry.objects.filter(jobpost__status="Live")
            .annotate(count=Count("jobpost", filter=Q(jobpost__status="Live"), distinct=True))
            .filter(count__gt=0)
            .order_by("-count", "name")
            .values("id", "name", "slug", "count")
        )

        education = list(
            Qualification.objects.filter(jobpost__status="Live")
            .annotate(count=Count("jobpost", filter=Q(jobpost__status="Live"), distinct=True))
            .filter(count__gt=0)
            .order_by("-count", "name")
            .values("id", "name", "slug", "count")
        )

        from peeldb.models import JOB_TYPE

        type_counts = {
            row["job_type"]: row["count"]
            for row in live_jobs.values("job_type").annotate(count=Count("id"))
        }
        job_types = [
            {"value": value, "label": label, "count": type_counts[value]}
            for value, label in JOB_TYPE
            if type_counts.get(value)
        ]

        payload = {
            "locations": locations,
            "skills": skills,
            "industries": industries,
            "education": education,
            "job_types": job_types,
        }
        cache.set(cache_key, payload, 300)
        response = Response(payload)
        response["Cache-Control"] = "public, max-age=120, stale-while-revalidate=300"
        response["X-Cache"] = "MISS"
        return response
