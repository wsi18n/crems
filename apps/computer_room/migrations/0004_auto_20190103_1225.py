# Generated by Django 2.0.9 on 2019-01-03 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer_room', '0003_auto_20181227_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinet',
            name='used_unit_number',
            field=models.CharField(default='0', max_length=255),
        ),
    ]
