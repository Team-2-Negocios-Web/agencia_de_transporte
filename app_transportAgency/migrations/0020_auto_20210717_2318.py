# Generated by Django 3.2.3 on 2021-07-18 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_transportAgency', '0019_auto_20210717_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='seating',
            field=models.ManyToManyField(blank=True, null=True, to='app_transportAgency.Seating'),
        ),
        migrations.AlterField(
            model_name='tripscheduling',
            name='state',
            field=models.CharField(choices=[('4', 'cancelado'), ('3', 'finalizado'), ('1', 'A tiempo'), ('2', 'en viaje')], default='1', max_length=1),
        ),
        migrations.DeleteModel(
            name='AsignacionDeAsientos',
        ),
    ]
