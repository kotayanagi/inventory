# Generated by Django 3.1.2 on 2020-10-14 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='商品名')),
                ('price', models.IntegerField(default=0, verbose_name='価格')),
                ('on_sale', models.BooleanField(default=False, verbose_name='販売中かどうか')),
                ('stock', models.IntegerField(default=0, verbose_name='在庫')),
                ('discount', models.IntegerField(default=0, verbose_name='値引き')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField(default=0, verbose_name='値引額')),
                ('number', models.IntegerField(default=0, verbose_name='数')),
                ('person', models.CharField(blank=True, max_length=255, null=True, verbose_name='担当者')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stock', verbose_name='商品')),
            ],
        ),
    ]
