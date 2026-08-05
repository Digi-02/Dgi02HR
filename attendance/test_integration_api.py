from datetime import datetime, time

from django.test import TestCase, override_settings
from django.urls import reverse

from django.utils import timezone

from .models import AttendanceRecord, Category, Department, Employee, Organization


@override_settings(
    TECHNICAL_COMMAND_API_KEY="test-service-key",
    TECHNICAL_COMMAND_ORGANIZATION_SLUG="digi02",
    TECHNICAL_COMMAND_API_DEFAULT_PAGE_SIZE=2,
    TECHNICAL_COMMAND_API_MAX_PAGE_SIZE=10,
)
class TechnicalCommandPeopleAPITests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Digi02", slug="digi02")
        self.other_org = Organization.objects.create(name="Other", slug="other")
        self.category = Category.objects.create(organization=self.organization, name="Staff", code="STAFF", icon="person", color="primary")
        self.other_category = Category.objects.create(organization=self.other_org, name="Staff", code="STAFF", icon="person", color="primary")
        self.department = Department.objects.create(organization=self.organization, name="Engineering", code="ENG")
        self.manager = self.employee("EMP-001", "Grace", "Lead", position="Lead")
        self.person = self.employee("EMP-002", "Ada", "Samuel", line_manager=self.manager, skill_python="advanced")
        self.employee("EMP-003", "Inactive", "Person", is_active=False)
        self.employee("EMP-004", "Former", "Person", employment_status="completed")
        Employee.objects.create(organization=self.other_org, category=self.other_category, employee_id="OTHER-1", first_name="Other", last_name="Person", email="other@example.com", phone="0", gender="MALE")
        self.url = reverse("technical_command_people_api")
        self.auth = {"HTTP_AUTHORIZATION": "Api-Key test-service-key"}

    def employee(self, employee_id, first_name, last_name, **extra):
        defaults = dict(organization=self.organization, category=self.category, department=self.department, email=f"{employee_id.lower()}@example.com", phone="0800", gender="FEMALE", position="Engineer")
        defaults.update(extra)
        return Employee.objects.create(employee_id=employee_id, first_name=first_name, last_name=last_name, **defaults)

    def test_authentication_is_required_and_validated(self):
        self.assertEqual(self.client.get(self.url).status_code, 401)
        self.assertEqual(self.client.get(self.url, HTTP_AUTHORIZATION="Api-Key wrong").status_code, 403)

    def test_returns_only_active_configured_organization_people(self):
        response = self.client.get(self.url, **self.auth)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["api_version"], "v1")
        self.assertEqual(body["summary"]["total_active_people"], 2)
        self.assertEqual({item["employee_id"] for item in body["results"]}, {"EMP-001", "EMP-002"})

    def test_contract_contains_safe_fields_and_skills(self):
        response = self.client.get(self.url, {"search": "Ada"}, **self.auth)
        person = response.json()["results"][0]
        self.assertEqual(person["technical_skills"]["python"], "advanced")
        self.assertEqual(person["line_manager"]["employee_id"], "EMP-001")
        forbidden = {"phone", "date_of_birth", "bank_account_number", "basic_salary", "nin_number", "personal_email"}
        self.assertFalse(forbidden.intersection(person))

    def test_filter_order_pagination_and_invalid_queries(self):
        filtered = self.client.get(self.url, {"department": "ENG", "ordering": "-name", "page_size": 1}, **self.auth)
        self.assertEqual(filtered.status_code, 200)
        self.assertEqual(filtered.json()["pagination"]["total_results"], 2)
        self.assertIsNotNone(filtered.json()["pagination"]["next"])
        self.assertEqual(self.client.get(self.url, {"page_size": 11}, **self.auth).status_code, 400)
        self.assertEqual(self.client.get(self.url, {"ordering": "salary"}, **self.auth).status_code, 400)

    @override_settings(TECHNICAL_COMMAND_ORGANIZATION_SLUG="missing")
    def test_missing_configured_organization_fails_closed(self):
        self.assertEqual(self.client.get(self.url, **self.auth).status_code, 503)

    def test_todays_attendance_returns_statuses_and_summary(self):
        today = timezone.localdate()
        check_in_early = timezone.make_aware(datetime.combine(today, time(7, 30)))
        check_in_late = timezone.make_aware(datetime.combine(today, time(9, 0)))
        check_out = timezone.make_aware(datetime.combine(today, time(16, 0)))
        AttendanceRecord.objects.create(
            organization=self.organization, employee=self.manager,
            check_in_time=check_in_early,
        )
        AttendanceRecord.objects.create(
            organization=self.organization, employee=self.person,
            check_in_time=check_in_late, check_out_time=check_out,
        )
        response = self.client.get(reverse("technical_command_attendance_today_api"), **self.auth)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["summary"]["checked_in"], 1)
        self.assertEqual(body["summary"]["checked_out"], 1)
        self.assertEqual(body["summary"]["late"], 1)
        statuses = {item["employee_id"]: item["status"] for item in body["results"]}
        self.assertEqual(statuses["EMP-001"], "checked_in")
        self.assertEqual(statuses["EMP-002"], "checked_out")
        self.assertNotIn("OTHER-1", statuses)
