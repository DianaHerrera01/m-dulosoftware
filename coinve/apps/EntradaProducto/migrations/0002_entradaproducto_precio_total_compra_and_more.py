# Generated by Django 4.2.16 on 2024-10-01 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EntradaProducto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradaproducto',
            name='precio_total_compra',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='entradaproducto',
            name='precio_unidad_compra',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
