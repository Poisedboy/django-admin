# Generated by Django 5.0.4 on 2024-04-15 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('award', '0002_awardentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='AwardJury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('award_show', models.CharField(max_length=255)),
                ('bio', models.TextField()),
                ('image', models.ImageField(upload_to='jury_images/')),
                ('user_id', models.IntegerField()),
                ('is_super', models.BooleanField(default=False)),
                ('hide_from_final_judging', models.BooleanField(default=False)),
            ],
        ),
    ]
