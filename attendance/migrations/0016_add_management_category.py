from django.db import migrations


def add_management_category(apps, schema_editor):
    Organization = apps.get_model('attendance', 'Organization')
    Category = apps.get_model('attendance', 'Category')

    for organization in Organization.objects.all():
        Category.objects.get_or_create(
            organization=organization,
            code='MANAGEMENT',
            defaults={
                'name': 'Management',
                'icon': 'bi-diagram-3',
                'color': 'secondary',
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0015_payrollrun_payslip'),
    ]

    operations = [
        migrations.RunPython(add_management_category, migrations.RunPython.noop),
    ]
