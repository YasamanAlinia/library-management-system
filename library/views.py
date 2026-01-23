from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Book, Borrow
from django.db.models import Exists, OuterRef
from django.db import transaction
from .forms import BookForm, BorrowForm, BorrowMemberForm


# Create your views here.
class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'library/book_list.html'
    paginate_by = 3
    
    def get_queryset(self):
        queryset = Book.objects.all()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query)
            ).order_by('-title')

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
            ),
            user_has_borrowed = Exists(
                Borrow.objects.filter(
                    book = OuterRef('pk'),
                    user = self.request.user,
                    status = 'B',
                )
            ) 
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'{self.object.title} Detail',
            'is_borrowed': self.object.is_borrowed,
            'return_book': self.object.return_book,
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

class LoanRecordListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Borrow
    context_object_name = 'records'
    template_name = 'library/loan_list.html'
    permission_required = 'view_borrow'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'M':
            queryset = Borrow.objects.filter(status='B', user=user)
        else:
            queryset = Borrow.objects.filter(status='B')
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(book__title__icontains=query) |
                Q(user__username__icontains=query) |
                Q(book__isbn__icontains=query)
            ).order_by('-book__title')

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'borrow records list',
        })
        return context

class BorrowCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Borrow
    fields = ()
    template_name = 'library/loan_form.html'
    permission_required = 'add_borrow'

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.book = self.book
            form.instance.user = self.request.user
            form.instance.mark_borrow()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.book.pk})
    
class LoanRecordUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Borrow
    template_name = 'library/loan_form.html'
    permission_required = 'change_borrow'
    success_url = reverse_lazy('loan-list')
    
    def get_form_class(self):
        if self.request.user.role == 'M':
            return BorrowMemberForm
        return BorrowForm
    
    def form_valid(self, form):
        with transaction.atomic():
            if form.instance.status == 'R':
                form.instance.mark_returned()
            return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'{self.object.book.title} status update'
        })
        return context