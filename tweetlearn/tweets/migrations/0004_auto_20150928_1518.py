# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0003_auto_20150926_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='category',
            field=models.IntegerField(default=b'NON_ANNOTE', choices=[(b'NON_ANNOTE', -1), (b'NEGATIF', 0), (b'NEUTRE', 1), (b'POSITIF', 2)]),
        ),
    ]
