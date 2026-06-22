# attendance/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from .models import (
    Category,
    Department,
    Employee,
    AttendanceRecord,
    AttendanceSettings,
    EmployeeEducation,
    EmployeeCertification,
    EmployeeWorkExperience,
    EmployeeDocument,
    OnboardingStage,
    OnboardingParticipant,
    OnboardingTask,
    Applicant,
    OnboardingInvitation,
    AdminReport,
    AttendanceException,
    AttendanceExceptionType,
    AuditLog,
    LeaveType,
    LeaveRequest,
    Organization,
    OrganizationMembership,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'slug', 'email']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'organization']
    search_fields = ['user__username', 'user__email', 'organization__name']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'organization', 'actor', 'area', 'action', 'target_model', 'target_id']
    list_filter = ['organization', 'area', 'action', 'created_at']
    search_fields = ['summary', 'actor__username', 'target_model', 'target_id']
    readonly_fields = ['organization', 'actor', 'area', 'action', 'target_model', 'target_id', 'summary', 'metadata', 'created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(OnboardingTask)
class OnboardingTaskAdmin(admin.ModelAdmin):
    list_display = ['employee', 'stage', 'title', 'category', 'status', 'assigned_to', 'due_date', 'completed_at']
    list_filter = ['organization', 'stage', 'category', 'status', 'due_date']
    search_fields = ['title', 'employee__first_name', 'employee__last_name', 'employee__employee_id', 'notes']
    autocomplete_fields = ['employee', 'stage', 'assigned_to', 'completed_by']


@admin.register(OnboardingStage)
class OnboardingStageAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'code', 'order', 'color', 'is_active']
    list_filter = ['organization', 'is_active']
    search_fields = ['title', 'code', 'description', 'organization__name']
    list_editable = ['order', 'color', 'is_active']


@admin.register(OnboardingParticipant)
class OnboardingParticipantAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'organization', 'participant_type', 'stage', 'status', 'joining_date', 'moved_at']
    list_filter = ['organization', 'participant_type', 'stage', 'status']
    search_fields = [
        'applicant__first_name',
        'applicant__last_name',
        'applicant__email',
        'employee__first_name',
        'employee__last_name',
        'employee__email',
        'employee__employee_id',
    ]
    autocomplete_fields = ['organization', 'stage', 'applicant', 'employee', 'invitation']


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'organization', 'category', 'department', 'position', 'status', 'created_at']
    list_filter = ['organization', 'status', 'category', 'department']
    search_fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone', 'position']
    autocomplete_fields = ['organization', 'category', 'department', 'employee', 'invited_by', 'reviewed_by']


@admin.register(OnboardingInvitation)
class OnboardingInvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'organization', 'invitation_type', 'status', 'sent_at', 'expires_at']
    list_filter = ['organization', 'invitation_type', 'status', 'sent_at']
    search_fields = ['email', 'token', 'applicant__first_name', 'applicant__last_name', 'employee__first_name', 'employee__last_name']
    readonly_fields = ['token', 'sent_at', 'opened_at', 'submitted_at', 'created_at', 'updated_at']
    autocomplete_fields = ['organization', 'applicant', 'employee', 'invited_by']


@admin.register(AdminReport)
class AdminReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'report_type', 'tone', 'status', 'related_employee', 'event_date', 'created_by']
    list_filter = ['organization', 'report_type', 'tone', 'status', 'event_date']
    search_fields = ['title', 'body', 'action_taken', 'related_employee__first_name', 'related_employee__last_name']
    autocomplete_fields = ['organization', 'related_employee', 'related_department', 'created_by', 'reviewed_by']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'organization', 'icon', 'color', 'created_at']
    list_filter = ['organization']
    search_fields = ['name', 'code', 'organization__name']
    list_editable = ['icon', 'color']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'organization', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'organization__name']
    list_filter = ['organization', 'is_active']
    list_editable = ['is_active']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'display_name', 'category_badge', 'email', 
                    'department', 'organization', 'employment_status', 'attendance_status']
    list_filter = ['organization', 'category', 'department', 'employment_status', 'is_active', 'gender']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id']
    list_editable = ['employment_status']
    readonly_fields = ['employee_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Identification', {
            'fields': ('organization', 'user', 'employee_id', 'category')
        }),
        ('Personal Information', {
            'fields': ('profile_photo', 'title', 'first_name', 'middle_name', 'last_name', 'email', 'personal_email', 
                      'phone', 'gender', 'date_of_birth')
        }),
        ('Medical Information', {
            'fields': (
                'blood_group',
                'genotype',
                'allergies_or_medical_conditions',
                'emergency_medical_contact_name',
                'emergency_medical_contact_relationship',
                'emergency_medical_contact_phone',
            ),
            'classes': ('collapse',)
        }),
        ('Work Information', {
            'fields': ('department', 'position', 'hire_date', 'end_date', 'supervisor')
        }),
        ('Intern/Student Information', {
            'fields': (
                'institution',
                'faculty',
                'academic_department',
                'field_of_study',
                'student_id',
                'current_level',
                'expected_graduation_date',
                'academic_supervisor_name',
                'academic_supervisor_phone',
                'academic_supervisor_email',
                'internship_type',
                'internship_type_other',
                'area_of_interest',
                'area_of_interest_other',
                'preferred_department',
                'skill_html_css',
                'skill_javascript',
                'skill_python',
                'skill_java',
                'skill_c_cpp',
                'skill_django',
                'skill_react',
                'skill_nodejs',
                'skill_ui_ux',
                'skill_networking',
                'skill_cybersecurity',
                'other_technical_skill',
                'skill_other',
                'relevant_skills_projects',
            ),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('employment_status', 'is_active')
        }),
        ('Payroll', {
            'fields': (
                'bank_name',
                'bank_account_name',
                'bank_account_number',
                'bank_branch',
                'pension_rsa_pin',
                'pension_fund_administrator',
                'basic_salary',
                'housing_allowance',
                'transport_allowance',
                'other_allowances',
                'tax_deduction',
                'pension_deduction',
                'other_deductions',
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def display_name(self, obj):
        return obj.display_name
    display_name.short_description = 'Name'
    display_name.admin_order_field = 'first_name'
    
    def category_badge(self, obj):
        if obj.category:
            return format_html(
                '<span class="badge bg-{}">{}</span>',
                obj.category.color,
                obj.category.name
            )
        return '-'
    category_badge.short_description = 'Category'
    
    def attendance_status(self, obj):
        if obj.is_checked_in_today:
            record = obj.today_attendance
            late = " (Late)" if record and record.is_late else ""
            return format_html(
                '<span style="color: #10b981;">In{}</span>',
                late
            )
        return format_html('<span style="color: #6b7280;">Out</span>')
    attendance_status.short_description = 'Today'


@admin.register(EmployeeEducation)
class EmployeeEducationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'qualification_obtained', 'institution', 'year_of_graduation']
    list_filter = ['year_of_graduation']
    search_fields = ['employee__first_name', 'employee__last_name', 'qualification_obtained', 'institution']


@admin.register(EmployeeCertification)
class EmployeeCertificationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'certification_name', 'issuing_body', 'date_obtained', 'expiry_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'certification_name', 'issuing_body']


@admin.register(EmployeeWorkExperience)
class EmployeeWorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'employer_name', 'job_title', 'start_date', 'end_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employer_name', 'job_title']


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'document_type', 'title', 'issue_date', 'expiry_date', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id', 'title', 'notes']


@admin.register(AttendanceExceptionType)
class AttendanceExceptionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'organization', 'color', 'is_active', 'created_at']
    list_filter = ['organization', 'is_active']
    search_fields = ['name', 'code', 'description', 'organization__name']
    prepopulated_fields = {'code': ('name',)}


@admin.register(AttendanceException)
class AttendanceExceptionAdmin(admin.ModelAdmin):
    list_display = ['employee', 'organization', 'exception_type_display', 'start_date', 'end_date', 'day_span']
    list_filter = ['organization', 'exception_type', 'start_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id', 'notes']

    def exception_type_display(self, obj):
        return obj.get_exception_type_display()
    exception_type_display.short_description = 'Exception Type'

    def day_span(self, obj):
        return obj.day_count
    day_span.short_description = 'Days'


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'organization', 'annual_entitlement_days', 'is_paid', 'requires_attachment', 'is_active']
    list_filter = ['organization', 'is_paid', 'requires_attachment', 'is_active']
    search_fields = ['name', 'code', 'organization__name']
    prepopulated_fields = {'code': ('name',)}


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'organization', 'leave_type', 'start_date', 'end_date', 'day_count', 'status', 'reviewed_by']
    list_filter = ['organization', 'leave_type', 'status', 'start_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id', 'reason', 'review_note']
    readonly_fields = ['created_at', 'updated_at', 'reviewed_at']


class DateListFilter(admin.SimpleListFilter):
    """Custom filter for filtering by date"""
    title = 'Date'
    parameter_name = 'attendance_date'
    
    def lookups(self, request, model_admin):
        # Get unique dates from the last 30 days
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        dates = AttendanceRecord.objects.filter(
            check_in_time__date__gte=thirty_days_ago
        ).dates('check_in_time', 'day', order='DESC')
        
        return [(d.strftime('%Y-%m-%d'), d.strftime('%Y-%m-%d')) for d in dates[:30]]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(check_in_time__date=self.value())
        return queryset


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['employee', 'organization', 'employee_category', 'date_display', 
                    'check_in_display', 'check_out_display', 'hours_display', 'status_badge']
    list_filter = ['organization', 'employee__category', DateListFilter]  # Fixed: using custom filter
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__email']
    date_hierarchy = 'check_in_time'  # This gives clickable date drill-down
    
    def employee_category(self, obj):
        if obj.employee.category:
            return format_html(
                '<span class="badge bg-{}">{}</span>',
                obj.employee.category.color,
                obj.employee.category.code
            )
        return '-'
    employee_category.short_description = 'Cat'
    
    def date_display(self, obj):
        return obj.check_in_time.strftime('%Y-%m-%d')
    date_display.short_description = 'Date'
    date_display.admin_order_field = 'check_in_time'
    
    def check_in_display(self, obj):
        time_str = obj.check_in_time.strftime('%H:%M')
        if obj.is_late:
            return format_html('<span style="color: #f59e0b;">{} (Late)</span>', time_str)
        return time_str
    check_in_display.short_description = 'Check In'
    
    def check_out_display(self, obj):
        if obj.check_out_time:
            return obj.check_out_time.strftime('%H:%M')
        return '-'
    check_out_display.short_description = 'Check Out'
    
    def hours_display(self, obj):
        if obj.hours_worked:
            return f"{obj.hours_worked} hrs"
        return '-'
    hours_display.short_description = 'Hours'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: #10b981;">Active</span>')
        return format_html('<span style="color: #3b82f6;">Completed</span>')
    status_badge.short_description = 'Status'


@admin.register(AttendanceSettings)
class AttendanceSettingsAdmin(admin.ModelAdmin):
    list_display = ['organization', 'workday_start', 'late_threshold', 'birthday_reminder_days', 'internship_reminder_days', 'updated_at']

    def has_delete_permission(self, request, obj=None):
        return False
