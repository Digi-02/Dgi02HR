# core/urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from attendance import views

urlpatterns = [
    # Admin (only for superusers)
    path('admin/', admin.site.urls),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Public kiosk
    path('', views.kiosk_view, name='kiosk'),
    path('o/<slug:org_slug>/kiosk/', views.kiosk_view, name='organization_kiosk'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/category/<str:code>/', views.category_dashboard, name='category_dashboard'),
    
    # Organizations
    path('organizations/', views.organization_list, name='organization_list'),
    path('organizations/add/', views.organization_create, name='organization_create'),
    path('organizations/<int:pk>/edit/', views.organization_edit, name='organization_edit'),
    path('organizations/<int:pk>/switch/', views.organization_switch, name='organization_switch'),
    path('settings/', views.organization_settings, name='organization_settings'),
    path('settings/departments/', views.organization_departments, name='organization_departments'),
    path('settings/categories/', views.organization_categories, name='organization_categories'),
    path('settings/attendance/', views.organization_attendance_settings, name='organization_attendance_settings'),
    path('settings/leave-types/', views.organization_leave_types, name='organization_leave_types'),
    
    # Employee Management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/account/', views.employee_account_create, name='employee_account_create'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    # Employee Self-Service
    path('me/', views.employee_self_service_dashboard, name='employee_self_service_dashboard'),
    path('me/leave/request/', views.employee_leave_request_create, name='employee_leave_request_create'),
    path('manager/leave/', views.manager_leave_requests, name='manager_leave_requests'),
    path('manager/leave/<int:pk>/approve/', views.manager_leave_request_approve, name='manager_leave_request_approve'),
    path('manager/leave/<int:pk>/reject/', views.manager_leave_request_reject, name='manager_leave_request_reject'),
    
    # Attendance Management
    path('attendance/', views.attendance_reports, name='attendance_reports'),
    path('attendance/add/', views.manual_attendance_add, name='manual_attendance_add'),
    path('attendance/exception-types/', views.attendance_exception_types, name='attendance_exception_types'),

    # Leave Management
    path('leave/', views.leave_requests, name='leave_requests'),
    path('leave/add/', views.leave_request_create, name='leave_request_create'),
    path('leave/<int:pk>/approve/', views.leave_request_approve, name='leave_request_approve'),
    path('leave/<int:pk>/reject/', views.leave_request_reject, name='leave_request_reject'),

    # Payroll
    path('payroll/', views.payroll_runs, name='payroll_runs'),
    path('payroll/add/', views.payroll_run_create, name='payroll_run_create'),
    path('payroll/<int:pk>/', views.payroll_run_detail, name='payroll_run_detail'),
    path('payroll/<int:pk>/generate/', views.payroll_run_generate, name='payroll_run_generate'),
    path('payroll/<int:pk>/approve/', views.payroll_run_approve, name='payroll_run_approve'),
    path('payroll/<int:pk>/mark-paid/', views.payroll_run_mark_paid, name='payroll_run_mark_paid'),
    path('payslips/<int:pk>/', views.payslip_detail, name='payslip_detail'),
    
    # Reports
    path('reports/', views.reports_view, name='reports'),
    path('reports/export/', views.export_attendance_csv, name='export_attendance_csv'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
