# Generated by Django 4.1.3 on 2022-11-09 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonDRF', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
