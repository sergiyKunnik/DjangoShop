# Generated by Django 2.0.7 on 2018-07-31 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Бренд')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренди',
            },
        ),
    ]
