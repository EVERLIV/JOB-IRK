"""
Clear old PeelJobs IT catalog and reload Truddy regional fixtures.

Usage:
    python manage.py reload_truddy_catalog
    python manage.py reload_truddy_catalog --skip-users
"""
from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection, transaction

from peeldb.models import (
    AppliedJobs,
    City,
    Company,
    Country,
    FunctionalArea,
    Industry,
    JobPost,
    Skill,
    State,
    TechnicalSkill,
    User,
)


class Command(BaseCommand):
    help = "Replace cities/skills/industries with Irkutsk-region Truddy catalog and reseed demo users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-users",
            action="store_true",
            help="Only reload fixtures; do not run create_test_users",
        )

    def handle(self, *args, **options):
        signal_processor = apps.get_app_config("haystack").signal_processor
        signal_processor.teardown()
        try:
            with transaction.atomic():
                self.stdout.write("Clearing jobs, skills, cities, industries...")
                AppliedJobs.objects.all().delete()
                JobPost.objects.all().delete()
                TechnicalSkill.objects.all().delete()
                # Drop M2M leftovers via full model wipe
                Skill.objects.all().delete()
                Industry.objects.all().delete()
                FunctionalArea.objects.all().delete()
                City.objects.all().delete()
                State.objects.all().delete()
                Country.objects.all().delete()
                # Remove demo companies so slug recreate works cleanly
                Company.objects.filter(
                    slug__in=["baikaltech", "baikalmarket", "sibirhire"]
                ).delete()

            call_command("load_initial_data")

            if not options["skip_users"]:
                # Wipe demo users then recreate with new jobs
                demo_emails = [
                    "admin@jobirk.local",
                    "hr@baikaltech.local",
                    "recruiter@baikaltech.local",
                    "consult@sibirhire.local",
                    "seeker@example.local",
                ]
                User.objects.filter(email__in=demo_emails).delete()
                call_command("create_test_users", clear=True)

            # Reset sequences so new inserts continue after fixture PKs
            self._reset_sequences()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Done. skills={Skill.objects.count()} cities={City.objects.count()} "
                    f"live_jobs={JobPost.objects.filter(status='Live').count()}"
                )
            )
        finally:
            signal_processor.setup()

    def _reset_sequences(self):
        tables = [
            "peeldb_country",
            "peeldb_state",
            "peeldb_city",
            "peeldb_skill",
            "peeldb_industry",
            "peeldb_functionalarea",
            "peeldb_jobpost",
            "peeldb_company",
        ]
        with connection.cursor() as cursor:
            for table in tables:
                try:
                    cursor.execute(
                        f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                        f"COALESCE((SELECT MAX(id) FROM {table}), 1))"
                    )
                except Exception:
                    pass
