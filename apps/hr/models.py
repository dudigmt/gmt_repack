from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='positions')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        unique_together = ['title', 'department']
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return f"{self.title} ({self.department.name})"

class Employee(models.Model):
    EMPLOYMENT_STATUS = (
        ('active', 'Active'),
        ('probation', 'Probation'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned'),
        ('retired', 'Retired'),
    )

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),        
    )

    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('hr', 'HR Staff'),
        ('production', 'Production Staff'),
        ('warehouse', 'Warehouse Staff'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operator')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True, help_text="Unique employee identifier (NIK)")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')
    position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name='employees')
    hire_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS, default='active')
    
    # Personal info
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_employees')

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"
