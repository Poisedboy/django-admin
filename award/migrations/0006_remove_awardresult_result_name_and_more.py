# Generated by Django 5.0.4 on 2024-04-15 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('award', '0005_awardresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='awardresult',
            name='result_name',
        ),
        migrations.RemoveField(
            model_name='awardresult',
            name='winner',
        ),
    ]
