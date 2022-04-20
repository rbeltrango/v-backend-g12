# Generated by Django 4.0.3 on 2022-04-20 02:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fact_electr', '0002_Tipo_de_Mesa_Cambio_a_IntegerField'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='numeroDocumentoCliente',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='tipoDocumentoCliente',
            field=models.CharField(choices=[['RUC', 'RUC'], ['DNI', 'DNI']], max_length=5, null=True),
        ),
    ]