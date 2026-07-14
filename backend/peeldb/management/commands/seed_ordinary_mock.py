"""
Expand regional demo catalog: ordinary jobs + mock employers/seekers for Irkutsk area.
Also normalize JobPost.slug so detail pages resolve (legacy /slug/ and plain).
"""
from datetime import timedelta

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from peeldb.models import AppliedJobs, Company, JobPost, Skill, TechnicalSkill, User
from peeldb.slugify_ru import slugify_ru


EXTRA_JOBS = [
    # БайкалМаркет via company admin email owner later attached
    {
        "owner_email": "hr@baikaltech.local",
        "title": "Продавец непродовольственных товаров",
        "city": "Черемхово",
        "skills": ["Продажи", "Работа в торговом зале", "Мерчандайзинг"],
        "industries": ["Розничная торговля"],
        "min_year": 0,
        "max_year": 3,
        "min_salary": 40000,
        "max_salary": 58000,
        "vacancies": 2,
        "description": "<p>Продавец в отдел товаров для дома. Консультации, выкладка, работа с кассой сменой.</p>",
    },
    {
        "owner_email": "hr@baikaltech.local",
        "title": "Товаровед",
        "city": "Иркутск",
        "skills": ["Складской учёт", "1С Бухгалтерия", "Работа с первичной документацией"],
        "industries": ["Розничная торговля"],
        "min_year": 1,
        "max_year": 6,
        "min_salary": 60000,
        "max_salary": 85000,
        "vacancies": 1,
        "description": "<p>Товаровед: заказ поставщикам, контроль остатков, претензионная работа.</p>",
    },
    {
        "owner_email": "recruiter@baikaltech.local",
        "title": "Пекарь",
        "city": "Ангарск",
        "skills": ["Готовка", "Работа на кухне", "Санитарные нормы", "Работа в смене"],
        "industries": ["Общественное питание"],
        "min_year": 1,
        "max_year": 10,
        "min_salary": 52000,
        "max_salary": 72000,
        "vacancies": 2,
        "description": "<p>Пекарь в собственную пекарню магазина. Выпечка хлеба и выпечки, ночные смены по графику.</p>",
    },
    {
        "owner_email": "recruiter@baikaltech.local",
        "title": "Курьер на авто",
        "city": "Иркутск",
        "skills": ["Водительские права категории B", "Курьерская доставка", "Готовность к разъездам"],
        "industries": ["Транспорт и логистика"],
        "min_year": 0,
        "max_year": 5,
        "min_salary": 55000,
        "max_salary": 90000,
        "vacancies": 3,
        "description": "<p>Доставка интернет-заказов по Иркутску. Своё или служебное авто, оплата сдельная + оклад.</p>",
    },
    {
        "owner_email": "consult@sibirhire.local",
        "title": "Разнорабочий на стройку",
        "city": "Братск",
        "skills": ["Физическая выносливость", "Строительные нормы", "Работа в команде"],
        "industries": ["Строительство"],
        "min_year": 0,
        "max_year": 8,
        "min_salary": 55000,
        "max_salary": 80000,
        "vacancies": 6,
        "company_name": "СибирьСтрой",
        "description": "<p>Разнорабочие на жилой объект в Братске. Инструмент выдаём, спецодежда.</p>",
    },
    {
        "owner_email": "consult@sibirhire.local",
        "title": "Машинист экскаватора",
        "city": "Усть-Илимск",
        "skills": ["Работа с техникой", "Техника безопасности", "Вахтовый метод"],
        "industries": ["Строительство"],
        "min_year": 2,
        "max_year": 20,
        "min_salary": 110000,
        "max_salary": 160000,
        "vacancies": 2,
        "company_name": "СибирьСтрой",
        "description": "<p>Машинист экскаватора, права на спецтехнику. Вахта или проживание в городе.</p>",
    },
    {
        "owner_email": "consult@sibirhire.local",
        "title": "Повар в столовую",
        "city": "Северобайкальск",
        "skills": ["Готовка", "Кулинария", "Санитарные нормы"],
        "industries": ["Общественное питание"],
        "min_year": 1,
        "max_year": 12,
        "min_salary": 50000,
        "max_salary": 75000,
        "vacancies": 1,
        "company_name": "СеверСервис",
        "description": "<p>Повар в столовую предприятия. График 5/2, комплексные обеды.</p>",
    },
    {
        "owner_email": "consult@sibirhire.local",
        "title": "Продавец-кассир АЗС",
        "city": "Красноярск",
        "skills": ["Кассовая дисциплина", "Работа с клиентами", "Ответственность"],
        "industries": ["Розничная торговля"],
        "min_year": 0,
        "max_year": 5,
        "min_salary": 42000,
        "max_salary": 60000,
        "vacancies": 2,
        "company_name": "БайкалНефтепродукт",
        "description": "<p>Работа на АЗС: касса, зал, контроль смены. Обучение с нуля.</p>",
    },
    {
        "owner_email": "consult@sibirhire.local",
        "title": "Медсестра / медбрат",
        "city": "Иркутск",
        "skills": ["Уход за пациентами", "Медицинская документация", "Коммуникабельность"],
        "industries": ["Медицина и фармацевтика"],
        "min_year": 1,
        "max_year": 15,
        "min_salary": 45000,
        "max_salary": 70000,
        "vacancies": 2,
        "company_name": "Клиника Ангара",
        "description": "<p>Медсестра в частную клинику. Смены дневные, соцпакет.</p>",
    },
    {
        "owner_email": "consult@sibirhire.local",
        "title": "Автомеханик",
        "city": "Иркутск",
        "skills": ["Авторемонт", "Диагностика автомобилей", "Шиномонтаж"],
        "industries": ["Автосервис и автобизнес"],
        "min_year": 1,
        "max_year": 12,
        "min_salary": 70000,
        "max_salary": 120000,
        "vacancies": 2,
        "company_name": "АвтоСервис Байкал",
        "description": "<p>Автомеханик на СТО: ТО, ремонт, шиномонтаж. Проценты от заказов.</p>",
    },
    {
        "owner_email": "consult@sibirhire.local",
        "title": "Официант",
        "city": "Улан-Удэ",
        "skills": ["Обслуживание гостей", "Коммуникабельность", "Работа в смене"],
        "industries": ["Общественное питание"],
        "min_year": 0,
        "max_year": 5,
        "min_salary": 35000,
        "max_salary": 55000,
        "vacancies": 3,
        "company_name": "Кафе Байкал",
        "description": "<p>Официант в кафе в центре Улан-Удэ. Чаевые остаются вам.</p>",
    },
    {
        "owner_email": "consult@sibirhire.local",
        "title": "Комплектовщик склада",
        "city": "Чита",
        "skills": ["Комплектация заказов", "Складской учёт", "Физическая выносливость"],
        "industries": ["Складское хозяйство"],
        "min_year": 0,
        "max_year": 4,
        "min_salary": 45000,
        "max_salary": 65000,
        "vacancies": 4,
        "company_name": "ВостокЛогистика",
        "description": "<p>Комплектовщик на склад маркетплейса. Сдельная оплата, общежитие рядом.</p>",
    },
]

EXTRA_SEEKERS = [
    {
        "email": "anna.seller@example.local",
        "username": "anna.seller",
        "first_name": "Анна",
        "last_name": "Кузнецова",
        "password": "123456",
        "mobile": "+79131112233",
        "gender": "F",
        "city": "Иркутск",
        "experience_years": 3,
        "experience_months": 0,
        "current_salary": "48000",
        "expected_salary": "60000",
        "notice_period": "2 Weeks",
        "profile_description": "Продавец-консультант с опытом в продуктовом ритейле Иркутска.",
        "resume_title": "Анна Кузнецова — продавец",
        "is_looking_for_job": True,
        "is_open_to_offers": True,
        "relocation": False,
        "preferred_cities": ["Иркутск", "Ангарск"],
        "skills": [
            {"name": "Продажи", "years": 3, "proficiency": "Good", "is_major": True},
            {"name": "Кассовая дисциплина", "years": 3, "proficiency": "Good", "is_major": False},
            {"name": "Работа с клиентами", "years": 3, "proficiency": "Good", "is_major": False},
        ],
        "employment_history": [
            {
                "company": "Магнит",
                "designation": "Продавец-кассир",
                "years_ago_start": 0,
                "current_job": True,
                "job_profile": "Касса и зал, выкладка товара.",
            }
        ],
        "education": {
            "institute": "Иркутский колледж экономики и сервиса",
            "institute_address": "Иркутск",
            "qualification": "Среднее профессиональное",
            "specialization": "Коммерция",
            "score": "4.0",
            "years_ago_start": 6,
            "years_ago_end": 3,
        },
        "languages": [{"name": "Русский", "read": True, "write": True, "speak": True}],
    },
    {
        "email": "sergey.driver@example.local",
        "username": "sergey.driver",
        "first_name": "Сергей",
        "last_name": "Иванов",
        "password": "123456",
        "mobile": "+79135556677",
        "gender": "M",
        "city": "Братск",
        "experience_years": 7,
        "experience_months": 0,
        "current_salary": "85000",
        "expected_salary": "100000",
        "notice_period": "1 Month",
        "profile_description": "Водитель грузового транспорта, маршруты по Иркутской области.",
        "resume_title": "Сергей Иванов — водитель C",
        "is_looking_for_job": True,
        "is_open_to_offers": True,
        "relocation": True,
        "preferred_cities": ["Братск", "Иркутск", "Усть-Илимск"],
        "skills": [
            {"name": "Водительские права категории C", "years": 7, "proficiency": "Expert", "is_major": True},
            {"name": "Управление грузовым транспортом", "years": 7, "proficiency": "Expert", "is_major": False},
            {"name": "Логистика", "years": 3, "proficiency": "Average", "is_major": False},
        ],
        "employment_history": [
            {
                "company": "ЛесТранс",
                "designation": "Водитель категории C",
                "years_ago_start": 2,
                "current_job": True,
                "job_profile": "Перевозка пиломатериалов по области.",
            }
        ],
        "education": {
            "institute": "Братский индустриальный техникум",
            "institute_address": "Братск",
            "qualification": "Среднее профессиональное",
            "specialization": "Автомеханик",
            "score": "3.8",
            "years_ago_start": 12,
            "years_ago_end": 9,
        },
        "languages": [{"name": "Русский", "read": True, "write": True, "speak": True}],
    },
    {
        "email": "olga.cook@example.local",
        "username": "olga.cook",
        "first_name": "Ольга",
        "last_name": "Смирнова",
        "password": "123456",
        "mobile": "+79137778899",
        "gender": "F",
        "city": "Ангарск",
        "experience_years": 5,
        "experience_months": 0,
        "current_salary": "52000",
        "expected_salary": "65000",
        "notice_period": "2 Weeks",
        "profile_description": "Повар горячего цеха, опыт в столовых и кафе Ангарска.",
        "resume_title": "Ольга Смирнова — повар",
        "is_looking_for_job": True,
        "is_open_to_offers": True,
        "relocation": False,
        "preferred_cities": ["Ангарск", "Иркутск"],
        "skills": [
            {"name": "Готовка", "years": 5, "proficiency": "Good", "is_major": True},
            {"name": "Кулинария", "years": 5, "proficiency": "Good", "is_major": False},
            {"name": "Санитарные нормы", "years": 5, "proficiency": "Good", "is_major": False},
        ],
        "employment_history": [
            {
                "company": "Столовая №3",
                "designation": "Повар",
                "years_ago_start": 1,
                "current_job": True,
                "job_profile": "Горячий цех, комплексные обеды.",
            }
        ],
        "education": {
            "institute": "Ангарский техникум общественного питания",
            "institute_address": "Ангарск",
            "qualification": "Среднее профессиональное",
            "specialization": "Повар-кондитер",
            "score": "4.3",
            "years_ago_start": 9,
            "years_ago_end": 6,
        },
        "languages": [{"name": "Русский", "read": True, "write": True, "speak": True}],
    },
]


class Command(BaseCommand):
    help = "Normalize job slugs and add ordinary mock jobs/seekers for Truddy"

    def handle(self, *args, **options):
        signal_processor = apps.get_app_config("haystack").signal_processor
        signal_processor.teardown()
        try:
            # Drop leftover IT-titled jobs if any
            it_q = (
                JobPost.objects.filter(title__icontains="Developer")
                | JobPost.objects.filter(title__icontains="DevOps")
                | JobPost.objects.filter(title__icontains="Python")
                | JobPost.objects.filter(title__icontains="React")
                | JobPost.objects.filter(title__icontains="Backend")
                | JobPost.objects.filter(title__icontains="Frontend")
                | JobPost.objects.filter(title__icontains="QA ")
                | JobPost.objects.filter(title__icontains="Full Stack")
                | JobPost.objects.filter(title__icontains=".NET")
            )
            deleted, _ = it_q.delete()
            self.stdout.write(f"Removed IT-like jobs: {deleted}")

            # Also wipe skills that are still IT type
            Skill.objects.filter(skill_type="it").delete()

            self._normalize_slugs()
            self._add_extra_jobs()
            self._add_seekers()
            self._normalize_slugs()

            live = JobPost.objects.filter(status="Live").count()
            seekers = User.objects.filter(user_type="JS").count()
            self.stdout.write(
                self.style.SUCCESS(f"Done. live_jobs={live} seekers={seekers}")
            )
        finally:
            signal_processor.setup()

    def _normalize_slugs(self):
        used = set()
        for job in JobPost.objects.all().order_by("id"):
            company = job.company_name or (job.company.name if job.company_id else "truddy")
            base = slugify_ru(f"{job.title}-{company}-{job.id}") or f"job-{job.id}"
            # Store as /slug/ for compatibility with older API retrieve
            plain = base
            n = 1
            while True:
                slug = f"/{plain}/"
                conflict = JobPost.objects.filter(slug=slug).exclude(pk=job.pk).exists()
                if plain not in used and not conflict:
                    break
                plain = f"{base}-{n}"
                n += 1
            used.add(plain)
            if job.slug != slug:
                job.slug = slug
                job.save(update_fields=["slug"])
        self.stdout.write(f"Normalized slugs for {JobPost.objects.count()} jobs")

    def _add_extra_jobs(self):
        from peeldb.management.commands.create_test_users import Command as SeedCmd

        seed = SeedCmd()
        seed.country = seed._get_country() if hasattr(seed, "_get_country") else None
        # Reuse helper methods
        from peeldb.models import City, Country, Industry

        country = Country.objects.filter(status="Enabled").first()
        created = 0
        for raw in EXTRA_JOBS:
            owner = User.objects.filter(email=raw["owner_email"]).first()
            if not owner:
                self.stdout.write(self.style.WARNING(f"Skip job, no owner {raw['owner_email']}"))
                continue
            # Avoid duplicates by title+owner
            if JobPost.objects.filter(user=owner, title=raw["title"]).exists():
                continue
            city = City.objects.filter(name=raw["city"], status="Enabled").first()
            company_label = raw.get("company_name") or (
                owner.company.name if owner.company_id else f"{owner.first_name}"
            )
            slug = slugify_ru(f"{raw['title']}-{company_label}")
            base = slug
            i = 1
            while JobPost.objects.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            job = JobPost.objects.create(
                user=owner,
                company=owner.company,
                title=raw["title"],
                slug=slug,
                description=raw["description"],
                vacancies=raw.get("vacancies", 1),
                min_year=raw.get("min_year", 0),
                max_year=raw.get("max_year", 5),
                min_month=0,
                max_month=0,
                min_salary=raw.get("min_salary", 0),
                max_salary=raw.get("max_salary", 0),
                salary_type="Month",
                job_type="full-time",
                work_mode="in-office",
                status="Live",
                published_on=timezone.now() - timedelta(hours=created),
                fresher=raw.get("min_year", 0) == 0,
                country=country,
                meta_title=raw["title"],
                meta_description=raw["title"],
                company_name=company_label,
                company_address=owner.company.address if owner.company_id else "",
                company_description=owner.company.profile if owner.company_id else "",
            )
            if city:
                job.location.add(city)
            for name in raw.get("skills", []):
                skill = Skill.objects.filter(name__icontains=name, status="Active").first()
                if skill:
                    job.skills.add(skill)
            for name in raw.get("industries", []):
                ind = Industry.objects.filter(name__icontains=name, status="Active").first()
                if ind:
                    job.industry.add(ind)
            created += 1
        self.stdout.write(f"Added extra jobs: {created}")

    def _add_seekers(self):
        from peeldb.management.commands.create_test_users import Command as SeedCmd

        seed = SeedCmd()
        seed.cities = list(__import__("peeldb.models", fromlist=["City"]).City.objects.filter(status="Enabled"))
        seed.skills = list(Skill.objects.filter(status="Active"))
        seed.industries = list(
            __import__("peeldb.models", fromlist=["Industry"]).Industry.objects.filter(status="Active")
        )
        seed.qualifications = list(
            __import__("peeldb.models", fromlist=["Qualification"]).Qualification.objects.filter(
                status="Active"
            )
        )
        seed.languages = list(
            __import__("peeldb.models", fromlist=["Language"]).Language.objects.all()
        )
        seed.country = __import__("peeldb.models", fromlist=["Country"]).Country.objects.filter(
            status="Enabled"
        ).first()
        seed.test_users = {}
        for data in EXTRA_SEEKERS:
            if User.objects.filter(email=data["email"]).exists():
                continue
            seed._create_jobseeker(data)
        self.stdout.write(f"Seekers total JS: {User.objects.filter(user_type='JS').count()}")
