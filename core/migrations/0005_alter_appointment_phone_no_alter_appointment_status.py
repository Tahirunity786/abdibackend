# Generated by Django 5.0.3 on 2024-04-06 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_appointment_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='phone_no',
            field=models.BigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Ok', 'Ok'), ('Pending', 'Pending'), ('Decline', 'Decline')], db_index=True, max_length=100),
        ),
    ]
