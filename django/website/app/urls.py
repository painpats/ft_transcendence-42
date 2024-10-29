from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index_view, name='index'),
    path('set_language/', views.set_language_view, name='set_language'),
    path('sign-up/', views.sign_up_view, name='sign_up'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('friends/', views.friends_view, name='friends'),
    path('friend/<str:username>/', views.friend_profile_view, name='friend_profile'),
    path('settings/', views.settings_view, name='settings'),
    path('game/', views.game_view, name='game'),
    path('classic/', views.classic_view, name='classic'),
    path('bot/', views.bot_view, name='bot'),
    path('tournament/', views.tournament_view, name='tournament'),
    path('tournament_matches/', views.tournament_matches_view, name='tournament_matches'),
    path('tournament_play/<int:match_id>/', views.tournament_play_view, name='tournament_play'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('sign-in/', views.sign_in_view, name='sign_in'),
    path('auth_42/', views.auth_42, name='auth_42'),
    path('callback_42/', views.callback_view, name='callback_42'),
]
