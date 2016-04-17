# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('URL_original', models.CharField(max_length=64)),
                ('URL_acortada', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
