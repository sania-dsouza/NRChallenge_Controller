# Generated by Django 3.1.7 on 2021-02-25 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controllerreadings',
            name='measured_date',
            field=models.DateField(),
        ),
    ]
