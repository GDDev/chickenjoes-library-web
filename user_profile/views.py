from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

class Create(View):
    ...

class Update(View):
    ...

class Delete(View):
    ...
class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LOGIN')
class Logout(View):
    ...
