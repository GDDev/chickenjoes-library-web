from django.urls import path
from book import views

app_name = 'book'

urlpatterns = [
    path('', views.ListBooks.as_view(), name='index'),
]

