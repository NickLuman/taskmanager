# Generated by Django 3.1.1 on 2020-10-05 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_auto_20201005_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskchange',
            name='changed_status',
            field=models.CharField(default='No changes.', max_length=35),
        ),
    ]
