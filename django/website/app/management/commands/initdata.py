from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.models import Dashboard, Tournament, TournamentParticipant
import os

class Command(BaseCommand):
    help = 'Initializes data for the application'

    def handle(self, *args, **options):
        User = get_user_model()
        email = os.environ.get('DJANGO_MAIL')
        username = os.environ.get('DJANGO_USER')
        password = os.environ.get('DJANGO_PASSWORD')

        users_data = [
            {
                "username": os.environ.get('USER_1_NAME'),
                "email": os.environ.get('USER_1_EMAIL'),
                "password": os.environ.get('USER_1_PASSWORD')
            },
            {
                "username": os.environ.get('USER_2_NAME'),
                "email": os.environ.get('USER_2_EMAIL'),
                "password": os.environ.get('USER_2_PASSWORD')
            },
            {
                "username": os.environ.get('USER_3_NAME'),
                "email": os.environ.get('USER_3_EMAIL'),
                "password": os.environ.get('USER_3_PASSWORD')
            },
            {
                "username": os.environ.get('USER_4_NAME'),
                "email": os.environ.get('USER_4_EMAIL'),
                "password": os.environ.get('USER_4_PASSWORD')
            },
            {
                "username": os.environ.get('USER_5_NAME'),
                "email": os.environ.get('USER_5_EMAIL'),
                "password": os.environ.get('USER_5_PASSWORD')
            },
            {
                "username": os.environ.get('USER_6_NAME'),
                "email": os.environ.get('USER_6_EMAIL'),
                "password": os.environ.get('USER_6_PASSWORD')
            },
            {
                "username": os.environ.get('USER_7_NAME'),
                "email": os.environ.get('USER_7_EMAIL'),
                "password": os.environ.get('USER_7_PASSWORD')
            }
        ]

        if email and username and password:
            if not User.objects.filter(email=email).exists():
                admin_user = User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS(f'Superuser created: {admin_user.username}'))

                Dashboard.objects.create(
                    member=admin_user,
                    wins=5,
                    losses=0,
                    games_played=5,
                    total_points=50,
                    total_points_against=20,
                )
                self.stdout.write(self.style.SUCCESS(f'Dashboard created for admin user {admin_user.username}'))

            else:
                self.stdout.write(self.style.WARNING('Admin user already exists.'))

        for user_data in users_data:
            if not User.objects.filter(email=user_data["email"]).exists():
                user = User.objects.create_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password"]
                )
                self.stdout.write(self.style.SUCCESS(f'User created: {user.username}'))

                Dashboard.objects.create(
                    member=user,
                    wins=0,
                    losses=0,
                    games_played=0,
                    total_points=0,
                    total_points_against=0,
                )
                self.stdout.write(self.style.SUCCESS(f'Dashboard created for user {user.username}'))

        try:
            host = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" not found.'))
            return

        if not Tournament.objects.filter(host=host, number_of_players=8).exists():
            tournament = Tournament.objects.create(
                host=host,
                number_of_players=8,
                is_full=True,
                is_started=True,
                is_finished=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Tournament created and hosted by: {host.username}'))

            for user_data in users_data:
                try:
                    player = User.objects.get(username=user_data["username"])
                    TournamentParticipant.objects.create(
                        tournament=tournament,
                        player=player,
                        alias=user_data["username"]
                    )
                    self.stdout.write(self.style.SUCCESS(f'Added {player.username} to the tournament'))
                except User.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'User {user_data["username"]} not found.'))

            TournamentParticipant.objects.create(
                tournament=tournament,
                player=host,
                alias=username
            )
            self.stdout.write(self.style.SUCCESS(f'Added {host.username} to the tournament'))
