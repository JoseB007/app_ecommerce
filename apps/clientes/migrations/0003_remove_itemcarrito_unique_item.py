# Generated by Django 5.1.5 on 2025-02-21 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_itemcarrito_options'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='itemcarrito',
            name='unique_item',
        ),
    ]
