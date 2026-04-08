from django import forms
from django.core.exceptions import ValidationError
from .models import Movie, Genre, Platform


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "title",
            "description",
            "release_date",
            "producer",
            "genre",
            "platforms",
            "status",
            "rating",
        ]

    def clean_title(self):
        title = self.cleaned_data["title"]

        if "test" in title.lower():
            raise ValidationError("Tytuł filmu nie może zawierać słowa 'test'.")

        return title


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]


class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = ["name"]