from django.contrib import admin

from home.models import Player, Game


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_filter = ['is_winner']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass
