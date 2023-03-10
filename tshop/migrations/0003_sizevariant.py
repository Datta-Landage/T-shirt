# Generated by Django 3.1.5 on 2021-01-25 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tshop', '0002_auto_20210125_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sizevariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Xtra Large')], max_length=50)),
                ('tshirt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tshop.tshirt')),
            ],
        ),
    ]
