# Generated by Django 4.2.16 on 2024-09-27 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_proveedor', models.CharField(max_length=100)),
                ('apellidos_proveedor', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoServicio',
            fields=[
                ('id_producto_servicio', models.AutoField(primary_key=True, serialize=False)),
                ('nom_producto_servicio', models.CharField(max_length=100)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proveedor.proveedor')),
            ],
        ),
    ]