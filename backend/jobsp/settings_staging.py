"""
Staging / soft-launch settings for Railway + Neon + Vercel.

Defaults stay lightweight (console email, local media, eager Celery, SimpleEngine).
Set env flags below to harden toward full production without a separate settings module.
"""
from django.core.exceptions import ImproperlyConfigured

from .settings import *  # noqa: F403

DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # noqa: F405

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(  # noqa: F405
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,.railway.app,.onrender.com,.loca.lt",
    ).split(",")
    if host.strip()
]

# Cross-origin auth: cookies are set by SvelteKit frontends, not Django
AUTH_COOKIE_DOMAIN = os.getenv("AUTH_COOKIE_DOMAIN") or None
AUTH_COOKIE_SECURE = os.getenv("AUTH_COOKIE_SECURE", "true").lower() == "true"
AUTH_COOKIE_SAMESITE = os.getenv("AUTH_COOKIE_SAMESITE", "Lax")

SESSION_COOKIE_SECURE = AUTH_COOKIE_SECURE
CSRF_COOKIE_SECURE = AUTH_COOKIE_SECURE
SESSION_COOKIE_SAMESITE = AUTH_COOKIE_SAMESITE
CSRF_COOKIE_SAMESITE = AUTH_COOKIE_SAMESITE

# Soft launch default: auto-verify (no SMTP). Full public launch: AUTO_VERIFY_EMAIL=false
AUTO_VERIFY_EMAIL = os.getenv("AUTO_VERIFY_EMAIL", "true").lower() == "true"  # noqa: F405

# Email: console by default; set EMAIL_BACKEND=django_ses.SESBackend (+ AWS_* SES vars) for prod
_email_backend = os.getenv("EMAIL_BACKEND", "").strip()  # noqa: F405
if _email_backend:
    EMAIL_BACKEND = _email_backend
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Media: local FS by default (ephemeral on Railway). Set MEDIA_STORAGE=s3 + AWS_* for durable uploads
_media_storage = os.getenv("MEDIA_STORAGE", "local").lower()  # noqa: F405
_aws_enabled = os.getenv("AWS_ENABLED", "false").lower() == "true"  # noqa: F405
if _media_storage == "s3" or _aws_enabled:
    if not AWS_STORAGE_BUCKET_NAME:  # noqa: F405
        raise ImproperlyConfigured(
            "MEDIA_STORAGE=s3 / AWS_ENABLED=true requires AWS_STORAGE_BUCKET_NAME"
        )
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ENABLED = True
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    AWS_ENABLED = False

# Search without Elasticsearch
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
    },
}
HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.BaseSignalProcessor"

# Run Celery tasks synchronously without Redis
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
