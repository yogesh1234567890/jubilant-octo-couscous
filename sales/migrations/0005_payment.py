# Generated by Django 3.1 on 2021-02-28 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_auto_20210223_0722'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.salesitem')),
            ],
            options={
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
