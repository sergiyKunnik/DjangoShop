# Generated by Django 2.0.7 on 2018-08-02 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0012_auto_20180802_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='')),
                ('last_name', models.CharField(max_length=200, verbose_name='')),
                ('phone', models.CharField(max_length=200, verbose_name='')),
                ('address', models.CharField(max_length=200, verbose_name='')),
                ('type', models.CharField(choices=[('Самовиклик', 'Самовиклик'), ('Доставка', 'Доставка')], max_length=200, verbose_name='')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='')),
                ('comments', models.TextField(verbose_name='')),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Зомовлення',
                'verbose_name_plural': 'Зомовлення',
            },
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Product', verbose_name='Продукт'),
        ),
    ]
