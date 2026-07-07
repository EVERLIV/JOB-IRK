from django.db import migrations, models
from django.utils import timezone


def backfill_auth_token_timestamps(apps, schema_editor):
    User = apps.get_model("peeldb", "User")
    now = timezone.now()

    User.objects.filter(
        activation_code__isnull=False,
        activation_code_created__isnull=True,
    ).exclude(activation_code="").update(activation_code_created=now)

    User.objects.filter(
        password_reset_token__isnull=False,
        password_reset_token_created__isnull=True,
    ).exclude(password_reset_token="").update(password_reset_token_created=now)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("peeldb", "0072_remove_facebook_github_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="activation_code_created",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(backfill_auth_token_timestamps, noop_reverse),
    ]
