# Generated by Django 3.2.3 on 2021-07-16 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_transportAgency', '0015_alter_tripscheduling_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='route_schedule',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tripscheduling',
            name='state',
            field=models.CharField(choices=[('4', 'cancelado'), ('2', 'en viaje'), ('1', 'A tiempo'), ('3', 'finalizado')], default='1', max_length=1),
        ),
    ]
