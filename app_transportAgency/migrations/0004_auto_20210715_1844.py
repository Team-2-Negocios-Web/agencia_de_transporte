# Generated by Django 3.2.3 on 2021-07-16 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_transportAgency', '0003_auto_20210715_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_transportAgency.schedule'),
        ),
        migrations.AlterField(
            model_name='tripscheduling',
            name='state',
            field=models.CharField(choices=[('1', 'A tiempo'), ('3', 'finalizado'), ('2', 'en viaje'), ('4', 'cancelado')], default='1', max_length=1),
        ),
    ]