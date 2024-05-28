from django.contrib import admin
from .models import Booking, BookBooking

class BookBookingInline(admin.TabularInline):
    model = BookBooking
    extra = 1

class BookingAdmin(admin.ModelAdmin):
    inlines = [BookBookingInline]

admin.site.register(Booking, BookingAdmin)
admin.site.register(BookBooking)
