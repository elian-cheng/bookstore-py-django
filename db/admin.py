from django.contrib import admin

from db.models import Genre, Author, Book

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
