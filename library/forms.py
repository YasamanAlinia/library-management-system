from django import forms
from .models import Book, Borrow

class FormStyleMixin:
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (
                f'{classes} custom-input text-secondary border rounded p-2'
            ).strip()
class BookForm(FormStyleMixin, forms.ModelForm ):
    class Meta:
        model = Book
        exclude = (
            'created_time',
            'isbn',
        )
    
        widgets = {
        'publish_date': forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
            ),
        }
    

        
class BorrowForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Borrow
        exclude = ('created_time',)

class BorrowMemberForm(FormStyleMixin, forms.ModelForm):
    
    class Meta:
        model = Borrow
        fields = ('status',)