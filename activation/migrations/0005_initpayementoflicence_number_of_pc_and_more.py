# Generated by Django 5.1.3 on 2024-12-15 13:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activation', '0004_alter_activation_id_of_installed_pc'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='initpayementoflicence',
            name='number_of_pc',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='initpayementoflicence',
            name='promo_code',
            field=models.CharField(default='aaaa', max_length=60),
        ),
        migrations.AlterField(
            model_name='initpayementoflicence',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
