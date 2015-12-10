# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='category',
            field=models.IntegerField(default=-1, choices=[(b'NON_ANNOTE', -1), (b'NEGATIF', 0), (b'NEUTRE', 1), (b'POSITIF', 2)]),
        ),
    ]
