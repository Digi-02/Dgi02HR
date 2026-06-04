from django.contrib.auth.models import User
from django.test import TestCase

from .models import Organization, OrganizationMembership
from .organization import (
    user_has_hr_access,
    user_has_manager_access,
    user_has_payroll_access,
    user_has_viewer_access,
)


class RolePermissionTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name='Digi02 Test',
            slug='digi02-test',
        )

    def make_user_with_role(self, role):
        user = User.objects.create_user(username=f'{role}_user', password='pass12345')
        OrganizationMembership.objects.create(
            user=user,
            organization=self.organization,
            role=role,
            is_active=True,
        )
        return user

    def test_hr_roles_have_hr_access(self):
        for role in ['owner', 'hr_admin']:
            with self.subTest(role=role):
                self.assertTrue(user_has_hr_access(self.make_user_with_role(role)))

    def test_payroll_officer_has_payroll_but_not_hr_access(self):
        user = self.make_user_with_role('payroll_officer')

        self.assertTrue(user_has_payroll_access(user))
        self.assertFalse(user_has_hr_access(user))

    def test_viewer_can_view_but_not_manage_hr_or_payroll(self):
        user = self.make_user_with_role('viewer')

        self.assertTrue(user_has_viewer_access(user))
        self.assertFalse(user_has_hr_access(user))
        self.assertFalse(user_has_payroll_access(user))

    def test_employee_has_no_management_access(self):
        user = self.make_user_with_role('employee')

        self.assertFalse(user_has_hr_access(user))
        self.assertFalse(user_has_payroll_access(user))
        self.assertFalse(user_has_viewer_access(user))
        self.assertFalse(user_has_manager_access(user))
