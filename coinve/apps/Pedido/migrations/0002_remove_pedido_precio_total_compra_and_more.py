# Generated by Django 4.2.16 on 2024-10-02 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pedido', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='precio_total_compra',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='precio_unidad_compra',
        ),
    ]
