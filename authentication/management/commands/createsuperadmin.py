from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a super admin user'
    
    def add_arguments(self, parser):
        parser.add_argument('--username', required=True, help='Username for super admin')
        parser.add_argument('--email', required=True, help='Email for super admin')
        parser.add_argument('--password', required=True, help='Password for super admin')
    
    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            return
        
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            user_type='super_admin'
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'Super admin {username} created successfully!'
        ))