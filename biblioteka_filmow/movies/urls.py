from django.urls import path
from .views import *

urlpatterns = [
    path("", MovieListView.as_view(), name="movie_list"),
    path("movie/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("movie/add/", MovieCreateView.as_view(), name="movie_add"),
    path("movie/<int:pk>/edit/", MovieUpdateView.as_view(), name="movie_edit"),
    path("movie/<int:pk>/delete/", MovieDeleteView.as_view(), name="movie_delete"),

    path("genres/", GenreListView.as_view(), name="genre_list"),
    path("genre/<int:pk>/", GenreDetailView.as_view(), name="genre_detail"),
    path("genre/add/", GenreCreateView.as_view(), name="genre_add"),
    path("genre/<int:pk>/edit/", GenreUpdateView.as_view(), name="genre_edit"),
    path("genre/<int:pk>/delete/", GenreDeleteView.as_view(), name="genre_delete"),
]