# Generated by Django 3.2 on 2022-03-21 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20220320_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='is_cash_advance',
            field=models.BooleanField(default=False),
        ),
    ]
