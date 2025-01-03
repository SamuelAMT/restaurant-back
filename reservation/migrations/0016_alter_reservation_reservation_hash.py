from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0015_rename_reservation_reserve_9df32c_idx_reservation_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='reservation',
            name='reservation_reserve_9df32c_idx',
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_hash',
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]