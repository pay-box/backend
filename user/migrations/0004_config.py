# Generated by Django 2.2.6 on 2019-11-02 19:04

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20191025_0420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('background_color', colorfield.fields.ColorField(default='#327F8F', max_length=18)),
                ('paid_background_color', colorfield.fields.ColorField(default='#45c175', max_length=18)),
                ('pay_background_color', colorfield.fields.ColorField(default='#4585c1', max_length=18)),
                ('error_background_color', colorfield.fields.ColorField(default='#808080', max_length=18)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
