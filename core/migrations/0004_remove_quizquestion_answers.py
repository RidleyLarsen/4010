# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150504_0315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizquestion',
            name='answers',
        ),
    ]
