# Generated by Django 2.1.4 on 2019-01-01 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rawmaterialstock',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='rawmaterialstock',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='rawmaterialstock',
            name='raw_material',
        ),
        migrations.RemoveField(
            model_name='rawmaterialstock',
            name='warehouse',
        ),
        migrations.RemoveField(
            model_name='stockcredit',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='stockcredit',
            name='stock',
        ),
        migrations.DeleteModel(
            name='RawMaterialStock',
        ),
        migrations.DeleteModel(
            name='StockCredit',
        ),
    ]