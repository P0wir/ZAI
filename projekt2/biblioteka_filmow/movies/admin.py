from django.contrib import admin
from .models import Genre, Platform, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "imdb_id", "genre", "status", "release_date", "producer", "rating", "created_at")
    list_filter = ("status", "genre", "platforms")
    search_fields = ("title", "imdb_id", "description", "producer")
