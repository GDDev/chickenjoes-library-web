from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

class FinishBooking(View):
    def get(self, *args, **kwargs):
        return HttpResponse('BOOKING')

class Detail(View):
    ...
