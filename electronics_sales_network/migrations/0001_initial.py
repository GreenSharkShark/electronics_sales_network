# Generated by Django 4.2.6 on 2023-11-21 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='почта')),
                ('country', models.CharField(max_length=100, verbose_name='страна')),
                ('city', models.CharField(max_length=100, verbose_name='город')),
                ('street', models.CharField(max_length=100, verbose_name='улица')),
                ('house_number', models.CharField(max_length=10, verbose_name='номер дома')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('model', models.CharField(max_length=255, verbose_name='модель')),
                ('release_date', models.DateField(verbose_name='дата выхода на рынок')),
            ],
        ),
        migrations.CreateModel(
            name='ChainLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('debt_to_the_supplier', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='задолженность перед поставщиком')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True)),
                ('is_factory', models.BooleanField(default=False)),
                ('is_retail_network', models.BooleanField(default=False)),
                ('is_individual_entrepreneur', models.BooleanField(default=False)),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='electronics_sales_network.contact', verbose_name='контакты')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='electronics_sales_network.product', verbose_name='продукты')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='electronics_sales_network.chainlink', verbose_name='поставщик')),
            ],
        ),
    ]