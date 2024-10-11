# Generated by Django 4.2.16 on 2024-10-02 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Pedido', '0001_initial'),
        ('EntradaProducto', '0002_entradaproducto_precio_total_compra_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradaproducto',
            name='pedido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedido.pedido'),
        ),
    ]
