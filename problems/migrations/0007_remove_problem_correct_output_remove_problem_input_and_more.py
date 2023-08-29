# Generated by Django 4.2.3 on 2023-08-29 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0006_rename_percentage_submission_result_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='correct_output',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='input',
        ),
        migrations.AddField(
            model_name='problem',
            name='number_of_testcases',
            field=models.IntegerField(default=1),
        ),
    ]