# Generated by Django 4.2.3 on 2023-08-03 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0009_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='problem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='problems.problem'),
        ),
    ]