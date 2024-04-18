from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_game/', views.add_game_view, name='add_game'),
    path('edit_game/<int:game_id>/', views.edit_game, name='edit_game'),
    path('game/delete/<int:game_id>/', views.delete_game, name='delete_game'),
    path('game/<int:game_id>/', views.game_details, name='game_details'),
    path('game/add_review/<int:game_id>/', views.add_review, name='add_review'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('players/', views.players, name='players'),
    path('player/<int:player_id>/', views.player_details, name='player_details'),
    path('player/edit_bio/<int:user_id>/', views.edit_bio, name='edit_bio'),
    path('sign-in/', LoginView.as_view(template_name='signIn.html', next_page="/games/"), name='signIn'),
    path('sign-up/', views.signUp, name='signUp'),
    path('logout/', LogoutView.as_view(next_page='/games/'), name='logout'),
]
