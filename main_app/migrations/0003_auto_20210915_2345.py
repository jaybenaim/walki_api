# Generated by Django 3.2.7 on 2021-09-15 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210915_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
