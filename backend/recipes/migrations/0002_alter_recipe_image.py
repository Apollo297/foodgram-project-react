# Generated by Django 3.2.16 on 2024-03-08 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes_images/', verbose_name='Ссылка на картинку на сайте'),
        ),
    ]
