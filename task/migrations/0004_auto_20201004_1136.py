# Generated by Django 3.1.1 on 2020-10-04 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20200930_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='slug',
            field=models.SlugField(max_length=15, unique=True),
        ),
    ]
