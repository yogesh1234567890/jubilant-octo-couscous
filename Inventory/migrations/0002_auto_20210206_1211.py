# Generated by Django 3.1 on 2021-02-06 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
