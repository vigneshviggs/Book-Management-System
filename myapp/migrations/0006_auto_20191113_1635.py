# Generated by Django 2.2.5 on 2019-11-13 21:35

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20191006_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='num_reviews',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2019, 11, 13, 21, 35, 5, 116342, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer', models.EmailField(max_length=254)),
                ('rating', models.PositiveIntegerField()),
                ('comments', models.TextField(blank=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Book')),
            ],
        ),
    ]
