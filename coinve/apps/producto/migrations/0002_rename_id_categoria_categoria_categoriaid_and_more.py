# Generated by Django 4.2.16 on 2024-09-26 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoria',
            old_name='id_categoria',
            new_name='categoriaID',
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='precio_unidad_compra',
            new_name='preciounidadcompra',
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='precio_unidad_venta',
            new_name='preciounidadventa',
        ),
    ]
