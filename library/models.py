from django.db import models
from confg.settings import AUTH_USER_MODEL
import random  


class Category(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        db_table = 'books_categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['-title']

    def __str__(self):
        return self.title
    
class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField()
    birth_date = models.DateField()

    class Meta:
        db_table = 'authors'
        verbose_name = 'author'
        verbose_name_plural = 'authors'
        ordering = ['-name']

    def __str__(self):
        return self.name

def isbn_generator():
    return ''.join(str(random.randint(0, 9)) for _ in range(13))
class Book(models.Model):
    title = models.CharField(max_length=120)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    publish_date = models.DateField()
    available = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'books'
        verbose_name = 'book'
        verbose_name_plural = 'books'
        ordering = ['-publish_date']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.isbn:
            while True:
                isbn = isbn_generator()
                if not Book.objects.filter(isbn=isbn).exists():
                    self.isbn = isbn
                    break
        super().save(*args, **kwargs)
    
class Borrow(models.Model):
    STATUS_CHOICES = (
        ('B', 'Borrowed'),
        ('R', 'Returned'),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrower')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrower')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'books_borrow'
        verbose_name = 'borrow'
        verbose_name_plural = 'borrows'
        ordering = ['created_time']

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
