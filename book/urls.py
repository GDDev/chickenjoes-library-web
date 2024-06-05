from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    path('', views.ListBooks.as_view(), name='listbooks'),
    path('addtocart/', views.AddToCart.as_view(), name="addtocart"),
    path('removefromcart/', views.RemoveFromCart.as_view(), name="removefromcart"),
    path('cart/', views.Cart.as_view(), name="cart"),
    path('<slug>/', views.DetailBook.as_view(), name="detail"),
]
