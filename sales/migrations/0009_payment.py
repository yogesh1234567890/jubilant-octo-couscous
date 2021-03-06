# Generated by Django 3.1 on 2021-02-28 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amt', models.FloatField()),
                ('status', models.CharField(choices=[('FullyPaid', 'Fully paid'), ('PartiallyPaid', 'Partially paid'), ('NotPaid', 'Not Paid')], max_length=200)),
                ('mode', models.CharField(choices=[('cash', 'Cash'), ('card', 'Card'), ('Online', 'Online')], max_length=200)),
                ('sales_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.sales')),
            ],
            options={
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
