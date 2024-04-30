from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from db.models import Genre, Author, Book

admin.site.register(Author, UserAdmin)
admin.site.register(Genre)
admin.site.register(Book)
