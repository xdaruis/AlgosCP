# Generated by Django 4.2.3 on 2023-08-25 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_problem_time_limit_submission_percentage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='percentage',
            new_name='result',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='status',
            new_name='test_cases',
        ),
    ]
