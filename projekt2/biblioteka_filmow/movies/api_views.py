from datetime import datetime
import requests

from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Movie, Genre
from .serializers import MovieSerializer, GenreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filterset_fields = ["genre", "status"]
    search_fields = ["title", "description", "producer", "imdb_id"]
    ordering_fields = ["title", "release_date", "rating", "created_at"]
    ordering = ["title"]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


def parse_omdb_date(date_str):
    if not date_str or date_str == "N/A":
        return None

    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None


def parse_omdb_rating(value):
    if not value or value == "N/A":
        return None

    try:
        return round(float(value), 1)
    except ValueError:
        return None


@api_view(["POST"])
def import_movie_from_omdb(request):
    title = request.data.get("title")
    imdb_id = request.data.get("imdb_id")

    if not title and not imdb_id:
        return Response(
            {"error": "Podaj 'title' albo 'imdb_id'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not settings.OMDB_API_KEY:
        return Response(
            {"error": "Brak klucza OMDB_API_KEY w settings / zmiennych środowiskowych."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    params = {"apikey": settings.OMDB_API_KEY}

    if imdb_id:
        params["i"] = imdb_id
    else:
        params["t"] = title

    try:
        response = requests.get("https://www.omdbapi.com/", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return Response(
            {"error": f"Błąd połączenia z OMDb: {str(e)}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    if data.get("Response") == "False":
        return Response(
            {"error": data.get("Error", "Nie znaleziono filmu w OMDb.")},
            status=status.HTTP_404_NOT_FOUND,
        )

    genre_name = "Unknown"
    raw_genre = data.get("Genre")
    if raw_genre and raw_genre != "N/A":
        genre_name = raw_genre.split(",")[0].strip()

    genre, _ = Genre.objects.get_or_create(name=genre_name)

    movie, created = Movie.objects.update_or_create(
        imdb_id=data.get("imdbID"),
        defaults={
            "title": data.get("Title", ""),
            "description": data.get("Plot", "") if data.get("Plot") != "N/A" else "",
            "release_date": parse_omdb_date(data.get("Released")),
            "producer": data.get("Director", "") if data.get("Director") != "N/A" else "",
            "genre": genre,
            "rating": parse_omdb_rating(data.get("imdbRating")),
        },
    )

    serializer = MovieSerializer(movie)

    return Response(
        {
            "message": "Film zaimportowany" if created else "Film zaktualizowany",
            "created": created,
            "movie": serializer.data,
        },
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
    )
@api_view(["POST"])
def import_movies_bulk(request):
    query = request.data.get("query")

    if not query:
        return Response(
            {"error": "Podaj 'query' (np. batman)."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not settings.OMDB_API_KEY:
        return Response(
            {"error": "Brak klucza OMDB_API_KEY."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    params = {
        "apikey": settings.OMDB_API_KEY,
        "s": query,
        "page": 1,
    }

    try:
        response = requests.get("https://www.omdbapi.com/", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return Response(
            {"error": f"Błąd połączenia z OMDb: {str(e)}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    if data.get("Response") == "False":
        return Response(
            {"error": data.get("Error")},
            status=status.HTTP_404_NOT_FOUND,
        )

    results = data.get("Search", [])

    created_count = 0
    updated_count = 0

    for item in results:
        imdb_id = item.get("imdbID")

        # pobierz szczegóły filmu
        params_detail = {
            "apikey": settings.OMDB_API_KEY,
            "i": imdb_id,
        }

        try:
            detail_response = requests.get("https://www.omdbapi.com/", params=params_detail, timeout=10)
            detail_data = detail_response.json()
        except:
            continue

        genre_name = "Unknown"
        raw_genre = detail_data.get("Genre")
        if raw_genre and raw_genre != "N/A":
            genre_name = raw_genre.split(",")[0].strip()

        genre, _ = Genre.objects.get_or_create(name=genre_name)

        movie, created = Movie.objects.update_or_create(
            imdb_id=detail_data.get("imdbID"),
            defaults={
                "title": detail_data.get("Title", ""),
                "description": detail_data.get("Plot", "") if detail_data.get("Plot") != "N/A" else "",
                "release_date": parse_omdb_date(detail_data.get("Released")),
                "producer": detail_data.get("Director", "") if detail_data.get("Director") != "N/A" else "",
                "genre": genre,
                "rating": parse_omdb_rating(detail_data.get("imdbRating")),
            },
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

    return Response(
        {
            "message": "Import zakończony",
            "created": created_count,
            "updated": updated_count,
            "total": len(results),
        }
    )