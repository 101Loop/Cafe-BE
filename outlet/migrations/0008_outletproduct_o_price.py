# Generated by Django 2.1.4 on 2019-02-15 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outlet', '0007_auto_20190102_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='outletproduct',
            name='o_price',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Price'),
        ),
    ]
