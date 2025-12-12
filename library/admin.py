from django.contrib import admin
from django.contrib.admin import register
from .models import Category, Book, Author, Borrow


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    
@register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'birth_date',
    )
    search_fields = ('name',)

@register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'author',
        'publish_date',
        'available',
    )
    search_fields = (
        'title',
        'category',
        'author',
        'isbn',
    )

@register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'user',
        'status',
    )
    search_fields = ('book',)