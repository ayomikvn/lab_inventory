# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-30 02:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('serialnumber', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('device_model', models.CharField(max_length=12)),
                ('device_type', models.CharField(max_length=24)),
                ('x0_ip', models.GenericIPAddressField(null=True)),
                ('x1_ip', models.GenericIPAddressField()),
                ('x1_subnetmask', models.GenericIPAddressField(null=True)),
                ('x1_gateway', models.GenericIPAddressField(null=True)),
                ('x3_ip', models.GenericIPAddressField(null=True)),
                ('x3_subnetmask', models.GenericIPAddressField(null=True)),
                ('x3_gateway', models.GenericIPAddressField(null=True)),
                ('pod_rdpip', models.GenericIPAddressField()),
                ('podnumber', models.IntegerField()),
                ('firmware', models.CharField(max_length=12, null=True)),
                ('available', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='RequestHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateField()),
                ('time_requested', models.TimeField()),
                ('date_returned', models.DateField(null=True)),
                ('time_returned', models.TimeField(null=True)),
                ('serialnumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podrequest.Device')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
