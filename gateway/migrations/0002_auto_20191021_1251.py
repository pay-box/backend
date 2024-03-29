# Generated by Django 2.2.6 on 2019-10-21 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gateway',
            name='currency',
            field=models.CharField(choices=[('irr', 'IRR'), ('usd', 'USD'), ('eur', 'EUR'), ('btc', 'BTC')], default='irr', max_length=5),
        ),
        migrations.AlterField(
            model_name='gateway',
            name='type',
            field=models.CharField(blank=True, choices=[('bahamta', 'Bahamta')], max_length=50, null=True),
        ),
    ]
