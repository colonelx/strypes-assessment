# Generated by Django 5.1.1 on 2024-09-24 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_item_inventory_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1, help_text='Quantity, for space calculation (qtty * size)', null=True),
        ),
    ]
