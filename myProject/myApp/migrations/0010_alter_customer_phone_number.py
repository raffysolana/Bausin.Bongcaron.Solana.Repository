# Generated by Django 5.1.3 on 2024-11-20 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0009_alter_customer_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=11),
        ),
    ]
