# Generated by Django 3.1 on 2021-02-06 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0002_auto_20210206_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product',
            field=models.IntegerField(default='40'),
            preserve_default=False,
        ),
    ]
