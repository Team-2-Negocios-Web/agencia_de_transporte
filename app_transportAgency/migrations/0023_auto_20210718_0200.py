# Generated by Django 3.2.3 on 2021-07-18 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_transportAgency', '0022_auto_20210718_0126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='seating',
            new_name='bus',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='date_ticket',
            new_name='ticket_reservation',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='available',
        ),
        migrations.AddField(
            model_name='ticket',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_transportAgency.client'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_available',
            field=models.IntegerField(default=16),
        ),
        migrations.AlterField(
            model_name='bus',
            name='seating',
            field=models.ManyToManyField(to='app_transportAgency.Seating'),
        ),
        migrations.AlterField(
            model_name='tripscheduling',
            name='state',
            field=models.CharField(choices=[('2', 'en viaje'), ('4', 'cancelado'), ('1', 'A tiempo'), ('3', 'finalizado')], default='1', max_length=1),
        ),
        migrations.CreateModel(
            name='SeatAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_transportAgency.bus')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_transportAgency.client')),
                ('seating', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_transportAgency.seating')),
            ],
        ),
    ]
