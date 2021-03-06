# Generated by Django 3.2.3 on 2021-07-23 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_transportAgency', '0031_auto_20210722_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seatassignment',
            name='client',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_transportAgency.client'),
        ),
        migrations.AlterField(
            model_name='tripscheduling',
            name='state',
            field=models.CharField(choices=[('1', 'A tiempo'), ('2', 'en viaje'), ('4', 'cancelado'), ('3', 'finalizado')], max_length=1),
        ),
    ]
