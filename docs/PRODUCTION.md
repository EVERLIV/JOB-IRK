# Production release runbook (Truddy.ru)

Stack: **Vercel** (site + recruiter) → **Railway** (Django API) → **Neon** (PostgreSQL).

Current soft-launch profile uses [`backend/jobsp/settings_staging.py`](../backend/jobsp/settings_staging.py).

| Component | URL |
|-----------|-----|
| Site | https://job-irk.vercel.app |
| Recruiter | https://job-irk-recruiter.vercel.app |
| API | https://api-production-e35c.up.railway.app/api/v1 |

---

## 1. Seed data (once per database)

Reference data (Irkutsk-region cities + ordinary work skills) plus curated БайкалМаркет demo jobs (~15 Live).

```powershell
$env:DATABASE_URL = "postgresql://USER:PASSWORD@HOST/neondb?sslmode=require"
powershell -File scripts/seed-production.ps1
```

What runs: `migrate` → `reload_truddy_catalog` (clears old IT catalog, loads fixtures, `create_test_users`).

Do **not** run `create_test_data` on production (bulk spam).

Geography: Иркутская область + Бурятия / Забайкалье / Красноярск (сосед), без Москвы и всей РФ.
Skills: продажи, водители, склад, общепит, стройка, охрана и т.п. (не Java/Python).

### Demo logins (change passwords after launch)

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@jobirk.local` | `123456` |
| HR | `hr@baikaltech.local` | `123456` |
| Recruiter | `recruiter@baikaltech.local` | `123456` |
| Jobseeker | `seeker@example.local` | `123456` |

### Adding more vacancies

- Recruiter UI: https://job-irk-recruiter.vercel.app (login as HR/recruiter)
- API: `POST /api/v1/recruiter/auth/login/` then `POST /api/v1/recruiter/jobs/create/` + `.../publish/`
- Jobseeker login is separate: `POST /api/v1/auth/login/` (JS users only)

---

## 2. Environment checklist

### Railway (API)

See [`backend/.env.staging.example`](../backend/.env.staging.example).

| Variable | Soft launch | Full public |
|----------|-------------|-------------|
| `DJANGO_SETTINGS_MODULE` | `jobsp.settings_staging` | same |
| `DEBUG` | `false` | `false` |
| `SECRET_KEY` | strong secret | rotate if leaked |
| `DATABASE_URL` | Neon + `sslmode=require` | same |
| `PEEL_URL` | API public URL | same |
| `ALLOWED_HOSTS` | API host + `.railway.app` | + custom domain |
| `SITE_FRONTEND_URL` | `https://job-irk.vercel.app` | custom domain |
| `RECRUITER_FRONTEND_URL` | `https://job-irk-recruiter.vercel.app` | custom domain |
| `AUTH_COOKIE_SECURE` | `true` | `true` |
| `AUTH_COOKIE_SAMESITE` | `Lax` | `Lax` (or `None` only with shared parent domain plan) |
| `AUTO_VERIFY_EMAIL` | `true` | **`false`** |
| `DEFAULT_FROM_EMAIL` | `Truddy <noreply@…>` | verified domain |
| `EMAIL_BACKEND` | unset (console) | `django_ses.SESBackend` |
| `AWS_ACCESS_KEY` / `AWS_SECRET_KEY` | unset | SES (+ S3) keys |
| `AWS_SES_REGION_NAME` / `AWS_SES_REGION_ENDPOINT` | unset | e.g. `eu-central-1` |
| `MEDIA_STORAGE` / `AWS_ENABLED` | local / false | `s3` / `true` |
| `AWS_STORAGE_BUCKET_NAME` | unset | media bucket |

Deploy helper: `powershell -File scripts/deploy-railway-backend.ps1`

### Vercel (site `job-irk` + recruiter `job-irk-recruiter`)

| Variable | Site | Recruiter |
|----------|------|-----------|
| `PUBLIC_API_BASE_URL` | `https://api-production-e35c.up.railway.app/api/v1` | same |
| `PUBLIC_SITE_URL` | site URL | recruiter URL |
| `PUBLIC_RECRUITER_URL` | recruiter URL | — |
| `PUBLIC_JOBSEEKER_URL` | — | site URL |

Helper: `powershell -File scripts/set-vercel-env.ps1 -ApiBaseUrl https://api-production-e35c.up.railway.app/api/v1`

Browsers call `/api/v1` on the same origin; SvelteKit proxies to Railway so JWT cookies work.

---

## 3. Release order

1. Confirm Neon `DATABASE_URL` on Railway.
2. Deploy API (`bin/start.sh` runs migrate + collectstatic).
3. Seed once: `scripts/seed-production.ps1`.
4. Set Vercel `PUBLIC_*` and redeploy both frontends.
5. Smoke:
   - `GET /api/v1/jobs/` → ~15 Live
   - Jobseeker login on site
   - Recruiter login + create/publish job
6. Soft launch OK with `AUTO_VERIFY_EMAIL=true`.
7. Before open registration: hard production steps below.

---

## 4. Hard production (before open registration)

Wire these on Railway when you leave soft-launch mode:

```text
AUTO_VERIFY_EMAIL=false
EMAIL_BACKEND=django_ses.SESBackend
AWS_ACCESS_KEY=...
AWS_SECRET_KEY=...
AWS_SES_REGION_NAME=eu-central-1
AWS_SES_REGION_ENDPOINT=email.eu-central-1.amazonaws.com
DEFAULT_FROM_EMAIL=Truddy <noreply@your-verified-domain>
MEDIA_STORAGE=s3
AWS_ENABLED=true
AWS_STORAGE_BUCKET_NAME=your-media-bucket
```

Then:

1. Verify SES domain / sender identity.
2. Confirm register → verification email arrives; reset password works.
3. Upload a logo/resume and confirm it survives Railway redeploy (S3).
4. Rotate Neon DB password if it was ever shared in chat/logs.
5. Change all demo account passwords (or disable demo emails).

Optional later: Redis/Celery workers, Elasticsearch, Sentry, custom domains.

---

## 6. Why pages feel slow (1–2 minutes)

Measured stack (Vercel SSR → Railway API → Neon):

| Layer | Typical wait |
|-------|--------------|
| Neon autosuspend wake | 3–10+ s on first query |
| Railway free sleep / cold dyno | +several seconds |
| Home SSR used to call API **sequentially** | ~2× API latency |
| `filter-options` heavy COUNT queries every request | 3+ s when cold |

Mitigations in code: parallel SSR, LocMem cache for filter-options, fewer N+1 queries, short `Cache-Control`, auth timeouts, GitHub Actions keepalive cron.

Still required for stable speed:

1. Neon Console → disable **Scale to zero** / keep compute awake (or paid plan).
2. Railway → keep service always on (not slept).
3. Prefer Neon region close to Railway region.

---

## 5. What not to do

- Do not run `create_test_data` on Neon production.
- Do not use `load_test_jobs.py` / `load_education_data.py` (legacy non-RF).
- Do not create JobPosts in Django admin (model not registered); use recruiter UI/API.
- Do not paste env values with trailing `\r\n` (Windows); frontend `clean()` strips them, but prefer clean secrets.
