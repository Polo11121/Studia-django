from django.contrib import admin

from .models import Player, Game, PlayerProfile, PlayerGameLink


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'average_score_display')

    search_fields = ('title', 'genre')

    def average_score_display(self, obj):
        return round(obj.average_score(), 2) if obj.average_score() is not None else "No ratings"

    average_score_display.short_description = 'Average Score'


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('get_username',)

    search_fields = ('user__username',)

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'


class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'bio')

    search_fields = ('player__user__username', 'bio')

    def get_username(self, obj):
        return obj.player.user.username

    get_username.short_description = 'Player Username'


class PlayerGameLinkAdmin(admin.ModelAdmin):
    list_display = ('get_player_username', 'get_game_title', 'score', 'comment')

    search_fields = ('player__user__username', 'game__title')

    list_filter = ('score',)

    def get_player_username(self, obj):
        return obj.player.user.username

    get_player_username.short_description = 'Player Username'

    def get_game_title(self, obj):
        return obj.game.title

    get_game_title.short_description = 'Game Title'


admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerProfile, PlayerProfileAdmin)
admin.site.register(PlayerGameLink, PlayerGameLinkAdmin)
