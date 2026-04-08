from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Movie, Genre, Platform
from .forms import MovieForm, GenreForm, PlatformForm


class MovieListView(ListView):
    model = Movie
    template_name = "movies/movie_list.html"
    context_object_name = "movies"


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"


class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = "movies/movie_form.html"
    success_url = reverse_lazy("movie_list")


class MovieUpdateView(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = "movies/movie_form.html"
    success_url = reverse_lazy("movie_list")


class MovieDeleteView(DeleteView):
    model = Movie
    template_name = "movies/movie_confirm_delete.html"
    success_url = reverse_lazy("movie_list")


class GenreListView(ListView):
    model = Genre
    template_name = "movies/genre_list.html"
    context_object_name = "genres"


class GenreDetailView(DetailView):
    model = Genre
    template_name = "movies/genre_detail.html"
    context_object_name = "genre"


class GenreCreateView(CreateView):
    model = Genre
    form_class = GenreForm
    template_name = "movies/genre_form.html"
    success_url = reverse_lazy("genre_list")


class GenreUpdateView(UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = "movies/genre_form.html"
    success_url = reverse_lazy("genre_list")


class GenreDeleteView(DeleteView):
    model = Genre
    template_name = "movies/genre_confirm_delete.html"
    success_url = reverse_lazy("genre_list")