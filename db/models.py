from django.db import models

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    pen_name = models.CharField(max_length=100)

    def __str__(self):
        if self.pen_name:
            return f"Author {self.pk}: {self.pen_name}"
        else:
            return f"Author {self.pk}: {self.first_name} {self.last_name}"


class Genre(models.Model):
    format = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Literary genre {self.pk}: {self.format}"


# Choices db data type
class Book(models.Model):
    COVER_CHOICES = [("H", "Hard"), ("S", "Soft")]
    title = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    cover = models.CharField(max_length=1, choices=COVER_CHOICES)

    def __str__(self):
        return f"Book {self.pk}: {self.title}"
