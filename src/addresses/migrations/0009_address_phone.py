# Generated by Django 2.1.5 on 2019-09-22 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0008_auto_20190423_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
