# Generated by Django 5.1.3 on 2024-11-29 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0003_alter_useractivation_date_de_fin_de_validite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivation',
            name='date_de_fin_de_validite',
            field=models.DateField(),
        ),
    ]
