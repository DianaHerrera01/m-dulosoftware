# Generated by Django 4.2.16 on 2024-10-04 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0003_factura_precio_total_venta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='precio_total_venta',
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='precio_total_venta',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
