# Generated by Django 4.0.3 on 2022-04-13 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plato',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('foto', models.ImageField(upload_to='')),
                ('disponible', models.BooleanField(default=True)),
                ('precio', models.FloatField()),
            ],
            options={
                'db_table': 'platos',
            },
        ),
    ]
