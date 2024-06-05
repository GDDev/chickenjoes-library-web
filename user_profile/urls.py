from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('', views.Create.as_view(), name='createuser'),
    # path('updateuser/', views.Update.as_view(), name='updateuser'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]

