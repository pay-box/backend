# Generated by Django 2.2.6 on 2019-10-25 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20191025_0420'),
        ('transaction', '0004_auto_20191025_0340'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_application', to='user.Application'),
        ),
    ]
