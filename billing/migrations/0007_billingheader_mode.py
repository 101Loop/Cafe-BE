# Generated by Django 2.0.7 on 2018-08-10 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_auto_20180806_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingheader',
            name='mode',
            field=models.CharField(choices=[('C', 'Cash'), ('I', 'Instamojo')], default='I', max_length=10, verbose_name='Mode of Payment'),
        ),
    ]
