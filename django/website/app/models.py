from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

################################################################################################
# ALL models can be changed, use "make re" to make sure migrations are done and database is ok #
# If you want to see tables directly, go on https://transcendence.fr/admin                     #
# Fill the form with DJANGO_USER and DJANGO_PASSWORD (.env)                                    #
################################################################################################

################################################################################################
# MEMBER MODELS                                                                                #
################################################################################################

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class MemberManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class Member(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='', null=True, blank=True)
    language = models.CharField(max_length=2, default='en')
    is_online = models.BooleanField(default=True)
    last_request = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


################################################################################################
# GAME MODEL                                                                                   #
################################################################################################

class Game(models.Model):
    CLASSIC = 'C'
    BOT = 'B'
    TOURNAMENT = 'T'

    STATUS_CHOICES = [
        (CLASSIC, 'Classic'),
        (BOT, 'Bot'),
        (TOURNAMENT, 'Tournament'),
    ]

    player = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='player_sessions')
    player_alias = models.CharField(max_length=15)
    opponent_alias = models.CharField(max_length=15, blank=True, null=True)
    player_points = models.IntegerField()
    opponent_points = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    game_type = models.CharField(max_length=1, choices=STATUS_CHOICES, default=CLASSIC)

    def __str__(self):
        return f"Game between {self.player_alias} and {self.opponent_alias} ({self.date})"

################################################################################################
# TOURNAMENT MODELS                                                                            #
################################################################################################

class Tournament(models.Model):
    host = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='hosted_tournaments')
    number_of_players = models.IntegerField(choices=[(4, '4 Players'), (8, '8 Players')], default=4)
    participants = models.ManyToManyField(Member, through='TournamentParticipant', related_name='tournaments')
    is_full = models.BooleanField(default=False)
    is_started = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"Tournament hosted by {self.host.username}"

class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participants_list')
    player = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='tournaments_participated')
    alias = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.alias} ({self.player.username}) in {self.tournament.host.username}'s tournament"

class TournamentMatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    player1 = models.ForeignKey(TournamentParticipant, on_delete=models.CASCADE, related_name='player1_matches')
    player2 = models.ForeignKey(TournamentParticipant, on_delete=models.CASCADE, related_name='player2_matches')
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"Match between {self.player1.alias} and {self.player2.alias} in {self.tournament}"


################################################################################################
# DASHBOARD MODEL                                                                              #
################################################################################################

class Dashboard(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    ############################################################
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    total_points_against = models.IntegerField(default=0)
    ############################################################
    wins_classic = models.IntegerField(default=0)
    losses_classic = models.IntegerField(default=0)
    games_played_classic = models.IntegerField(default=0)
    total_points_classic = models.IntegerField(default=0)
    total_points_against_classic = models.IntegerField(default=0)
    ############################################################
    wins_bot = models.IntegerField(default=0)
    losses_bot = models.IntegerField(default=0)
    games_played_bot = models.IntegerField(default=0)
    total_points_bot = models.IntegerField(default=0)
    total_points_against_bot = models.IntegerField(default=0)
    ############################################################
    wins_tournament = models.IntegerField(default=0)
    losses_tournament = models.IntegerField(default=0)
    games_played_tournament = models.IntegerField(default=0)
    total_points_tournament = models.IntegerField(default=0)
    total_points_against_tournament = models.IntegerField(default=0)
    ################################################

    def __str__(self):
        return f"Dashboard for {self.member.username}"

################################################################################################
# FRIENDS MODEL                                                                                #
################################################################################################

class Friend(models.Model):
    PENDING = 'P'
    ACCEPTED = 'A'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
    ]

    user = models.ForeignKey(Member, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(Member, related_name='friend_of', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} and {self.friend.username} ({self.get_status_display()})"
