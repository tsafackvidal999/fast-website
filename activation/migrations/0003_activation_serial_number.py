# Generated by Django 5.1.3 on 2024-12-10 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activation', '0002_softwareactivation_activation_id_of_installed_pc'),
    ]

    operations = [
        migrations.AddField(
            model_name='activation',
            name='serial_number',
            field=models.CharField(default='', max_length=60),
        ),
    ]
