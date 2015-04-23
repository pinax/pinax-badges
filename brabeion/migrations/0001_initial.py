# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeAward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('awarded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.CharField(max_length=255)),
                ('level', models.IntegerField()),
                ('user', models.ForeignKey(related_name='badges_earned', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
