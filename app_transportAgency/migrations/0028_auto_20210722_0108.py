# Generated by Django 3.2.3 on 2021-07-22 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_transportAgency', '0027_alter_tripscheduling_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='bus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app_transportAgency.bus'),
        ),
        migrations.AlterField(
            model_name='tripscheduling',
            name='state',
            field=models.CharField(choices=[('2', 'en viaje'), ('4', 'cancelado'), ('1', 'A tiempo'), ('3', 'finalizado')], max_length=1),
        ),
    ]
