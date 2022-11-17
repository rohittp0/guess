import random

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from home.models import Player, Game


# Create your views here.
def home(request: WSGIRequest) -> HttpResponse:
    uid = request.COOKIES.get("uid")
    game = Game.objects.all().first()

    if uid is None:
        player = Player.objects.create(game=game)
    else:
        player = Player.objects.get(id=uid)

    context = {
        "started": game.started,
        "ended": game.ended,
        "total": game.total - player.value,
        "players": game.players,
    }

    response = render(request, 'home.html', context=context)
    response.set_cookie("uid", player.id)

    return response


def guess(request: WSGIRequest) -> HttpResponse:
    uid = request.COOKIES.get("uid")
    player = Player.objects.get(id=uid or -1)

    player.guess = int(request.GET.get("guess")) if player.guess == -1 else player.guess
    player.is_winner = player.guess == player.value
    player.save()

    context = {
        "winner": player.is_winner,
    }

    return render(request, 'guess.html', context=context)


def start(request: WSGIRequest) -> HttpResponse:
    game = Game.objects.all().first()

    game.total = 0

    for player in Player.objects.all():
        player.value = random.randint(1, game.players)
        game.total += player.value
        player.save()

    game.started = True
    game.ended = False
    game.save()

    return HttpResponse("Game started")


def stop(request: WSGIRequest) -> HttpResponse:
    game = Game.objects.all().first()

    game.started = False
    game.ended = True
    game.save()

    return HttpResponse("Game stopped")
