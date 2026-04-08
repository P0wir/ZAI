from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Movie(models.Model):
    class Status(models.TextChoices):
        TO_WATCH = "to_watch", "Do obejrzenia"
        WATCHING = "watching", "W trakcie"
        WATCHED = "watched", "Obejrzany"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField(blank=True, null=True)
    producer = models.CharField(max_length=150, blank=True)

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="movies",
    )

    platforms = models.ManyToManyField(
        Platform,
        blank=True,
        related_name="movies",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TO_WATCH,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(fields=["title", "release_date"], name="unique_movie_title_release_date")
        ]

    def __str__(self):
        return self.title