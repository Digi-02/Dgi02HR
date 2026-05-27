# attendance/models.py

from django.db import models
from django.utils import timezone
from datetime import date, time


class Category(models.Model):
    """User categories: Staff, Intern, Student"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    icon = models.CharField(max_length=50, help_text="Bootstrap icon name (e.g., bi-person-badge)")
    color = models.CharField(max_length=20, help_text="Bootstrap color class (e.g., primary, success, info)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Department(models.Model):
    """Organization departments"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Employee(models.Model):
    """Unified model for Staff, Interns, and Students"""
    
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    
    TITLE_CHOICES = [
        ('Mr.', 'Mr.'),
        ('Ms', 'Ms'),
        ('Mrs.', 'Mrs.'),
        ('Engr.', 'Engr.'),
        ('Dr.', 'Dr.'),
        ('Prof.', 'Prof.'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    GENOTYPE_CHOICES = [
        ('AA', 'AA'),
        ('AS', 'AS'),
        ('AC', 'AC'),
        ('SS', 'SS'),
        ('SC', 'SC'),
    ]
    
    EMPLOYMENT_STATUS = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
        ('completed', 'Completed'),  # For interns/students who finished
    ]
    
    # === Identification ===
    employee_id = models.CharField(max_length=20, unique=True, help_text="Auto-generated ID")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='employees')
    
    # === Personal Information ===
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, help_text="Work/primary email used for kiosk check-in")
    personal_email = models.EmailField(blank=True, null=True, help_text="Personal email (for interns/students)")
    phone = models.CharField(max_length=20)
    alternative_phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True, help_text="Required for Staff only")
    nationality = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    religion = models.CharField(max_length=100, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    genotype = models.CharField(max_length=5, choices=GENOTYPE_CHOICES, blank=True)

    residential_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    local_government = models.CharField(max_length=100, blank=True)

    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_relationship = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    next_of_kin_name = models.CharField(max_length=150, blank=True)
    next_of_kin_relationship = models.CharField(max_length=100, blank=True)
    next_of_kin_phone = models.CharField(max_length=20, blank=True)
    next_of_kin_email = models.EmailField(blank=True)
    next_of_kin_address = models.TextField(blank=True)
    
    # === Work Information ===
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=100, blank=True, help_text="Job title or role")
    line_manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='direct_reports',
        help_text="Line manager or reporting manager",
    )
    
    # === Dates ===
    hire_date = models.DateField(null=True, blank=True, help_text="Staff: Hire date. Intern/Student: Start date")
    end_date = models.DateField(null=True, blank=True, help_text="For interns/students: Expected end date")
    probation_end_date = models.DateField(null=True, blank=True)
    
    # === Intern/Student Specific ===
    institution = models.CharField(max_length=200, blank=True, help_text="University/School name")
    qualification_obtained = models.CharField(max_length=150, blank=True)
    field_of_study = models.CharField(max_length=100, blank=True, help_text="Course or program")
    year_of_graduation = models.PositiveIntegerField(null=True, blank=True)
    class_of_degree = models.CharField(max_length=100, blank=True)
    student_id = models.CharField(max_length=50, blank=True, help_text="School ID number")
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='supervisees', help_text="Supervising staff member")

    nin_number = models.CharField(max_length=20, blank=True)
    passport_number = models.CharField(max_length=30, blank=True)
    passport_expiry_date = models.DateField(null=True, blank=True)
    tin_number = models.CharField(max_length=30, blank=True)
    drivers_license_number = models.CharField(max_length=50, blank=True)
    work_permit_number = models.CharField(max_length=50, blank=True)
    work_permit_expiry_date = models.DateField(null=True, blank=True)
    
    # === Status ===
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS, default='active')
    is_active = models.BooleanField(default=True, help_text="Uncheck to disable kiosk access")
    
    # === Metadata ===
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'first_name', 'last_name']
    
    def __str__(self):
        return f"[{self.category.code}] {self.full_name}"
    
    def save(self, *args, **kwargs):
        # Auto-generate employee_id if not set
        if not self.employee_id:
            prefix = self.category.code if self.category else 'USR'
            year = timezone.now().year
            last_emp = Employee.objects.filter(
                employee_id__startswith=f"{prefix}-{year}"
            ).order_by('-employee_id').first()
            
            if last_emp:
                last_num = int(last_emp.employee_id.split('-')[-1])
                new_num = str(last_num + 1).zfill(3)
            else:
                new_num = '001'
            
            self.employee_id = f"{prefix}-{year}-{new_num}"
        
        # Auto-set title based on gender if not provided
        if not self.title:
            if self.gender == 'MALE':
                self.title = 'Mr.'
            elif self.gender == 'FEMALE':
                self.title = 'Ms'
        
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def display_name(self):
        """Returns formatted name with title"""
        if self.title:
            return f"{self.title} {self.full_name}"
        return self.full_name
    
    @property
    def is_staff(self):
        return self.category.code == 'STAFF' if self.category else False
    
    @property
    def is_intern(self):
        return self.category.code == 'INTERN' if self.category else False
    
    @property
    def is_student(self):
        return self.category.code == 'STUDENT' if self.category else False
    
    @property
    def is_checked_in_today(self):
        """Check if employee has an open attendance record today"""
        today = timezone.now().date()
        return self.attendance_records.filter(
            check_in_time__date=today,
            check_out_time__isnull=True
        ).exists()
    
    @property
    def today_attendance(self):
        """Get today's attendance record if it exists"""
        today = timezone.now().date()
        return self.attendance_records.filter(
            check_in_time__date=today
        ).first()
    
    @property
    def work_anniversary_today(self):
        """Check if today is work anniversary (Staff only)"""
        if not self.hire_date or self.category.code != 'STAFF':
            return False
        today = date.today()
        return self.hire_date.month == today.month and self.hire_date.day == today.day
    
    @property
    def years_of_service(self):
        """Calculate years of service (Staff only)"""
        if not self.hire_date:
            return None
        today = date.today()
        years = today.year - self.hire_date.year
        if today.month < self.hire_date.month or (
            today.month == self.hire_date.month and today.day < self.hire_date.day
        ):
            years -= 1
        return years
    
    def get_anniversary_this_week(self):
        """Check if work anniversary is in the next 7 days"""
        if not self.hire_date or self.category.code != 'STAFF':
            return None
        
        today = date.today()
        anniversary_this_year = date(today.year, self.hire_date.month, self.hire_date.day)
        
        days_until = (anniversary_this_year - today).days
        
        if 0 <= days_until <= 7:
            return {
                'date': anniversary_this_year,
                'days_until': days_until,
                'years': self.years_of_service
            }
        return None


class EmployeeEducation(models.Model):
    """Repeatable educational qualifications for an employee."""

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations')
    qualification_obtained = models.CharField(max_length=150)
    institution = models.CharField(max_length=200, blank=True)
    field_of_study = models.CharField(max_length=150, blank=True)
    year_of_graduation = models.PositiveIntegerField(null=True, blank=True)
    class_of_degree = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year_of_graduation', 'qualification_obtained', 'institution']

    def __str__(self):
        return f"{self.employee.full_name} - {self.qualification_obtained}"


class EmployeeCertification(models.Model):
    """Repeatable professional certifications for an employee."""

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=150)
    issuing_body = models.CharField(max_length=150, blank=True)
    date_obtained = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_obtained', 'certification_name']

    def __str__(self):
        return f"{self.employee.full_name} - {self.certification_name}"


class EmployeeWorkExperience(models.Model):
    """Repeatable pre-employment work history for an employee."""

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='work_experiences')
    employer_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=150, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    reason_for_leaving = models.TextField(blank=True)
    skills_and_competence = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-end_date', '-start_date', 'employer_name']

    def __str__(self):
        return f"{self.employee.full_name} - {self.employer_name}"


class AttendanceException(models.Model):
    """Day-based attendance exceptions like leave, sick days, and approved absences."""

    EXCEPTION_TYPE_CHOICES = [
        ('leave', 'Leave'),
        ('sick', 'Sick Day'),
        ('authorized_absence', 'Authorized Absence'),
        ('training', 'Training'),
        ('remote', 'Remote Work'),
        ('half_day', 'Half Day'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_exceptions')
    exception_type = models.CharField(max_length=30, choices=EXCEPTION_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date', '-end_date', 'employee__first_name']
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['employee', 'start_date']),
        ]

    def __str__(self):
        return f"{self.employee.full_name} - {self.get_exception_type_display()}"

    @property
    def day_count(self):
        return (self.end_date - self.start_date).days + 1


class AttendanceRecord(models.Model):
    """Check-in and check-out records for all users"""
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-check_in_time']
        indexes = [
            models.Index(fields=['check_in_time']),
            models.Index(fields=['employee', 'check_in_time']),
        ]
    
    def __str__(self):
        return f"{self.employee.display_name} - {self.check_in_time.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def hours_worked(self):
        """Calculate hours worked for this record"""
        if self.check_out_time:
            delta = self.check_out_time - self.check_in_time
            return round(delta.total_seconds() / 3600, 2)
        return None
    
    @property
    def is_active(self):
        """Check if this record is still open (no check-out)"""
        return self.check_out_time is None
    
    @property
    def is_late(self):
        """Check if check-in was after the configured late threshold."""
        local_check_in = timezone.localtime(self.check_in_time)
        threshold = AttendanceSettings.get_solo().late_threshold
        return local_check_in.time() >= threshold
    
    @property
    def status(self):
        """Return status label"""
        if self.is_active:
            if self.is_late:
                return 'late'
            return 'active'
        return 'completed'


class AttendanceSettings(models.Model):
    """Singleton-like settings for attendance behavior and reminders."""

    workday_start = models.TimeField(default=time(8, 0), help_text="Official workday start time.")
    late_threshold = models.TimeField(default=time(8, 30), help_text="Check-ins at or after this time are marked late.")
    birthday_reminder_days = models.PositiveSmallIntegerField(default=7)
    internship_reminder_days = models.PositiveSmallIntegerField(default=14)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attendance Settings"
        verbose_name_plural = "Attendance Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Attendance Settings"

    @classmethod
    def get_solo(cls):
        settings_obj = cls.objects.first()
        if settings_obj:
            return settings_obj
        return cls(pk=1)
