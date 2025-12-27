from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Book, Borrow
from django.db.models import Exists, OuterRef
from .forms import BookForm


# Create your views here.
class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'library/book_list.html'
    paginate_by = 3
    
    def get_queryset(self):
        queryset = Book.objects.filter(available=True)
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(author__name__icontains=query)).order_by('-title')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Book List',
            'total_books': self.get_queryset().count(),
        })
        return context
    
class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'library/book_detail.html'
    def get_queryset(self):
        return Book.objects.annotate(
            is_borrowed = Exists(
                Borrow.objects.filter(
                    book = OuterRef('pk'),
                    status = 'B',
                )
            )
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'{self.object.title} Detail',
            'is_borrowed': self.object.is_borrowed,
        })
        return context

class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    permission_required = 'library.add_book'
    success_url = reverse_lazy('book-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Add Book',
        })
        return context
    
class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    permission_required = 'library.change_book'
    
    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'{self.object.title} Edit',
        })
        return context
    
class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'library/book_delete.html'
    context_object_name = 'book'
    permission_required = 'library.delete_book'
    success_url = reverse_lazy('book-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'{self.object.title} delete permission',
        })
        return context
    
    
