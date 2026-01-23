from django.urls import path
from .views import *

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='edit-book'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='delete-book'),
    path('books/create/', BookCreateView.as_view(), name='add-book'),
    path('books/loans/', LoanRecordListView.as_view(), name='loan-list'),
    path('books/detail/<int:pk>/borrow/create/', BorrowCreateView.as_view(), name='add-borrow'),
    path('books/borrow/<int:pk>/edit/', LoanRecordUpdateView.as_view(), name='borrowed-record-edit'),
]