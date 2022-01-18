# Generated by Django 3.2 on 2022-01-15 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_loan_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='loan_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('declined', 'Declined'), ('approved', 'Approved')], default='pending', max_length=50),
        ),
    ]