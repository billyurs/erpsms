# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import erpsms.erpsms.multifield


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlerURls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, db_index=True)),
                ('url', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('createdon', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Farmingdetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, db_index=True)),
                ('url', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('createdon', models.DateTimeField(auto_now_add=True)),
                ('info', models.IntegerField(default=0)),
                ('search_key', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PushNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_preferences', erpsms.erpsms.multifield.MultiSelectField(max_length=500, choices=[(b'------', b'------')])),
                ('notifyme', models.BooleanField(default=False)),
                ('user_prefernces_customization', models.TextField()),
                ('last_notified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('farming_interest', models.CharField(max_length=10, db_index=True)),
                ('crop_place', models.CharField(max_length=10)),
                ('user_customization', models.TextField()),
                ('type_of_user', models.CharField(db_index=True, max_length=100, choices=[(b'Farmer', b'Farmer'), (b'Sales Agent', b'Sales Agent'), (b'Delivery Agent', b'Delivery Agent'), (b'Bank Emp', b'Bank Emp'), (b'CRM Executive', b'CRM Executive'), (b'Farming Labour', b'Farming Labour')])),
                ('type_of_farming', models.CharField(db_index=True, max_length=100, choices=[(b'Food Production', b'Food Production'), (b'Diary Products', b'Diary Products'), (b'Animal husbandry', b'Animal husbandry')])),
                ('userid', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='pushnotification',
            name='userid',
            field=models.ForeignKey(to='api.UserInfo'),
        ),
    ]
