# Generated by Django 4.2.6 on 2023-10-29 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestProducts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionlist',
            name='created_date',
        ),
        migrations.AddField(
            model_name='sessionlist',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
