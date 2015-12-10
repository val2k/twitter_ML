# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_auto_20150926_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.IntegerField(default=0, serialize=False, primary_key=True)),
                ('user', models.CharField(max_length=30)),
                ('text', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('request', models.CharField(max_length=100)),
                ('category', models.IntegerField(default=-1, choices=[(b'NON_ANNOTE', -1), (b'NEGATIF', 0), (b'NEUTRE', 1), (b'POSITIF', 2)])),
            ],
        ),
        migrations.DeleteModel(
            name='Tweets',
        ),
    ]
