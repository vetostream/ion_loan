# Generated by Django 3.2 on 2022-04-03 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_loan_loan_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='notes',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]