
from .views import *
from .api_views import MovieViewSet, GenreViewSet, import_movie_from_omdb, import_movies_bulk
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'api/movies', MovieViewSet, basename='api-movie')
router.register(r'api/genres', GenreViewSet, basename='api-genre')

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
    path("api/import/movie/", import_movie_from_omdb, name="api-import-movie"),
    path("api/import/movies/", import_movies_bulk, name="api-import-movies"),

    path("", include(router.urls)),
]

urlpatterns += [
    path("", include(router.urls)),
]