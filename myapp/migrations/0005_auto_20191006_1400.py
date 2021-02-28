# Generated by Django 2.2.5 on 2019-10-06 18:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20191002_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='publisher',
            name='country',
            field=models.CharField(default='USA', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2019, 10, 6, 18, 0, 31, 458287, tzinfo=utc)),
        ),
    ]