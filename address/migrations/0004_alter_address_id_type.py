from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('address', '0003_convert_ids_to_uuid'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
        ),

        migrations.RunSQL(
            sql="""
            UPDATE address 
            SET address_id = uuid_generate_v4()::text 
            WHERE address_id ~ '^[0-9]+$';

            ALTER TABLE address 
            ALTER COLUMN address_id TYPE uuid USING address_id::uuid;
            """,
            reverse_sql="""
            ALTER TABLE address 
            ALTER COLUMN address_id TYPE varchar;
            """
        ),
    ]