# Generated by Django 2.0.9 on 2019-01-14 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('computer_room', '0005_auto_20190103_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinetunit',
            name='machine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.Machine'),
        ),
    ]
