# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 12:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20170810_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='RobotInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(default='empty', max_length=150)),
                ('answer', models.CharField(default='empty', max_length=500)),
                ('keyword', models.CharField(default='empty', max_length=100)),
                ('weight', models.IntegerField(default=0)),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Admin')),
            ],
        ),
    ]