# Generated by Django 5.1.3 on 2024-12-22 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activation', '0014_delete_softwareactivation'),
    ]

    operations = [
        migrations.AddField(
            model_name='initpayementoflicence',
            name='payement_phone_number',
            field=models.PositiveIntegerField(default=674579282),
        ),
    ]
