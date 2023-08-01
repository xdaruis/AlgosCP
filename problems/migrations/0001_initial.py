# Generated by Django 4.2.3 on 2023-07-31 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('example', models.CharField(max_length=50)),
                ('constraints', models.CharField(max_length=50)),
            ],
        ),
    ]
