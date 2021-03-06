# Generated by Django 3.2.3 on 2021-07-16 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_transportAgency', '0005_auto_20210715_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='name_seating',
            field=models.ManyToManyField(to='app_transportAgency.Seating'),
        ),
        migrations.AlterField(
            model_name='tripscheduling',
            name='state',
            field=models.CharField(choices=[('2', 'en viaje'), ('3', 'finalizado'), ('4', 'cancelado'), ('1', 'A tiempo')], default='1', max_length=1),
        ),
    ]
