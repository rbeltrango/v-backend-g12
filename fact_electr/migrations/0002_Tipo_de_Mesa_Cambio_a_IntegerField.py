# Generated by Django 4.0.3 on 2022-04-20 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_electr', '0001_Creacion_Tablas_Comprobantes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='mesa',
            field=models.IntegerField(),
        ),
    ]