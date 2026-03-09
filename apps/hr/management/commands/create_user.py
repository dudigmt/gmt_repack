from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.hr.models import Employee

class Command(BaseCommand):
    help = 'Create user with simple password'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('password', type=str, help='Password')
        parser.add_argument('--employee-id', type=str, help='Employee ID to link', default=None)
        parser.add_argument('--email', type=str, help='Email', default='')
        parser.add_argument('--first-name', type=str, help='First name', default='')
        parser.add_argument('--last-name', type=str, help='Last name', default='')
        parser.add_argument('--superuser', action='store_true', help='Create superuser')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        first_name = options['first_name']
        last_name = options['last_name']
        employee_id = options['employee_id']
        is_superuser = options['superuser']

        # Cek user sudah ada
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User {username} already exists'))
            return

        # Buat user
        if is_superuser:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

        # Link ke employee jika ada
        if employee_id:
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                employee.user = user
                employee.save()
                self.stdout.write(self.style.SUCCESS(f'Linked to employee {employee_id}'))
            except Employee.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Employee {employee_id} not found'))

        self.stdout.write(self.style.SUCCESS(f'User {username} created successfully'))
