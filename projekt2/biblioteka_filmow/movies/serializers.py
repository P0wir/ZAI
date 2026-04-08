from rest_framework import serializers
from .models import Movie, Genre, Platform


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ["id", "name"]


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        source="genre",
        write_only=True
    )
    platforms = PlatformSerializer(many=True, read_only=True)
    platform_ids = serializers.PrimaryKeyRelatedField(
        queryset=Platform.objects.all(),
        many=True,
        source="platforms",
        write_only=True,
        required=False
    )

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "imdb_id",
            "description",
            "release_date",
            "producer",
            "genre",
            "genre_id",
            "platforms",
            "platform_ids",
            "status",
            "rating",
            "created_at",
        ]

    def validate_title(self, value):
        if "test" in value.lower():
            raise serializers.ValidationError(
                "Tytuł filmu nie może zawierać słowa 'test'."
            )
        return value

    def validate_rating(self, value):
        if value is not None and (value < 0 or value > 10):
            raise serializers.ValidationError("Ocena musi być w zakresie 0-10.")
        return value