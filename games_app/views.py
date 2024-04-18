from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .models import Game, Player, PlayerGameLink, PlayerProfile


def signUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            player = Player.objects.create(user=user)
            PlayerProfile.objects.create(player=player)
            login(request, user)

            return redirect('/games/')
    else:
        form = UserCreationForm()
    return render(request, 'signUp.html', {'form': form})


def signIn(request):
    return render(request, 'signIn.html')


def home(request):
    genre_query = request.GET.get('genre')
    sort_order = request.GET.get('sort', 'title')  # Default sort by title

    if genre_query:
        games = Game.objects.filter(genre__icontains=genre_query)
    else:
        games = Game.objects.all()

    if sort_order == 'average_score':
        games = games.annotate(average_score=Avg('playergamelink__score')).order_by('-average_score')
    else:
        games = games.order_by(sort_order)

    return render(request, 'home.html', {'games': games})


def players(request):
    player_name_query = request.GET.get('name')
    sort = request.GET.get('sort', 'username')

    if player_name_query:
        players = Player.objects.annotate(review_count=Count('playergamelink')).filter(
            user__username__icontains=player_name_query)
    else:
        if sort == 'reviews':
            players = Player.objects.annotate(review_count=Count('playergamelink')).order_by('-review_count')
        else:
            players = Player.objects.annotate(review_count=Count('playergamelink')).order_by('user__username')

    return render(request, 'players.html', {'players': players})


def game_details(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    reviews = PlayerGameLink.objects.filter(game=game)  # Pobieranie opinii dla gry
    return render(request, 'game_details.html', {'game': game, 'reviews': reviews})


def player_details(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player_profile = get_object_or_404(PlayerProfile, player=player)
    reviews = PlayerGameLink.objects.filter(player=player)

    return render(request, 'player_details.html', {
        'player': player,
        'player_profile': player_profile,
        'reviews': reviews
    })


@login_required
def edit_bio(request, user_id):
    player_profile = get_object_or_404(PlayerProfile, player__user__id=user_id)
    if request.method == 'POST':
        bio = request.POST.get('bio')
        player_profile.bio = bio
        player_profile.save()
        return redirect('player_details', player_id=player_profile.player.id)
    return render(request, 'edit_bio.html', {'player_profile': player_profile})


@login_required
def add_review(request, game_id):
    if request.user.is_superuser:
        return redirect('game_details', game_id=game_id)

    game = get_object_or_404(Game, pk=game_id)
    if request.method == 'POST':
        score = request.POST.get('score')
        comment = request.POST.get('comment')
        player, created = Player.objects.get_or_create(user=request.user)
        PlayerGameLink.objects.create(player=player, game=game, score=score, comment=comment)
        return redirect('game_details', game_id=game_id)
    return redirect('game_details', game_id=game_id)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(PlayerGameLink, id=review_id, player__user=request.user)
    if request.method == 'POST':
        review.score = request.POST.get('score')
        review.comment = request.POST.get('comment')
        review.save()
        if 'from_profile' in request.GET:
            return HttpResponseRedirect('/games/player/' + str(request.user.player.id))  # Adjust the URL as needed
        else:
            return redirect('game_details', game_id=review.game.id)
    return redirect('game_details', game_id=review.game.id)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(PlayerGameLink, id=review_id, player__user=request.user)
    game_id = review.game.id
    review.delete()

    if 'from_profile' in request.GET:
        return HttpResponseRedirect('/games/player/' + str(request.user.player.id))  # Adjust the URL as needed
    else:
        return redirect('game_details', game_id=game_id)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        game.title = request.POST.get('title')
        game.genre = request.POST.get('genre')
        if 'image' in request.FILES:
            game.image = request.FILES['image']
        game.save()
        return redirect('/games/')
    return render(request, 'edit_game.html', {'game': game})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_game_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        image = request.FILES.get('image')
        Game.objects.create(title=title, genre=genre, image=image)
        return redirect('/games/')
    return render(request, 'add_game.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_game(_request, game_id):
    game = Game.objects.get(pk=game_id)
    game.delete()
    return redirect('/games/')
