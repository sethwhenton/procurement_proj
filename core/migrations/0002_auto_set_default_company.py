# core/migrations/0002_auto_set_default_company.py

from django.db import migrations, models

def set_default_company(apps, schema_editor):
    Company = apps.get_model('core', 'Company')
    Budget = apps.get_model('core', 'Budget')
    default_company, created = Company.objects.get_or_create(name='Default Company')
    Budget.objects.filter(company__isnull=True).update(company=default_company)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_default_company),
        migrations.AlterField(
            model_name='budget',
            name='company',
            field=models.ForeignKey(to='core.Company', on_delete=models.CASCADE),
        ),
    ]
