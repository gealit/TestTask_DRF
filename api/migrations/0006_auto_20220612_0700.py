# Generated by Django 3.1.6 on 2022-06-12 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20220612_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='deposit',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='term',
            field=models.IntegerField(null=True),
        ),
    ]
