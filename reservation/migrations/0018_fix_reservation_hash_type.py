from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0017_alter_reservation_reservation_hash_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE reservation
            ALTER COLUMN reservation_hash
            TYPE UUID
            USING reservation_hash::uuid;
            """,
            reverse_sql="""
            ALTER TABLE reservation
            ALTER COLUMN reservation_hash
            TYPE VARCHAR(36)
            USING reservation_hash::varchar;
            """,
        ),
    ]