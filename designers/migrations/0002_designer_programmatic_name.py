# Generated by Django 3.2 on 2022-01-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='designer',
            name='programmatic_name',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
