# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150504_0305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='questions',
        ),
        migrations.AddField(
            model_name='quizanswer',
            name='question',
            field=models.ForeignKey(default=0, to='core.QuizQuestion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='quiz',
            field=models.ForeignKey(default=0, to='core.Quiz'),
            preserve_default=False,
        ),
    ]
