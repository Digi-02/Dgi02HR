# attendance/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Employee, AttendanceRecord, Category, Department
from .models import EmployeeEducation, EmployeeCertification, EmployeeWorkExperience, AttendanceException


class EmployeeForm(forms.ModelForm):
    """Form for adding/editing employees with category-specific fields"""
    
    class Meta:
        model = Employee
        fields = [
            'category', 'title', 'first_name', 'last_name', 
            'email', 'personal_email', 'phone', 'alternative_phone', 'gender',
            'date_of_birth', 'nationality', 'marital_status', 'religion',
            'blood_group', 'genotype',
            'residential_address', 'permanent_address', 'city', 'state',
            'country', 'postal_code', 'local_government',
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone',
            'next_of_kin_name', 'next_of_kin_relationship', 'next_of_kin_phone',
            'next_of_kin_email', 'next_of_kin_address',
            'department', 'position', 'line_manager',
            'hire_date', 'end_date', 'probation_end_date', 'institution',
            'qualification_obtained', 'field_of_study', 'year_of_graduation',
            'class_of_degree', 'student_id', 'supervisor',
            'nin_number', 'passport_number', 'passport_expiry_date',
            'tin_number', 'drivers_license_number',
            'work_permit_number', 'work_permit_expiry_date',
            'employment_status', 'is_active'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'id': 'category-select'
            }),
            'title': forms.Select(attrs={'class': 'form-select'}),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Work email (used for kiosk)'
            }),
            'personal_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Personal email (optional)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'alternative_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Alternative phone number'
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nationality'
            }),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'religion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Religion'
            }),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'genotype': forms.Select(attrs={'class': 'form-select'}),
            'residential_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Current residential address'
            }),
            'permanent_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Permanent home address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal code'
            }),
            'local_government': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Local government area'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact full name'
            }),
            'emergency_contact_relationship': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Relationship'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact phone'
            }),
            'next_of_kin_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Next of kin full name'
            }),
            'next_of_kin_relationship': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Relationship'
            }),
            'next_of_kin_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Next of kin phone'
            }),
            'next_of_kin_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Next of kin email'
            }),
            'next_of_kin_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Next of kin address'
            }),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Software Developer, Intern, Student'
            }),
            'line_manager': forms.Select(attrs={'class': 'form-select'}),
            'hire_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Start date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Expected end date (interns/students)'
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control intern-student-field',
                'placeholder': 'University/School name'
            }),
            'qualification_obtained': forms.TextInput(attrs={
                'class': 'form-control intern-student-field',
                'placeholder': 'Qualification obtained'
            }),
            'field_of_study': forms.TextInput(attrs={
                'class': 'form-control intern-student-field',
                'placeholder': 'Course or program'
            }),
            'year_of_graduation': forms.NumberInput(attrs={
                'class': 'form-control intern-student-field',
                'placeholder': 'Year of graduation',
                'min': 1900
            }),
            'class_of_degree': forms.TextInput(attrs={
                'class': 'form-control intern-student-field',
                'placeholder': 'Class of degree'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control student-field',
                'placeholder': 'School ID number'
            }),
            'supervisor': forms.Select(attrs={
                'class': 'form-select intern-student-field'
            }),
            'probation_end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'nin_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NIN number'
            }),
            'passport_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Passport number'
            }),
            'passport_expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tin_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'TIN'
            }),
            'drivers_license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Driver's license number"
            }),
            'work_permit_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Work permit or visa permit number'
            }),
            'work_permit_expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'employment_status': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter supervisor choices to only Staff
        staff_category = Category.objects.filter(code='STAFF').first()
        if staff_category:
            self.fields['supervisor'].queryset = Employee.objects.filter(
                category=staff_category,
                is_active=True
            )
        else:
            self.fields['supervisor'].queryset = Employee.objects.none()

        self.fields['line_manager'].queryset = Employee.objects.filter(
            is_active=True
        ).order_by('first_name', 'last_name')
        if self.instance.pk:
            self.fields['line_manager'].queryset = self.fields['line_manager'].queryset.exclude(pk=self.instance.pk)
            self.fields['supervisor'].queryset = self.fields['supervisor'].queryset.exclude(pk=self.instance.pk)
        
        # Make fields required based on category (handled by JS, but set initial)
        self.fields['department'].required = False
        self.fields['supervisor'].required = False
        self.fields['line_manager'].required = False
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            qs = Employee.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('A person with this email already exists.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')

        # Staff-specific validation (birthday is now optional for all)
        if category and category.code == 'STAFF':
            if not cleaned_data.get('hire_date'):
                self.add_error('hire_date', 'Hire date is required for Staff.')
            if not cleaned_data.get('department'):
                self.add_error('department', 'Department is required for Staff.')

        # Intern-specific validation
        if category and category.code == 'INTERN':
            if not cleaned_data.get('hire_date'):
                self.add_error('hire_date', 'Start date is required for Interns.')
            if not cleaned_data.get('end_date'):
                self.add_error('end_date', 'End date is required for Interns.')
            if not cleaned_data.get('institution'):
                self.add_error('institution', 'Institution is required for Interns.')

        # Student-specific validation
        if category and category.code == 'STUDENT':
            if not cleaned_data.get('hire_date'):
                self.add_error('hire_date', 'Start date is required for Students.')
            if not cleaned_data.get('end_date'):
                self.add_error('end_date', 'End date is required for Students.')
            if not cleaned_data.get('institution'):
                self.add_error('institution', 'Institution is required for Students.')
            if not cleaned_data.get('student_id'):
                self.add_error('student_id', 'Student ID is required.')

        return cleaned_data


class ManualAttendanceForm(forms.Form):
    """Form for HR to manually add attendance records"""

    ENTRY_TYPE_CHOICES = [
        ('work_session', 'Work Session'),
        ('exception', 'Attendance Exception'),
    ]

    entry_type = forms.ChoiceField(
        choices=ENTRY_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='work_session'
    )

    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(is_active=True, employment_status='active'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Person"
    )

    check_in_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        help_text="Date and time of check-in"
    )
    
    check_out_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        help_text="Leave blank if still working"
    )

    exception_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Select exception type')] + list(AttendanceException.EXCEPTION_TYPE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    exception_start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    exception_end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional notes or approval context'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Group employees by category in dropdown
        self.fields['employee'].queryset = Employee.objects.filter(
            is_active=True, 
            employment_status='active'
        ).select_related('category').order_by('category__name', 'first_name')

    def clean(self):
        cleaned_data = super().clean()
        entry_type = cleaned_data.get('entry_type')
        check_in = cleaned_data.get('check_in_time')
        check_out = cleaned_data.get('check_out_time')
        exception_type = cleaned_data.get('exception_type')
        exception_start_date = cleaned_data.get('exception_start_date')
        exception_end_date = cleaned_data.get('exception_end_date')

        if entry_type == 'work_session':
            if not check_in:
                self.add_error('check_in_time', 'Check-in time is required for a work session.')
            if check_in and check_out and check_out <= check_in:
                self.add_error('check_out_time', 'Check-out time must be after check-in time.')
        elif entry_type == 'exception':
            if not exception_type:
                self.add_error('exception_type', 'Select an exception type.')
            if not exception_start_date:
                self.add_error('exception_start_date', 'Start date is required for an attendance exception.')
            if not exception_end_date:
                self.add_error('exception_end_date', 'End date is required for an attendance exception.')
            if exception_start_date and exception_end_date and exception_end_date < exception_start_date:
                self.add_error('exception_end_date', 'End date cannot be earlier than the start date.')

        return cleaned_data


class DateFilterForm(forms.Form):
    """Form for filtering attendance by date"""
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )
    
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'From'
        }),
        required=False
    )
    
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'To'
        }),
        required=False
    )
    
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        empty_label="All People"
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        empty_label="All Categories"
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True).order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        empty_label="All Departments"
    )

    employment_status = forms.ChoiceField(
        choices=[('', 'All Employment Status')] + list(Employee.EMPLOYMENT_STATUS),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search name, email, or employee ID'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.filter(is_active=True).order_by('first_name', 'last_name')


class EmployeeEducationForm(forms.ModelForm):
    class Meta:
        model = EmployeeEducation
        fields = ['qualification_obtained', 'institution', 'field_of_study', 'year_of_graduation', 'class_of_degree']
        widgets = {
            'qualification_obtained': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qualification obtained'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institution'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Field of study'}),
            'year_of_graduation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year', 'min': 1900}),
            'class_of_degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class of degree'}),
        }


class EmployeeCertificationForm(forms.ModelForm):
    class Meta:
        model = EmployeeCertification
        fields = ['certification_name', 'issuing_body', 'date_obtained', 'expiry_date']
        widgets = {
            'certification_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certification name'}),
            'issuing_body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Issuing body'}),
            'date_obtained': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class EmployeeWorkExperienceForm(forms.ModelForm):
    class Meta:
        model = EmployeeWorkExperience
        fields = ['employer_name', 'job_title', 'start_date', 'end_date', 'reason_for_leaving', 'skills_and_competence']
        widgets = {
            'employer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Previous employer'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job title'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason_for_leaving': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for leaving'}),
            'skills_and_competence': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Skills and competence'}),
        }


EmployeeEducationFormSet = inlineformset_factory(
    Employee,
    EmployeeEducation,
    form=EmployeeEducationForm,
    extra=1,
    can_delete=True,
)

EmployeeCertificationFormSet = inlineformset_factory(
    Employee,
    EmployeeCertification,
    form=EmployeeCertificationForm,
    extra=1,
    can_delete=True,
)

EmployeeWorkExperienceFormSet = inlineformset_factory(
    Employee,
    EmployeeWorkExperience,
    form=EmployeeWorkExperienceForm,
    extra=1,
    can_delete=True,
)
