# Generated by Django 4.2.5 on 2023-10-04 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelobsidian', '0003_delete_authgroup_delete_authgrouppermissions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
    ]