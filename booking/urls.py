from django.urls import path
from booking import views

app_name = 'booking'

urlpatterns = [
    path('savebooking/', views.SaveBooking.as_view(), name='savebooking'),
    path('checkout/', views.CheckOut.as_view(), name='checkout'),
    path('cancel/', views.CancelBooking.as_view(), name='cancel'),
    path('return/', views.Return.as_view(), name='return'),
    path('list/', views.List.as_view(), name='list'),
    path('detail/<id>', views.Detail.as_view(), name='detail'),
]