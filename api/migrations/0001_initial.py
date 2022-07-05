# Generated by Django 3.1.6 on 2022-06-11 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=100)),
                ('term_min', models.IntegerField()),
                ('term_max', models.IntegerField()),
                ('rate_min', models.DecimalField(decimal_places=2, max_digits=4)),
                ('rate_max', models.DecimalField(decimal_places=2, max_digits=4)),
                ('payment_min', models.IntegerField()),
                ('payment_max', models.IntegerField()),
            ],
        ),
    ]
