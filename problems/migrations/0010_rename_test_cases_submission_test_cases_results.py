# Generated by Django 4.2.3 on 2023-08-31 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0009_remove_problem_num_tests'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='test_cases',
            new_name='test_cases_results',
        ),
    ]
