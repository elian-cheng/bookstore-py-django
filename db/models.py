from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime

# Create your models here.


# Custom Manager for the new User model
# Built-in Django User model has a UserManager class that provides helper functions
# to create and manage users.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Custom User Model
# Let's redesign the Author model into a User Model
# with an additional field, pen_name, and add authentication via email instead of the username.
# We can remove all other fields like first_name and last_name, as they are inherited
# from the AbstractUser model.
class Author(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20, default="")
    username = models.CharField(max_length=20, default="")
    pen_name = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# class Author(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     pen_name = models.CharField(max_length=100)

#     def __str__(self):
#         if self.pen_name:
#             return f"Author {self.pk}: {self.pen_name}"
#         else:
#             return f"Author {self.pk}: {self.first_name} {self.last_name}"

#     class Meta:
#         verbose_name = "Author"
#         verbose_name_plural = "Authors"
#         permissions = (
#             ("can_edit_author", "Can edit author details"),
#             ("can_delete_author", "Can delete author"),
#         )
#         # Suppose you want to ensure that the author's age is always greater than 18.
#         constraints = [CheckConstraint(check=Q(age__gt=18), name="age_greater_than_18")]


class Genre(models.Model):
    format = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Literary genre {self.id}: {self.format}"

    class Meta:
        db_table = "genre_table"
        ordering = ["format"]
        verbose_name_plural = "Genres"


class Book(models.Model):
    COVER_CHOICES = [
        ("H", "Hard"),
        ("S", "Soft"),
    ]
    title = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover = models.CharField(max_length=1, choices=COVER_CHOICES)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, default="")
    authors = models.ManyToManyField(Author)
    publication_date = models.DateField(default="2021-01-01")

    def __str__(self):
        return f"Book {self.id}: {self.title}"

    class Meta:
        # unique_together = ("title", "author")
        get_latest_by = "publication_date"
        constraints = [
            UniqueConstraint(
                fields=["title", "genre"], name="unique_book_titles_per_genre"
            )
        ]


# In this example, the UniqueConstraint ensures that no two books in the same genre have the same title.
# In the Book model, unique_together ensures that no two books have the same title and author.
# get_latest_by makes it easy to retrieve the most recently published book.
