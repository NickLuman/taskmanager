# Generated by Django 3.1.1 on 2020-09-30 21:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completion',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
