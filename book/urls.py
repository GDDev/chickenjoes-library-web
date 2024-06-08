from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    path('', views.ListBooks.as_view(), name='listbooks'),
    path('suggestbook/', views.SuggestBook.as_view(), name="suggestbook"),
    path('addauthortolist/', views.AddAuthorToList.as_view(), name="addauthortolist"),
    path('removeauthorfromlist/', views.RemoveAuthorFromList.as_view(), name="removeauthorfromlist"),
    path('suggestauthor/', views.SuggestAuthor.as_view(), name="suggestauthor"),
    path('assocauthor/', views.AssocAuthor.as_view(), name="assocauthor"),
    path('sendsuggestion/', views.SendSuggestion.as_view(), name="sendsuggestion"),
    path('addtocart/', views.AddToCart.as_view(), name="addtocart"),
    path('removefromcart/', views.RemoveFromCart.as_view(), name="removefromcart"),
    path('cart/', views.Cart.as_view(), name="cart"),
    path('<slug>/', views.DetailBook.as_view(), name="detail"),
]
