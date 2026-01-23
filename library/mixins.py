from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Exists, OuterRef
from django.db.models import Q
from .models import Borrow

class AuthPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    pass

class BookListMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query)
            ).order_by('-title')

        return qs
class BookStatusMixin:

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(
            is_borrowed=Exists(
                Borrow.objects.filter(book=OuterRef('pk'), status='B')
            ),
            return_book=Exists(
                Borrow.objects.filter(book=OuterRef('pk'), user=self.request.user, status='B')
            )
        )

class LoanRecordListMixin:
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'M':
            qs = Borrow.objects.filter(status='B', user=user)
        else:
            qs = Borrow.objects.filter(status='B')
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(
                Q(book__title__icontains=query) |
                Q(user__username__icontains=query) |
                Q(book__isbn__icontains=query)
            ).order_by('-book__title')

        return qs