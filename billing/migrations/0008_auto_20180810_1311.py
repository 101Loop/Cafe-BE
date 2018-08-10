# Generated by Django 2.0.7 on 2018-08-10 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_billingheader_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingheader',
            name='mode',
            field=models.CharField(choices=[('C', 'Cash'), ('I', 'Instamojo')], max_length=10, verbose_name='Mode of Payment'),
        ),
    ]
