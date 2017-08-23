# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-22 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20170820_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='empty', max_length=32)),
                ('myid', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='empty@empty.com', max_length=254, unique=True)),
                ('nickname', models.CharField(default='empty', max_length=50, unique=True)),
                ('password', models.CharField(default='empty', max_length=128)),
                ('telephone', models.CharField(default='empty', max_length=20)),
                ('location', models.CharField(default='empty', max_length=100)),
                ('description', models.CharField(default='empty', max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='SecretKey',
        ),
    ]