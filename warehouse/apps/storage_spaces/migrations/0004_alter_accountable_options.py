# Generated by Django 5.1.1 on 2024-09-23 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage_spaces', '0003_prio_idx_for_accountables'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountable',
            options={'permissions': [('can_manage_inventory', 'Can manage inventory')]},
        ),
    ]
