# Generated by Django 3.2 on 2022-01-20 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20220120_0523'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='net_cash_out',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
