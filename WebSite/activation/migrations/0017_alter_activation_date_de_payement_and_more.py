# Generated by Django 5.1.3 on 2024-12-24 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activation', '0016_initpayementoflicence_operateur_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activation',
            name='date_de_payement',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='activation',
            name='small_date_de_payement',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='initpayementoflicence',
            name='date_of_initialise',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
