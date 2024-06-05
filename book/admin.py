<<<<<<< HEAD
from django.contrib import admin

# Register your models here.
=======
from django import forms
from django.contrib import admin
from .models import Author, Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'authors': forms.CheckboxSelectMultiple(),
        }

class BookAdmin(admin.ModelAdmin):
    form = BookForm

admin.site.register(Author)
admin.site.register(Book, BookAdmin)
>>>>>>> b68ad8231849ff80a4984ebe22fc11694594f8ec
