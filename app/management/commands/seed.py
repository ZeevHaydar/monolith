from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from app.models import User

class Command(BaseCommand):
    help = 'Seed data for the User model'

    def handle(self, *args, **options):
        users_data = [
            {
                'username': 'user1',
                'nama_depan': 'John',
                'nama_belakang': 'Doe',
                'email': 'user1@example.com',
                'password': make_password('123456789'),
            },
            {
                'username': 'user2',
                'nama_depan': 'Jane',
                'nama_belakang': 'Smith',
                'email': 'user2@example.com',
                'password': make_password('123456789'), 
            },
            # Add more user data as needed
        ]

        for user_data in users_data:
            user = User(**user_data)
            user.save()

        self.stdout.write(self.style.SUCCESS('Data seeding completed!'))
