# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='empty@empty.com', max_length=254, unique=True)),
                ('nickname', models.CharField(default='empty', max_length=50, unique=True)),
                ('password', models.CharField(default='empty', max_length=128)),
                ('web_url', models.CharField(default='empty', max_length=200, unique=True)),
                ('widget_url', models.CharField(default='empty', max_length=200, unique=True)),
                ('mobile_url', models.CharField(default='empty', max_length=200, unique=True)),
                ('communication_key', models.CharField(default='empty', max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChattingLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(default='empty', max_length=100)),
                ('content', models.CharField(default='empty', max_length=500)),
                ('is_client', models.BooleanField(default=None)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='empty@empty.com', max_length=254, unique=True)),
                ('nickname', models.CharField(default='empty', max_length=50, unique=True)),
                ('password', models.CharField(default='empty', max_length=128)),
                ('is_online', models.BooleanField(default=False)),
                ('connection_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ImageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(default='empty', max_length=100)),
                ('image', models.ImageField(upload_to='screenshots')),
                ('is_client', models.BooleanField(default=None)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.CustomerService')),
            ],
        ),
        migrations.CreateModel(
            name='SerialNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serials', models.CharField(default='empty', max_length=50, unique=True)),
                ('is_used', models.BooleanField(default=None)),
            ],
        ),
        migrations.AddField(
            model_name='chattinglog',
            name='service_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.CustomerService'),
        ),
    ]
