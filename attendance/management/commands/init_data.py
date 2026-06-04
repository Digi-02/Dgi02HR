# attendance/management/commands/init_data.py

from django.core.management.base import BaseCommand
from attendance.models import Category, Department
from attendance.organization import DEFAULT_CATEGORIES, get_default_organization


class Command(BaseCommand):
    help = 'Initialize default categories and departments'

    def handle(self, *args, **options):
        organization = get_default_organization()

        # Create Categories
        for cat_data in DEFAULT_CATEGORIES:
            category, created = Category.objects.get_or_create(
                organization=organization,
                code=cat_data['code'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")
            else:
                self.stdout.write(f"Category already exists: {category.name}")

        # Create Departments
        departments = [
            {'name': 'Accounting', 'code': 'ACCT'},
            {'name': 'Administration', 'code': 'ADMIN'},
            {'name': 'IT', 'code': 'TECH'},
        ]

        for dept_data in departments:
            department, created = Department.objects.get_or_create(
                organization=organization,
                code=dept_data['code'],
                defaults=dept_data
            )
            if created:
                self.stdout.write(f"Created department: {department.name}")
            else:
                self.stdout.write(f"Department already exists: {department.name}")

        self.stdout.write(self.style.SUCCESS('\nInitialization complete!'))
