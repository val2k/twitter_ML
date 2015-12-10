# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('id', models.IntegerField(default=0, serialize=False, primary_key=True)),
                ('user', models.CharField(max_length=30)),
                ('text', models.TextField()),
                ('date', models.DateField()),
                ('request', models.CharField(max_length=100)),
                ('category', models.IntegerField(default=b'NON_ANNOTE', choices=[(b'NON_ANNOTE', -1), (b'NEGATIF', 0), (b'NEUTRE', 1), (b'POSITIF', 2)])),
            ],
        ),
    ]
