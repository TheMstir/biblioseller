# Generated by Django 4.2.1 on 2023-07-08 22:38

from django.db import migrations, models
import mainlib.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainlib', '0002_alter_library_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to=mainlib.models.image_directory_path, verbose_name='изображение'),
        ),
    ]
