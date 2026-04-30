from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    help = 'Setup production - run migrations and create admins'

    def handle(self, *args, **options):
        self.stdout.write('Running production setup...')

        # Run migrations
        from django.core.management import call_command
        call_command('migrate', '--noinput')
        self.stdout.write(self.style.SUCCESS('Migrations complete'))

        # Create admins if they don't exist
        admins = [
            {'username': 'admin1', 'email': 'admin1@printtease.art', 'password': 'PrintTease2024!'},
            {'username': 'admin2', 'email': 'admin2@printtease.art', 'password': 'PrintTease2024!'},
        ]

        for admin_data in admins:
            username = admin_data['username']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_superuser(
                    username=username,
                    email=admin_data['email'],
                    password=admin_data['password']
                )
                Profile.objects.get_or_create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Created admin: {username}'))

        # Collect static files
        call_command('collectstatic', '--noinput', '--clear')
        self.stdout.write(self.style.SUCCESS('Static files collected'))

        self.stdout.write(self.style.SUCCESS('Production setup complete!'))