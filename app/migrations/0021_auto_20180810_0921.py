# Generated by Django 2.0.7 on 2018-08-10 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20180810_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='products/images', verbose_name='Зображення'),
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, to='app.ProductImages', verbose_name='Інші зображення'),
        ),
    ]
