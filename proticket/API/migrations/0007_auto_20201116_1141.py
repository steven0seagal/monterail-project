# Generated by Django 3.1.3 on 2020-11-16 10:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0006_auto_20201116_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='reserved_until',
            field=models.DateTimeField(default=datetime.datetime(2012, 1, 1, 12, 0, tzinfo=utc)),
        ),
    ]