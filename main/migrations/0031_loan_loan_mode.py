# Generated by Django 3.2 on 2022-03-28 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20220328_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='loan_mode',
            field=models.CharField(choices=[('semi_monthly', 'Semi Monthly'), ('monthly', 'Monthly')], default='monthly', max_length=50),
        ),
    ]