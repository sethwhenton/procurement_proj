# Generated by Django 5.0.6 on 2024-07-12 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_selecteditem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selecteditem',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.customuser'),
        ),
    ]
