# Generated by Django 3.2.3 on 2021-07-18 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_transportAgency', '0018_auto_20210715_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus',
            name='name_seating',
        ),
        migrations.RemoveField(
            model_name='bus',
            name='seatings',
        ),
        migrations.CreateModel(
            name='AsignacionDeAsientos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_transportAgency.bus')),
                ('seating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_transportAgency.seating')),
            ],
            options={
                'unique_together': {('bus', 'seating')},
            },
        ),
    ]