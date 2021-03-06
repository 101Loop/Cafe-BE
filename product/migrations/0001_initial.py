# Generated by Django 2.1.4 on 2019-01-01 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import product.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taxation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date/Time')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Date/Time Modified')),
                ('name', models.CharField(max_length=254, unique=True, verbose_name='Category Name')),
                ('sku_prefix', models.CharField(max_length=4, unique=True, verbose_name='SKU Prefix')),
                ('hsn', models.CharField(max_length=6, verbose_name='HSN Code')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('d_uom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='stock.UnitOfMeasurementMaster', verbose_name='Default Unit of Measurement')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ComboProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date/Time')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Date/Time Modified')),
                ('name', models.CharField(max_length=254, unique=True, verbose_name='Combo Name')),
                ('price', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Price')),
                ('is_inclusive', models.BooleanField(default=True, verbose_name='Price inclusive of Tax?')),
                ('from_date', models.DateField(blank=True, null=True, verbose_name='Valid From (Date)')),
                ('to_date', models.DateField(blank=True, null=True, verbose_name='Valid Till (Date)')),
                ('from_time', models.TimeField(blank=True, null=True, verbose_name='Valid From (Time)')),
                ('to_time', models.TimeField(blank=True, null=True, verbose_name='Valid Till (Time)')),
            ],
            options={
                'verbose_name': 'Combo Product',
                'verbose_name_plural': 'Combo Products',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date/Time')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Date/Time Modified')),
                ('name', models.CharField(max_length=254, unique=True, verbose_name='Product Name')),
                ('price', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Price')),
                ('is_inclusive', models.BooleanField(default=True, verbose_name='Price inclusive of Tax?')),
                ('sku', models.CharField(max_length=28, unique=True, verbose_name='SKU Code')),
                ('o_hsn', models.CharField(blank=True, max_length=6, null=True, verbose_name='Override HSN Code')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.Category', verbose_name='Category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('instate_tax', models.ManyToManyField(blank=True, related_name='productinstate', to='taxation.Tax', verbose_name='In-State Tax')),
                ('interstate_tax', models.ManyToManyField(blank=True, related_name='productinterstate', to='taxation.Tax', verbose_name='Inter-State Tax')),
                ('uom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stock.UnitOfMeasurementMaster', verbose_name='Unit of Measurement')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date/Time')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Date/Time Modified')),
                ('name', models.CharField(max_length=154, verbose_name='Name')),
                ('image', models.ImageField(upload_to=product.utils.product_image_upload, verbose_name='Image')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.AddField(
            model_name='comboproduct',
            name='combo_product',
            field=models.ManyToManyField(to='product.Product', verbose_name='Combo Products'),
        ),
        migrations.AddField(
            model_name='comboproduct',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comboproduct',
            name='instate_tax',
            field=models.ManyToManyField(blank=True, related_name='comboinstate', to='taxation.Tax', verbose_name='In-State Tax'),
        ),
        migrations.AddField(
            model_name='comboproduct',
            name='interstate_tax',
            field=models.ManyToManyField(blank=True, related_name='combointerstate', to='taxation.Tax', verbose_name='Inter-State Tax'),
        ),
        migrations.AddField(
            model_name='comboproduct',
            name='uom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stock.UnitOfMeasurementMaster', verbose_name='Unit of Measurement'),
        ),
    ]
