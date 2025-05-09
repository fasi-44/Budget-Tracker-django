from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from api.models import TransactionType  # Import your Category model
import datetime


class Command(BaseCommand):
    help = 'Creates an initial admin user and default categories'

    def create_admin_user(self):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin@123'
        first_name = 'Mohammed'
        last_name = 'Fasi'

        if not User.objects.filter(username=username).exists():
            try:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_staff=True,
                    is_active=True,
                    date_joined=datetime.datetime.now()
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{username}"'))
                return True
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create superuser: {e}'))
                return False
        else:
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
            return True

    def create_default_transaction_type(self):
        transaction_types = ['Income', 'Expense']

        for name in transaction_types:
            if not TransactionType.objects.filter(name=name).exists():
                try:
                    TransactionType.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f'Successfully created transaction type "{name}"'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to create transaction type "{name}": {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'Transaction type "{name}" already exists.'))

    def handle(self, *args, **options):
        user_created = self.create_admin_user()
        categories_created = self.create_default_transaction_type()

        if user_created and categories_created:
            self.stdout.write(self.style.SUCCESS('Initial data seeding completed.'))
        else:
            self.stdout.write(self.style.ERROR('Some issues occurred during initial data seeding.'))