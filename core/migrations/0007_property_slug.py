# Generated by Django 3.2.15 on 2022-08-28 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_property_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='slug',
            field=models.SlugField(default='this'),
            preserve_default=False,
        ),
    ]
