# Generated by Django 3.2.15 on 2022-09-12 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertykey', to='core.property'),
        ),
    ]
