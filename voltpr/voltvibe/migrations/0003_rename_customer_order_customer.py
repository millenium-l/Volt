# Generated by Django 5.1.2 on 2024-10-18 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voltvibe', '0002_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Customer',
            new_name='customer',
        ),
    ]