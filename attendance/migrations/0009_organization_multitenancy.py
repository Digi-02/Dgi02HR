# Generated manually for organization scoping.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


DEFAULT_ORG_NAME = 'Digi02TechSystem'
DEFAULT_ORG_SLUG = 'digi02techsystem'


def attach_existing_data_to_default_org(apps, schema_editor):
    Organization = apps.get_model('attendance', 'Organization')
    OrganizationMembership = apps.get_model('attendance', 'OrganizationMembership')
    Category = apps.get_model('attendance', 'Category')
    Department = apps.get_model('attendance', 'Department')
    Employee = apps.get_model('attendance', 'Employee')
    AttendanceRecord = apps.get_model('attendance', 'AttendanceRecord')
    AttendanceExceptionType = apps.get_model('attendance', 'AttendanceExceptionType')
    AttendanceException = apps.get_model('attendance', 'AttendanceException')
    AttendanceSettings = apps.get_model('attendance', 'AttendanceSettings')
    User = apps.get_model('auth', 'User')

    organization, _ = Organization.objects.get_or_create(
        slug=DEFAULT_ORG_SLUG,
        defaults={'name': DEFAULT_ORG_NAME, 'is_active': True},
    )

    Category.objects.filter(organization__isnull=True).update(organization=organization)
    Department.objects.filter(organization__isnull=True).update(organization=organization)
    Employee.objects.filter(organization__isnull=True).update(organization=organization)
    AttendanceRecord.objects.filter(organization__isnull=True).update(organization=organization)
    AttendanceExceptionType.objects.filter(organization__isnull=True).update(organization=organization)
    AttendanceException.objects.filter(organization__isnull=True).update(organization=organization)

    settings_obj = AttendanceSettings.objects.filter(organization__isnull=True).first()
    if settings_obj:
        settings_obj.organization = organization
        settings_obj.save(update_fields=['organization'])
        AttendanceSettings.objects.filter(organization__isnull=True).delete()
    elif not AttendanceSettings.objects.filter(organization=organization).exists():
        AttendanceSettings.objects.create(organization=organization)

    for user in User.objects.filter(is_active=True):
        if user.is_staff or user.is_superuser:
            OrganizationMembership.objects.get_or_create(
                user=user,
                organization=organization,
                defaults={'role': 'owner' if user.is_superuser else 'hr_admin', 'is_active': True},
            )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0008_attendanceexceptiontype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(max_length=80, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('address', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OrganizationMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('owner', 'Owner'), ('hr_admin', 'HR Admin'), ('manager', 'Manager'), ('employee', 'Employee'), ('payroll_officer', 'Payroll Officer'), ('viewer', 'Viewer')], default='hr_admin', max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='attendance.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['organization__name', 'user__username'],
                'unique_together': {('user', 'organization')},
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='category',
            name='code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='department',
            name='code',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(help_text='Auto-generated ID', max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(help_text='Work/primary email used for kiosk check-in', max_length=254),
        ),
        migrations.AlterField(
            model_name='attendanceexceptiontype',
            name='code',
            field=models.SlugField(max_length=50),
        ),
        migrations.AlterField(
            model_name='attendanceexceptiontype',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='category',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='attendance.organization'),
        ),
        migrations.AddField(
            model_name='department',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='attendance.organization'),
        ),
        migrations.AddField(
            model_name='employee',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='attendance.organization'),
        ),
        migrations.AddField(
            model_name='attendanceexceptiontype',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_exception_types', to='attendance.organization'),
        ),
        migrations.AddField(
            model_name='attendanceexception',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_exceptions', to='attendance.organization'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='attendance.organization'),
        ),
        migrations.AddField(
            model_name='attendancesettings',
            name='organization',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_settings', to='attendance.organization'),
        ),
        migrations.RunPython(attach_existing_data_to_default_org, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='category',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='attendance.organization'),
        ),
        migrations.AlterField(
            model_name='department',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='attendance.organization'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='attendance.organization'),
        ),
        migrations.AlterField(
            model_name='attendanceexceptiontype',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_exception_types', to='attendance.organization'),
        ),
        migrations.AlterField(
            model_name='attendanceexception',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_exceptions', to='attendance.organization'),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='attendance.organization'),
        ),
        migrations.AlterField(
            model_name='attendancesettings',
            name='organization',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_settings', to='attendance.organization'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('organization', 'code'), ('organization', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='department',
            unique_together={('organization', 'code')},
        ),
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together={('organization', 'employee_id'), ('organization', 'email')},
        ),
        migrations.AlterUniqueTogether(
            name='attendanceexceptiontype',
            unique_together={('organization', 'code')},
        ),
    ]
