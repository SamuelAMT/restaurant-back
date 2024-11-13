from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0002_delete_blacklistedtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginlog',
            name='custom_user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]