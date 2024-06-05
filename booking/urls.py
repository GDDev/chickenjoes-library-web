from django.urls import path
from booking import views

app_name = 'booking'

urlpatterns = [
    path('', views.FinishBooking.as_view(), name='finishbooking'),
    path('detail/', views.Detail.as_view(), name='detail'),
]