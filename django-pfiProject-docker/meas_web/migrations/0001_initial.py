# Generated by Django 2.2.3 on 2019-08-20 14:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bore_id', models.CharField(max_length=20)),
                ('job_id', models.CharField(max_length=20)),
                ('device_id', models.CharField(max_length=20)),
                ('chemical_id', models.CharField(max_length=20)),
                ('concentration', models.CharField(max_length=20)),
                ('date', models.DateField(verbose_name='date')),
                ('time', models.TimeField(verbose_name='time')),
                ('status', models.CharField(choices=[('d', 'Draft'), ('p', 'Published')], default='d', max_length=1)),
                ('comment', models.CharField(default='', max_length=1000, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
    ]
