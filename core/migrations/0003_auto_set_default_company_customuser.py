# core/migrations/0003_auto_set_default_company_customuser.py

from django.db import migrations, models

def set_default_company(apps, schema_editor):
    Company = apps.get_model('core', 'Company')
    CustomUser = apps.get_model('core', 'CustomUser')
    Department = apps.get_model('core', 'Department')
    Budget = apps.get_model('core', 'Budget')
    default_company, created = Company.objects.get_or_create(name='Default Company')
    
    # Set default company for existing CustomUser entries
    CustomUser.objects.filter(company__isnull=True).update(company=default_company)
    
    # Set default company for existing Department entries
    Department.objects.filter(company__isnull=True).update(company=default_company)
    
    # Set default company for existing Budget entries
    Budget.objects.filter(company__isnull=True).update(company=default_company)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_set_default_company'),
    ]

    operations = [
        migrations.RunPython(set_default_company),
        migrations.AlterField(
            model_name='customuser',
            name='company',
            field=models.ForeignKey(to='core.Company', on_delete=models.CASCADE, null=False),
        ),
        migrations.AlterField(
            model_name='department',
            name='company',
            field=models.ForeignKey(to='core.Company', on_delete=models.CASCADE, null=False),
        ),
        migrations.AlterField(
            model_name='budget',
            name='company',
            field=models.ForeignKey(to='core.Company', on_delete=models.CASCADE, null=False),
        ),
    ]
