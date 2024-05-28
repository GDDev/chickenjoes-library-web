from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from . import models

class ListBooks(ListView):
    model = models.Book
    template_name = 'book/index.html'
    context_object_name = 'books'
    paginate_by = 20
