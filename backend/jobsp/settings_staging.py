"""
Staging settings for Railway + Neon deployment.
Uses simplified infrastructure: no Elasticsearch, no S3, no Celery broker.
"""
from .settings import *  # noqa: F403

DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # noqa: F405

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(  # noqa: F405
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,.railway.app",
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

# Email: log to console on staging (verification links appear in Railway logs)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Local file storage (ephemeral on Railway — fine for staging)
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
