from django.utils import timezone
from django.db import transaction
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.conf import settings
from .forms import *
from urllib.parse import urlencode
import requests

##########################################################################################
# INDEX VIEW                                                                             #
##########################################################################################

def index_view(request):
    lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, 'en')
    translation.activate(lang)
    request.LANGUAGE_CODE = lang
    return render(request, 'index.html')

def set_language_view(request):
    lang = request.GET.get('lang', 'en')
    translation.activate(lang)
    request.session[settings.LANGUAGE_COOKIE_NAME] = lang 

    if request.user.is_authenticated:
        member = Member.objects.get(email=request.user.email)
        member.language = lang
        member.save()

    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response

##########################################################################################
# SIGN UP VIEW                                                                           #
##########################################################################################

def sign_up_view(request):
    lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, 'en')
    translation.activate(lang)
    request.LANGUAGE_CODE = lang

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            member = form.save()
            login(request, member)
            Dashboard.objects.create(member=member)
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('sign_up')

    form = SignUpForm()
    return render(request, 'sign_up.html', {
        'form': form})

##########################################################################################
# SIGN IN VIEW                                                                           #
##########################################################################################

def sign_in_view(request):
    lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, 'en')
    translation.activate(lang)
    request.LANGUAGE_CODE = lang

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            member = authenticate(email=email, password=password)

            if member is not None:
                logout(request)
                login(request, member)
                user_lang = member.language
                if user_lang:
                    translation.activate(user_lang)
                    request.session[settings.LANGUAGE_COOKIE_NAME] = user_lang
                    response = redirect('profile')
                    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_lang)
                    return response

                return redirect('profile')
            else:
                messages.error(request, _("Invalid email or password."))
                return redirect('sign_in')
    
    form = SignInForm()
    return render(request, 'sign_in.html', {
        'form': form})


##########################################################################################
# PROFILE VIEW                                                                           #
##########################################################################################

@login_required
def profile_view(request):
    member = request.user
    dashboard, created = Dashboard.objects.get_or_create(member=member)
    games = Game.objects.filter(player=member).order_by('-date')
    return render(request, 'profile.html', {
        'member': member,
        'dashboard': dashboard,
        'games': games})

##########################################################################################
# DASHBOARD VIEW                                                                         #                                                                         
##########################################################################################


@login_required
def dashboard_view(request):
    member = request.user
    dashboard = Dashboard.objects.get(member=member)

    ratio_global = dashboard.wins / dashboard.games_played if dashboard.games_played > 0 else 0
    ratio_classic = dashboard.wins_classic / dashboard.games_played_classic if dashboard.games_played_classic > 0 else 0
    ratio_bot = dashboard.wins_bot / dashboard.games_played_bot if dashboard.games_played_bot > 0 else 0
    ratio_tournament = dashboard.wins_tournament / dashboard.games_played_tournament if dashboard.games_played_tournament > 0 else 0

    stats = {
        'global': {
            'wins': dashboard.wins,
            'losses': dashboard.losses,
            'games_played': dashboard.games_played,
            'total_points': dashboard.total_points,
            'total_points_against': dashboard.total_points_against,
            'ratio': ratio_global,
        },
        'classic': {
            'wins': dashboard.wins_classic,
            'losses': dashboard.losses_classic,
            'games_played': dashboard.games_played_classic,
            'total_points': dashboard.total_points_classic,
            'total_points_against': dashboard.total_points_against_classic,
            'ratio': ratio_classic,
        },
        'bot': {
            'wins': dashboard.wins_bot,
            'losses': dashboard.losses_bot,
            'games_played': dashboard.games_played_bot,
            'total_points': dashboard.total_points_bot,
            'total_points_against': dashboard.total_points_against_bot,
            'ratio': ratio_bot,
        },
        'tournament': {
            'wins': dashboard.wins_tournament,
            'losses': dashboard.losses_tournament,
            'games_played': dashboard.games_played_tournament,
            'total_points': dashboard.total_points_tournament,
            'total_points_against': dashboard.total_points_against_tournament,
            'ratio': ratio_tournament,
        }
    }

    stats_json = json.dumps(stats)

    return render(request, 'dashboard.html', {
        'member': member,
        'dashboard': dashboard,
        'stats': stats_json})

##########################################################################################
# GAME VIEW                                                                             #
##########################################################################################

@login_required
def game_view(request):
    member = request.user
    return render(request, 'game.html', {
        'member': member})

##########################################################################################
# CLASSIC VIEW                                                                           #
##########################################################################################

@login_required
def classic_view(request):
    member = request.user

    if request.method == 'POST':
        opponent_alias = request.POST.get('opponent_alias')
        player_points = int(request.POST.get('player_score'))
        opponent_points = int(request.POST.get('opponent_score'))
        game_type = 'C'

        game_instance = Game(
            player=member,
            player_alias=member.username,
            opponent_alias=opponent_alias,
            player_points=player_points,
            opponent_points=opponent_points,
            game_type='C',
            date=timezone.now()
        )
        game_instance.save()
        update_dashboard(member, player_points, opponent_points, game_type)
        return redirect('game')

    return render(request, 'classic.html', {
        'member': member})

##########################################################################################
# BOT VIEW                                                                              #
##########################################################################################

@login_required
def bot_view(request):
    member = request.user

    if request.method == 'POST':
        opponent_alias = request.POST.get('opponent_alias')
        player_points = int(request.POST.get('player_score'))
        opponent_points = int(request.POST.get('opponent_score'))
        game_type = 'B'

        game_instance = Game(
            player=member,
            player_alias=member.username,
            opponent_alias=opponent_alias,
            player_points=player_points,
            opponent_points=opponent_points,
            game_type='B',
            date=timezone.now()
        )
        game_instance.save()
        update_dashboard(member, player_points, opponent_points, game_type)
        return redirect('game')

    return render(request, 'bot.html', {
        'member': member})

##########################################################################################
# TOURNAMENT VIEW                                                                       #
##########################################################################################

@login_required
def tournament_view(request):
    member = request.user

    if request.method == 'POST':
        if 'create_tournament' in request.POST:
            return tournament_create_view(request)
        elif 'join_tournament' in request.POST:
            return tournament_join_view(request)

    tournaments_unfull = Tournament.objects.filter(is_full=False).exclude(host=member)
    tournaments_host = Tournament.objects.filter(host=member)
    tournaments_registered = Tournament.objects.filter(participants_list__player=member).exclude(host=member)

    return render(request, 'tournament.html', {
        'tournaments_unfull': tournaments_unfull,
        'tournaments_host': tournaments_host,
        'tournaments_registered': tournaments_registered})


@login_required
def tournament_create_view(request):
    member = request.user

    if Tournament.objects.filter(host=member, is_finished=False).exists():
        messages.error(request, _("You are already hosting an unfinished tournament."))
        return redirect('tournament')

    number_players = int(request.POST.get('number_players'))
    alias = request.POST.get('alias')

    tournament = Tournament.objects.create(host=member, number_of_players=number_players)
    TournamentParticipant.objects.create(tournament=tournament, player=member, alias=alias)

    return redirect('tournament')

@login_required
def tournament_join_view(request):
    member = request.user
    tournament_id = request.POST.get('tournament_id')
    alias = request.POST.get('alias')

    tournament = Tournament.objects.filter(id=tournament_id).first()

    if not tournament:
        messages.error(request, _("The tournament does not exist."))
        return redirect('tournament')

    if TournamentParticipant.objects.filter(tournament=tournament, player=member).exists():
        messages.error(request, _("You are already registered in this tournament."))
        return redirect('tournament')

    if TournamentParticipant.objects.filter(tournament=tournament, alias=alias).exists():
        messages.error(request, _("This alias is already taken in this tournament."))
        return redirect('tournament')

    TournamentParticipant.objects.create(tournament=tournament, player=member, alias=alias)

    if tournament.participants.count() >= tournament.number_of_players:
        tournament.is_full = True
        tournament.is_started = True
        tournament.save()

    return redirect('tournament')

@login_required
def tournament_matches_view(request):
    member = request.user
    tournament = Tournament.objects.filter(host=member, is_started=True).first()

    if not tournament:
        return redirect('tournament')

    participants = list(tournament.participants_list.all())
    if len(participants) == 1:
        TournamentMatch.objects.filter(tournament=tournament).delete()
        TournamentParticipant.objects.filter(id=participants[0].id).delete()
        tournament.delete()
        return redirect('game')

    if tournament.matches.count() > 0:
        matches = tournament.matches.filter(is_finished=False)
        return render(request, 'tournament_matches.html', {
            'tournament': tournament,
            'matches': matches})

    if len(participants) == 8:
        for i in range(0, len(participants), 2):
            TournamentMatch.objects.create(tournament=tournament, player1=participants[i], player2=participants[i+1])
    elif len(participants) == 4:
        for i in range(0, len(participants), 2):
            TournamentMatch.objects.create(tournament=tournament, player1=participants[i], player2=participants[i+1])
    elif len(participants) == 2:
        TournamentMatch.objects.create(tournament=tournament, player1=participants[0], player2=participants[1])

    matches = tournament.matches.filter(is_finished=False)

    return render(request, 'tournament_matches.html', {
        'tournament': tournament,
        'matches': matches})

@login_required
def tournament_play_view(request, match_id):
    match = TournamentMatch.objects.get(id=match_id)
    tournament = match.tournament

    if not tournament:
        return redirect('tournament')

    if request.method == 'POST':
        player_score = int(request.POST.get('player_score'))
        opponent_score = int(request.POST.get('opponent_score'))

        match.player1_score = player_score
        match.player2_score = opponent_score
        match.is_finished = True
        match.save()
        updateDashboardTournament(match)

        if match.player1_score > match.player2_score:
            loser = match.player2
        else:
            loser = match.player1
        TournamentParticipant.objects.filter(id=loser.id).delete()

        return redirect('tournament_matches')

    return render(request, 'tournament_play.html', {
        'match': match})

##########################################################################################
# UPDATE DASHBOARD                                                                       #
##########################################################################################

def updateDashboardTournament(match):
    player1 = match.player1.player
    player2 = match.player2.player
    dashboard1 = Dashboard.objects.get(member=player1)
    dashboard2 = Dashboard.objects.get(member=player2)

    Game.objects.create(
        player=player1,
        player_alias=match.player1.alias,
        opponent_alias=match.player2.alias,
        player_points=match.player1_score,
        opponent_points=match.player2_score,
        game_type='T',
        date=timezone.now()
    )
    
    Game.objects.create(player=player2,
        player_alias=match.player2.alias,
        opponent_alias=match.player1.alias,
        player_points=match.player2_score,
        opponent_points=match.player1_score,
        game_type='T',
        date=timezone.now()
    )

    if match.player1_score > match.player2_score:
        dashboard1.wins += 1
        dashboard2.losses += 1
    else:
        dashboard1.losses += 1
        dashboard2.wins += 1
    
    dashboard1.games_played += 1
    dashboard1.total_points += match.player1_score
    dashboard1.total_points_against += match.player2_score
    dashboard1.wins_tournament += 1 if match.player1_score > match.player2_score and match.tournament.participants_list.count() == 2 else 0
    dashboard1.losses_tournament += 1 if match.player1_score < match.player2_score else 0
    dashboard1.games_played_tournament += 1
    dashboard1.total_points_tournament += match.player1_score
    dashboard1.total_points_against_tournament += match.player2_score
    dashboard1.save()

    dashboard2.games_played += 1
    dashboard2.total_points += match.player2_score
    dashboard2.total_points_against += match.player1_score
    dashboard2.wins_tournament += 1 if match.player2_score > match.player1_score and match.tournament.participants_list.count() == 2 else 0
    dashboard2.losses_tournament += 1 if match.player2_score < match.player1_score else 0
    dashboard2.games_played_tournament += 1
    dashboard2.total_points_tournament += match.player2_score
    dashboard2.total_points_against_tournament += match.player1_score
    dashboard2.save()

def update_dashboard(member, player_points, opponent_points, game_type):
    dashboard = Dashboard.objects.get(member=member)
    
    dashboard.wins += 1 if player_points > opponent_points else 0
    dashboard.losses += 1 if player_points < opponent_points else 0
    dashboard.games_played += 1
    dashboard.total_points += player_points
    dashboard.total_points_against += opponent_points
    
    if game_type == 'C':
        dashboard.wins_classic += 1 if player_points > opponent_points else 0
        dashboard.losses_classic += 1 if player_points < opponent_points else 0
        dashboard.games_played_classic += 1
        dashboard.total_points_classic += player_points
        dashboard.total_points_against_classic += opponent_points
    elif game_type == 'B':
        dashboard.wins_bot += 1 if player_points > opponent_points else 0
        dashboard.losses_bot += 1 if player_points < opponent_points else 0
        dashboard.games_played_bot += 1
        dashboard.total_points_bot += player_points
        dashboard.total_points_against_bot += opponent_points

    dashboard.save()

##########################################################################################
# FRIENDS VIEW                                                                           #
##########################################################################################

@login_required
def friends_view(request):
    member = request.user
    friends = Friend.objects.filter(user=member, status='A')
    received_invitations = Friend.objects.filter(friend=member, status='P')
    sent_invitations = Friend.objects.filter(user=member, status='P')
    add_friend_form = AddFriendForm(user=member)


    if request.method == 'POST':
        if 'add_friend' in request.POST:
            add_friend_form = AddFriendForm(request.POST, user=member)
            if add_friend_form.is_valid():
                friend = add_friend_form.cleaned_data['add_friend']
                Friend.objects.create(user=member, friend=friend, status='P')
            else:
                for field, errors in add_friend_form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        elif 'accept_invitation' in request.POST:
            invitation_id = request.POST.get('accept_invitation')
            invitation = Friend.objects.get(id=invitation_id, friend=member)
            invitation.status = 'A'
            invitation.save()
            Friend.objects.create(user=member, friend=invitation.user, status='A')

        elif 'decline_invitation' in request.POST:
            invitation_id = request.POST.get('decline_invitation')
            invitation = Friend.objects.get(id=invitation_id, friend=member)
            invitation.delete()

        elif 'remove_friend' in request.POST:
            friend_id = request.POST.get('remove_friend')
            friendship = Friend.objects.get(id=friend_id, user=member)
            reverse_friendship = Friend.objects.get(user=friendship.friend, friend=member)
            friendship.delete()
            reverse_friendship.delete()

        return redirect('friends')

    return render(request, 'friends.html', {
        'member': member, 
        'friends': friends, 
        'received_invitations': received_invitations, 
        'sent_invitations': sent_invitations, 
        'add_friend_form': add_friend_form})

##########################################################################################
# FRIENDS HISTORY VIEW                                                                   #
##########################################################################################

@login_required
def friend_profile_view(request, username):
    member = request.user

    if not Friend.objects.filter(user=member, friend__username=username, status='A').exists():
        return redirect('friends')
    friend = Member.objects.get(username=username)
    games = Game.objects.filter(player=friend).order_by('-date')
    dashboard = Dashboard.objects.get(member=friend)
    
    return render(request, 'friend_profile.html', {
        'member': member,
        'friend': friend,
        'games': games,
        'dashboard': dashboard})

##########################################################################################
# SETTINGS VIEW                                                                          #
##########################################################################################

@login_required
def settings_view(request):
    member = request.user
    dashboard = Dashboard.objects.get(member=member)
    form_change_pseudo = ChangePseudoForm(instance=member)
    form_change_email = ChangeEmailForm(instance=member)
    form_change_password = ChangePasswordForm(user=member)
    form_change_avatar = ChangeAvatarForm(instance=member)
    

    if request.method == 'POST':
        if 'update_avatar' in request.POST:
            form_change_avatar = ChangeAvatarForm(request.POST, request.FILES, instance=member)
            if form_change_avatar.is_valid():
                form_change_avatar.save()
            else:
                messages.error(request, _("Cannot change avatar"))
                for field, errors in form_change_avatar.errors.items():
                    for error in errors:
                        messages.error(request, error)

        elif 'delete_avatar' in request.POST:
            if member.avatar:
                member.avatar.delete(save=False)
                member.avatar = None
                member.save()
            else:
                messages.error(request, _("No avatar to delete"))

        elif 'update_pseudo' in request.POST:
            form_change_pseudo = ChangePseudoForm(request.POST, instance=member)
            if form_change_pseudo.is_valid():
                form_change_pseudo.save()
            else:
                messages.error(request, _("Cannot change pseudo"))
                for field, errors in form_change_pseudo.errors.items():
                    for error in errors:
                        messages.error(request, error)

        elif 'update_email' in request.POST:
            form_change_email = ChangeEmailForm(request.POST, instance=member)
            if form_change_email.is_valid():
                form_change_email.save()
            else:
                messages.error(request, _("Cannot change email"))
                for field, errors in form_change_email.errors.items():
                    for error in errors:
                        messages.error(request, error)

        elif 'update_password' in request.POST:
            form_change_password = ChangePasswordForm(request.POST, user=member)
            if form_change_password.is_valid():
                new_password = form_change_password.cleaned_data['new_password']
                member.set_password(new_password)
                member.save()
                update_session_auth_hash(request, member)
            else:
                messages.error(request, _("Cannot change password"))
                for field, errors in form_change_password.errors.items():
                    for error in errors:
                        messages.error(request, error)
        
        elif 'delete_account' in request.POST:
            delete_member(request)

        return redirect('settings')


    return render(request, 'settings.html', {
        'member': member, 'dashboard': dashboard,
        'form_change_pseudo': form_change_pseudo,
        'form_change_email': form_change_email,
        'form_change_password': form_change_password,
        'form_change_avatar': form_change_avatar})


def delete_member(request):
    member = request.user
    
    with transaction.atomic():
        tournaments = TournamentParticipant.objects.filter(player=member)
        for tournament_participant in tournaments:
            tournament = tournament_participant.tournament
            
            if tournament.is_full and tournament.is_started and tournament.host != member:
                tournament.is_full = False
                tournament.is_started = False
                tournament.save()

            TournamentMatch.objects.filter(tournament=tournament).delete()

        Friend.objects.filter(user=member).delete()
        Friend.objects.filter(friend=member).delete()

        Game.objects.filter(player=member).delete()

        TournamentParticipant.objects.filter(player=member).delete()
        Tournament.objects.filter(host=member).delete()

        Dashboard.objects.filter(member=member).delete()

        member.delete()

    return redirect('index')

##########################################################################################
# authentification 42                                                                    #
##########################################################################################

def auth_42(request):
    client_id = settings.CLIENT_ID
    redirect_uri = settings.URI
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
    }
    authorization_url = f"https://api.intra.42.fr/oauth/authorize?{urlencode(params)}"

    return redirect(authorization_url)

def callback_view(request):
    code = request.GET.get('code')

    if code is None:
        return redirect('sign_in')
    token_url = 'https://api.intra.42.fr/oauth/token'
    
    data = {
        'grant_type': 'authorization_code',
        'client_id':settings.CLIENT_ID,
        'client_secret':settings.CLIENT_SECRET,
        'code': code,
        'redirect_uri':settings.URI,
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()
    access_token = token_data.get('access_token')
    if not access_token:
        return redirect('sign_in')
    user_info_url = 'https://api.intra.42.fr/v2/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    return authenticate_and_login_user(request, user_info)

def authenticate_and_login_user(request, user_info):
    email = user_info['email']
    username = user_info['login']

    user, created = Member.objects.get_or_create(
        email=email,
        defaults={'username': username}
    )

    login(request, user)
    return redirect('profile')