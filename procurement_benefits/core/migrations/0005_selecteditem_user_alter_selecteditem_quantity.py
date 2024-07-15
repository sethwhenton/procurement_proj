# Generated by Django 5.0.6 on 2024-07-12 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_selecteditem_user_alter_selecteditem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='selecteditem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.customuser'),
        ),
        migrations.AlterField(
            model_name='selecteditem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
