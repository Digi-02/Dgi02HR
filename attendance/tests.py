from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import (
    Applicant,
    AdminReport,
    AttendanceException,
    AttendanceRecord,
    Category,
    Department,
    Employee,
    LeaveRequest,
    LeaveType,
    OnboardingInvitation,
    OnboardingParticipant,
    OnboardingStage,
    Organization,
    OrganizationMembership,
)
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


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class OnboardingInvitationTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name='Digi02 Test',
            slug='digi02-test-onboarding',
        )
        self.category = Category.objects.create(
            organization=self.organization,
            name='Staff',
            code='STAFF',
            icon='bi-person',
            color='primary',
        )
        self.department = Department.objects.create(
            organization=self.organization,
            name='Engineering',
            code='ENG',
        )
        self.hr_user = User.objects.create_user(username='hr', password='pass12345')
        OrganizationMembership.objects.create(
            user=self.hr_user,
            organization=self.organization,
            role='hr_admin',
            is_active=True,
        )

    def test_hr_can_invite_applicant_and_public_link_accepts_submission(self):
        self.client.login(username='hr', password='pass12345')

        response = self.client.post(reverse('applicant_invite'), {
            'first_name': 'Ada',
            'middle_name': '',
            'last_name': 'Okafor',
            'email': 'ada@example.com',
            'phone': '08010000000',
            'gender': 'FEMALE',
            'category': self.category.pk,
            'department': self.department.pk,
            'position': 'Software Intern',
            'cover_note': 'Please complete your application.',
        })

        self.assertRedirects(response, reverse('onboarding_tasks'))
        applicant = Applicant.objects.get(email='ada@example.com')
        invitation = OnboardingInvitation.objects.get(applicant=applicant)
        self.assertEqual(invitation.status, 'sent')
        self.assertEqual(len(mail.outbox), 1)
        participant = OnboardingParticipant.objects.get(applicant=applicant)
        self.assertEqual(participant.stage.code, 'invitation_sent')

        response = self.client.post(reverse('public_onboarding_invitation', kwargs={'token': invitation.token}), {
            'first_name': 'Ada',
            'middle_name': '',
            'last_name': 'Okafor',
            'phone': '08010000001',
            'gender': 'FEMALE',
            'department': self.department.pk,
            'position': 'Software Intern',
            'cover_note': 'I am ready to join.',
        })

        self.assertEqual(response.status_code, 200)
        applicant.refresh_from_db()
        invitation.refresh_from_db()
        self.assertEqual(applicant.status, 'submitted')
        self.assertEqual(invitation.status, 'submitted')
        participant.refresh_from_db()
        self.assertEqual(participant.stage.code, 'application_submitted')

    def test_hr_can_convert_submitted_applicant_to_employee_and_send_setup_invite(self):
        self.client.login(username='hr', password='pass12345')
        applicant = Applicant.objects.create(
            organization=self.organization,
            first_name='Ada',
            last_name='Okafor',
            email='ada2@example.com',
            phone='08010000002',
            gender='FEMALE',
            category=self.category,
            department=self.department,
            position='Developer',
            status='submitted',
        )

        response = self.client.post(reverse('applicant_approve', kwargs={'pk': applicant.pk}))

        self.assertRedirects(response, reverse('onboarding_tasks'))
        applicant.refresh_from_db()
        self.assertEqual(applicant.status, 'converted')
        self.assertIsNotNone(applicant.employee)
        self.assertTrue(Employee.objects.filter(email='ada2@example.com').exists())
        self.assertTrue(
            OnboardingInvitation.objects.filter(
                employee=applicant.employee,
                invitation_type='employee_setup',
                status='sent',
            ).exists()
        )
        participant = OnboardingParticipant.objects.get(applicant=applicant)
        self.assertEqual(participant.employee, applicant.employee)
        self.assertEqual(participant.stage.code, 'profile_setup')

    def test_existing_employee_setup_invitation_creates_self_service_user(self):
        employee = Employee.objects.create(
            organization=self.organization,
            category=self.category,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='08020000000',
            gender='MALE',
            department=self.department,
            position='Analyst',
        )
        invitation = OnboardingInvitation.objects.create(
            organization=self.organization,
            invitation_type='employee_setup',
            employee=employee,
            email=employee.email,
            status='sent',
            invited_by=self.hr_user,
        )

        response = self.client.post(reverse('public_onboarding_invitation', kwargs={'token': invitation.token}), {
            'username': 'john_doe',
            'password': 'securepass123',
            'personal_email': 'john.personal@example.com',
            'phone': '08020000001',
            'residential_address': '12 Lagos Street',
            'emergency_contact_name': 'Jane Doe',
            'emergency_contact_phone': '08030000000',
        })

        self.assertRedirects(response, reverse('employee_self_service_dashboard'))
        employee.refresh_from_db()
        invitation.refresh_from_db()
        self.assertIsNotNone(employee.user)
        self.assertEqual(employee.user.username, 'john_doe')
        self.assertEqual(invitation.status, 'accepted')
        self.assertTrue(
            OrganizationMembership.objects.filter(
                user=employee.user,
                organization=self.organization,
                role='employee',
            ).exists()
        )
        participant = OnboardingParticipant.objects.get(employee=employee)
        self.assertEqual(participant.stage.code, 'pre_arrival')

    def test_hr_can_create_stage_and_move_onboarding_participant(self):
        self.client.login(username='hr', password='pass12345')

        response = self.client.post(reverse('onboarding_stage_create'), {
            'title': 'Medical Check',
            'description': 'Internal medical clearance stage.',
            'order': 55,
            'color': 'info',
            'is_active': 'on',
        })

        self.assertRedirects(response, reverse('onboarding_tasks'))
        custom_stage = OnboardingStage.objects.get(organization=self.organization, title='Medical Check')
        invitation_stage = OnboardingStage.objects.get(organization=self.organization, code='invitation_sent')
        applicant = Applicant.objects.create(
            organization=self.organization,
            first_name='Move',
            last_name='Candidate',
            email='move.candidate@example.com',
            phone='08031000000',
            gender='FEMALE',
            category=self.category,
            department=self.department,
            position='Designer',
            status='invited',
        )
        participant = OnboardingParticipant.objects.create(
            organization=self.organization,
            applicant=applicant,
            stage=invitation_stage,
            participant_type='applicant',
        )

        response = self.client.post(
            reverse('onboarding_participant_move', kwargs={'pk': participant.pk}),
            {'stage': custom_stage.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['ok'])
        self.assertEqual(response.json()['stage_id'], custom_stage.pk)
        participant.refresh_from_db()
        self.assertEqual(participant.stage, custom_stage)

    def test_hr_can_delete_empty_onboarding_stage(self):
        self.client.login(username='hr', password='pass12345')
        stage = OnboardingStage.objects.create(
            organization=self.organization,
            title='Temporary Stage',
            order=95,
            color='secondary',
        )

        response = self.client.post(reverse('onboarding_stage_delete', kwargs={'pk': stage.pk}))

        self.assertRedirects(response, reverse('onboarding_tasks'))
        self.assertFalse(OnboardingStage.objects.filter(pk=stage.pk).exists())

    def test_stage_with_participants_is_not_deleted(self):
        self.client.login(username='hr', password='pass12345')
        stage = OnboardingStage.objects.create(
            organization=self.organization,
            title='Protected Stage',
            order=96,
            color='warning',
        )
        applicant = Applicant.objects.create(
            organization=self.organization,
            first_name='Protected',
            last_name='Candidate',
            email='protected.candidate@example.com',
            phone='08032000000',
            gender='MALE',
            category=self.category,
            department=self.department,
            position='Developer',
            status='invited',
        )
        OnboardingParticipant.objects.create(
            organization=self.organization,
            applicant=applicant,
            stage=stage,
            participant_type='applicant',
        )

        response = self.client.post(reverse('onboarding_stage_delete', kwargs={'pk': stage.pk}))

        self.assertRedirects(response, reverse('onboarding_tasks'))
        self.assertTrue(OnboardingStage.objects.filter(pk=stage.pk).exists())

    def test_hr_can_create_admin_report(self):
        self.client.login(username='hr', password='pass12345')
        employee = Employee.objects.create(
            organization=self.organization,
            category=self.category,
            first_name='Report',
            last_name='Subject',
            email='report.subject@example.com',
            phone='08040000000',
            gender='MALE',
            department=self.department,
            position='Analyst',
        )

        response = self.client.post(reverse('admin_report_create'), {
            'title': 'Good client handover',
            'report_type': 'staff_feedback',
            'tone': 'positive',
            'event_date': '2026-06-21',
            'related_employee': employee.pk,
            'related_department': self.department.pk,
            'body': 'The employee handled the handover professionally.',
            'action_taken': 'Noted for performance review.',
            'status': 'open',
        })

        report = AdminReport.objects.get(title='Good client handover')
        self.assertRedirects(response, reverse('admin_report_detail', kwargs={'pk': report.pk}))
        self.assertEqual(report.organization, self.organization)
        self.assertEqual(report.created_by, self.hr_user)
        self.assertEqual(report.related_employee, employee)

    def test_hr_can_delete_admin_report(self):
        self.client.login(username='hr', password='pass12345')
        report = AdminReport.objects.create(
            organization=self.organization,
            title='Report to remove',
            report_type='general',
            tone='neutral',
            event_date='2026-06-21',
            body='This report should be deleted.',
            created_by=self.hr_user,
        )

        response = self.client.post(reverse('admin_report_delete', kwargs={'pk': report.pk}))

        self.assertRedirects(response, reverse('admin_reports'))
        self.assertFalse(AdminReport.objects.filter(pk=report.pk).exists())

    def test_attendance_reports_paginate_past_records(self):
        self.client.login(username='hr', password='pass12345')
        employee = Employee.objects.create(
            organization=self.organization,
            category=self.category,
            first_name='Attendance',
            last_name='Subject',
            email='attendance.subject@example.com',
            phone='08045000000',
            gender='MALE',
            department=self.department,
            position='Analyst',
        )
        for index in range(30):
            AttendanceRecord.objects.create(
                organization=self.organization,
                employee=employee,
                check_in_time=timezone.now() - timedelta(minutes=index),
            )
        for index in range(12):
            AttendanceRecord.objects.create(
                organization=self.organization,
                employee=employee,
                check_in_time=timezone.now() - timedelta(days=index + 1),
            )

        first_page = self.client.get(reverse('attendance_reports'))
        records_second_page = self.client.get(reverse('attendance_reports'), {'attendance_page': 2})
        days_second_page = self.client.get(reverse('attendance_reports'), {'days_page': 2})

        self.assertContains(first_page, 'Showing 1-25 of 30')
        self.assertContains(records_second_page, 'Showing 26-30 of 30')
        self.assertContains(days_second_page, 'Showing 11-13 of 13')

    def test_manual_attendance_employee_selector_is_searchable(self):
        self.client.login(username='hr', password='pass12345')
        employee = Employee.objects.create(
            organization=self.organization,
            category=self.category,
            first_name='Searchable',
            last_name='Person',
            email='searchable.person@example.com',
            phone='08046000000',
            gender='FEMALE',
            department=self.department,
            position='Operations Lead',
        )

        response = self.client.get(reverse('manual_attendance_add'))

        self.assertContains(response, 'data-searchable-select="true"')
        self.assertContains(response, 'Search employee name, ID, email, department')
        self.assertContains(response, employee.email)
        self.assertContains(response, self.department.name)

    def test_leave_overview_and_employee_leave_detail_render(self):
        self.client.login(username='hr', password='pass12345')
        employee = Employee.objects.create(
            organization=self.organization,
            category=self.category,
            first_name='Leave',
            last_name='Subject',
            email='leave.subject@example.com',
            phone='08050000000',
            gender='FEMALE',
            department=self.department,
            position='Designer',
        )
        leave_type = LeaveType.objects.create(
            organization=self.organization,
            name='Annual Leave',
            code='annual_leave',
            annual_entitlement_days=21,
            color='success',
            is_active=True,
        )
        LeaveRequest.objects.create(
            organization=self.organization,
            employee=employee,
            leave_type=leave_type,
            start_date='2026-06-22',
            end_date='2026-06-24',
            status='approved',
            manager_approval_status='not_required',
        )

        overview_response = self.client.get(reverse('leave_requests'))
        detail_response = self.client.get(reverse('employee_leave_detail', kwargs={'employee_pk': employee.pk}))

        self.assertEqual(overview_response.status_code, 200)
        self.assertContains(overview_response, 'Employee Leave Table')
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'Leave Profile')

    def test_hr_can_edit_leave_type(self):
        self.client.login(username='hr', password='pass12345')
        leave_type = LeaveType.objects.create(
            organization=self.organization,
            name='Study Leave',
            code='study_leave',
            annual_entitlement_days=5,
            color='warning',
            is_active=True,
        )

        response = self.client.post(reverse('organization_leave_type_edit', kwargs={'pk': leave_type.pk}), {
            'name': 'Updated Study Leave',
            'code': 'updated_study_leave',
            'annual_entitlement_days': 7,
            'color': 'info',
            'requires_attachment': 'on',
            'is_paid': 'on',
            'is_active': 'on',
        })

        self.assertRedirects(response, reverse('organization_leave_types'))
        leave_type.refresh_from_db()
        self.assertEqual(leave_type.name, 'Updated Study Leave')
        self.assertEqual(leave_type.annual_entitlement_days, 7)
        self.assertTrue(leave_type.requires_attachment)

    def test_hr_can_delete_unused_leave_type(self):
        self.client.login(username='hr', password='pass12345')
        leave_type = LeaveType.objects.create(
            organization=self.organization,
            name='Temporary Leave',
            code='temporary_leave',
            annual_entitlement_days=1,
            color='secondary',
            is_active=True,
        )

        response = self.client.post(reverse('organization_leave_type_delete', kwargs={'pk': leave_type.pk}))

        self.assertRedirects(response, reverse('organization_leave_types'))
        self.assertFalse(LeaveType.objects.filter(pk=leave_type.pk).exists())

    def test_used_leave_type_is_not_deleted(self):
        self.client.login(username='hr', password='pass12345')
        employee = Employee.objects.create(
            organization=self.organization,
            category=self.category,
            first_name='Protected',
            last_name='Leave',
            email='protected.leave@example.com',
            phone='08060000000',
            gender='MALE',
            department=self.department,
        )
        leave_type = LeaveType.objects.create(
            organization=self.organization,
            name='Protected Leave',
            code='protected_leave',
            annual_entitlement_days=2,
            color='primary',
            is_active=True,
        )
        LeaveRequest.objects.create(
            organization=self.organization,
            employee=employee,
            leave_type=leave_type,
            start_date='2026-06-25',
            end_date='2026-06-25',
            status='pending',
            manager_approval_status='not_required',
        )

        response = self.client.post(reverse('organization_leave_type_delete', kwargs={'pk': leave_type.pk}))

        self.assertRedirects(response, reverse('organization_leave_types'))
        self.assertTrue(LeaveType.objects.filter(pk=leave_type.pk).exists())

    def test_hr_can_view_and_edit_pending_leave_request(self):
        self.client.login(username='hr', password='pass12345')
        employee = Employee.objects.create(
            organization=self.organization,
            category=self.category,
            first_name='Editable',
            last_name='Leave',
            email='editable.leave@example.com',
            phone='08070000000',
            gender='FEMALE',
            department=self.department,
            position='Analyst',
        )
        leave_type = LeaveType.objects.create(
            organization=self.organization,
            name='Annual Leave',
            code='annual_leave',
            annual_entitlement_days=21,
            color='success',
            is_active=True,
        )
        leave_request = LeaveRequest.objects.create(
            organization=self.organization,
            employee=employee,
            leave_type=leave_type,
            start_date='2026-07-01',
            end_date='2026-07-02',
            status='pending',
            manager_approval_status='not_required',
        )

        detail_response = self.client.get(reverse('leave_request_detail', kwargs={'pk': leave_request.pk}))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'Editable Leave')

        response = self.client.post(reverse('leave_request_edit', kwargs={'pk': leave_request.pk}), {
            'employee': employee.pk,
            'leave_type': leave_type.pk,
            'start_date': '2026-07-03',
            'end_date': '2026-07-05',
            'day_part': 'full_day',
            'reason': 'Updated handover plan.',
        })

        self.assertRedirects(response, reverse('leave_request_detail', kwargs={'pk': leave_request.pk}))
        leave_request.refresh_from_db()
        self.assertEqual(str(leave_request.start_date), '2026-07-03')
        self.assertEqual(str(leave_request.end_date), '2026-07-05')
        self.assertEqual(leave_request.reason, 'Updated handover plan.')

    def test_hr_can_cancel_approved_leave_request_and_remove_synced_attendance_exception(self):
        self.client.login(username='hr', password='pass12345')
        employee = Employee.objects.create(
            organization=self.organization,
            category=self.category,
            first_name='Cancel',
            last_name='Leave',
            email='cancel.leave@example.com',
            phone='08080000000',
            gender='MALE',
            department=self.department,
            position='Engineer',
        )
        leave_type = LeaveType.objects.create(
            organization=self.organization,
            name='Annual Leave',
            code='annual_leave',
            annual_entitlement_days=21,
            color='success',
            is_active=True,
        )
        leave_request = LeaveRequest.objects.create(
            organization=self.organization,
            employee=employee,
            leave_type=leave_type,
            start_date='2026-07-06',
            end_date='2026-07-07',
            status='approved',
            manager_approval_status='not_required',
        )
        attendance_exception = AttendanceException.objects.create(
            organization=self.organization,
            employee=employee,
            exception_type='leave',
            start_date='2026-07-06',
            end_date='2026-07-07',
            notes='Annual Leave approved via leave management.',
        )

        response = self.client.post(reverse('leave_request_cancel', kwargs={'pk': leave_request.pk}), {
            'review_note': 'Plans changed.',
        })

        self.assertRedirects(response, reverse('leave_request_detail', kwargs={'pk': leave_request.pk}))
        leave_request.refresh_from_db()
        self.assertEqual(leave_request.status, 'cancelled')
        self.assertEqual(leave_request.review_note, 'Plans changed.')
        self.assertFalse(AttendanceException.objects.filter(pk=attendance_exception.pk).exists())

    def test_hr_can_delete_leave_request(self):
        self.client.login(username='hr', password='pass12345')
        employee = Employee.objects.create(
            organization=self.organization,
            category=self.category,
            first_name='Delete',
            last_name='Leave',
            email='delete.leave@example.com',
            phone='08090000000',
            gender='FEMALE',
            department=self.department,
            position='Coordinator',
        )
        leave_type = LeaveType.objects.create(
            organization=self.organization,
            name='Study Leave',
            code='study_leave',
            annual_entitlement_days=5,
            color='info',
            is_active=True,
        )
        leave_request = LeaveRequest.objects.create(
            organization=self.organization,
            employee=employee,
            leave_type=leave_type,
            start_date='2026-07-10',
            end_date='2026-07-10',
            status='pending',
            manager_approval_status='not_required',
        )

        response = self.client.post(reverse('leave_request_delete', kwargs={'pk': leave_request.pk}))

        self.assertRedirects(response, reverse('employee_leave_detail', kwargs={'employee_pk': employee.pk}))
        self.assertFalse(LeaveRequest.objects.filter(pk=leave_request.pk).exists())
