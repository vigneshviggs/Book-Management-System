# Generated by Django 2.2.5 on 2019-10-02 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20191002_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='optional',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='publisher',
            name='country',
            field=models.CharField(default='USA', max_length=2000),
        ),
        migrations.AlterField(
            model_name='member',
            name='address',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='member',
            name='city',
            field=models.CharField(default='Windsor', max_length=20),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.IntegerField(choices=[(0, 'Purchase'), (1, 'Borrow')], default=1)),
                ('order_date', models.DateField()),
                ('books', models.ManyToManyField(to='myapp.Book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Member')),
            ],
        ),
    ]
