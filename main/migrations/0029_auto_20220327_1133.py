# Generated by Django 3.2 on 2022-03-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20220324_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='fee_others',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='llrf',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
