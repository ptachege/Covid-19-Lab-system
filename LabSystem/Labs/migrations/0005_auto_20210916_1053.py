# Generated by Django 3.1.7 on 2021-09-16 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Labs', '0004_specimen_ref_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specimen',
            name='results',
            field=models.CharField(blank=True, choices=[('Positive', 'Positive'), ('Negative', 'Negative')], max_length=20, null=True),
        ),
    ]
