# Generated by Django 4.0.5 on 2022-06-17 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Models',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_Model', models.IntegerField()),
                ('order_Model', models.IntegerField()),
                ('value_dolar_Model', models.IntegerField()),
                ('value_rub_Model', models.IntegerField()),
                ('delivery_time_Model', models.DateTimeField()),
            ],
        ),
    ]
