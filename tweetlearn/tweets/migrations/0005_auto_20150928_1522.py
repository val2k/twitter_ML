# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20150928_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='category',
            field=models.IntegerField(default=-1, choices=[(-1, -1), (0, 0), (1, 1), (2, 2)]),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='request',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
