# Generated by Django 3.2 on 2022-02-28 06:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20220228_0430'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='post_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collection',
            name='refundable_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]