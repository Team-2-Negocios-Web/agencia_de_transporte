# Generated by Django 3.2.3 on 2021-07-24 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_transportAgency', '0049_auto_20210723_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripscheduling',
            name='state',
            field=models.CharField(choices=[('2', 'en viaje'), ('3', 'finalizado'), ('1', 'A tiempo'), ('4', 'cancelado')], max_length=1),
        ),
    ]
