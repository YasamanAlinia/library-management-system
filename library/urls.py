from django.urls import path
from .views import BookListView, BookDetailView, BookUpdateView, BookDeleteView, BookCreateView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='edit-book'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='delete-book'),
    path('books/create/', BookCreateView.as_view(), name='add-book')
]