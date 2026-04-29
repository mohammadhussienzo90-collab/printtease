from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create admin users for PrintTease'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username for admin user',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email for admin user',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for admin user',
        )

    def handle(self, *args, **options):
        admins = [
            {
                'username': options.get('username') or 'admin1',
                'email': options.get('email') or 'admin1@printtease.art',
                'password': options.get('password') or 'PrintTease2024!',
            },
            {
                'username': 'admin2',
                'email': 'admin2@printtease.art',
                'password': 'PrintTease2024!',
            },
        ]

        for admin_data in admins:
            username = admin_data['username']
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'Admin user "{username}" already exists'))
            else:
                user = User.objects.create_superuser(
                    username=username,
                    email=admin_data['email'],
                    password=admin_data['password']
                )
                self.stdout.write(self.style.SUCCESS(f'Created admin user: {username}'))
                # Create profile for admin
                from accounts.models import Profile
                Profile.objects.get_or_create(user=user)

        self.stdout.write(self.style.SUCCESS('Admin setup complete!'))