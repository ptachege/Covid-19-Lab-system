# Generated by Django 3.1.7 on 2021-09-15 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Labs', '0002_auto_20210915_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='id_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
