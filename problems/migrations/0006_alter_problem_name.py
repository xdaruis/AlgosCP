# Generated by Django 4.2.3 on 2023-08-01 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_alter_problem_constraints'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='name',
            field=models.CharField(default='lowercase letters only', max_length=50, unique=True),
        ),
    ]
