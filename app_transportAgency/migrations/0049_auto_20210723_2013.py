# Generated by Django 3.2.3 on 2021-07-24 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_transportAgency', '0048_auto_20210723_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seatassignment',
            name='routes',
        ),
        migrations.RemoveField(
            model_name='seatassignment',
            name='ticket_reservation',
        ),
        migrations.AddField(
            model_name='seatassignment',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_transportAgency.ticket'),
        ),
        migrations.AlterField(
            model_name='tripscheduling',
            name='state',
            field=models.CharField(choices=[('2', 'en viaje'), ('4', 'cancelado'), ('3', 'finalizado'), ('1', 'A tiempo')], max_length=1),
        ),
    ]