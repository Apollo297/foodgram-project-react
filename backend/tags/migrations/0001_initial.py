# Generated by Django 3.2.16 on 2024-03-03 12:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('color', models.CharField(max_length=7, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(regex='^[-a-zA-Z0-9_]+$')])),
            ],
        ),
    ]
