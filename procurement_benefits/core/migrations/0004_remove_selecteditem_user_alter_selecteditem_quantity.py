# Generated by Django 5.0.6 on 2024-07-11 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_selecteditem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selecteditem',
            name='user',
        ),
        migrations.AlterField(
            model_name='selecteditem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
