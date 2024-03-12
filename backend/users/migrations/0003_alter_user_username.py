# Generated by Django 3.2.16 on 2024-03-10 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.SlugField(help_text='Имя пользователя', max_length=150, unique=True, verbose_name='Имя пользователя'),
        ),
    ]