from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from .models import Booking, BookBooking

class BookBookingInline(admin.TabularInline):
    model = BookBooking
    extra = 1

class BookingAdmin(admin.ModelAdmin):
    inlines = [BookBookingInline]

admin.site.register(Booking, BookingAdmin)
admin.site.register(BookBooking)
>>>>>>> b68ad8231849ff80a4984ebe22fc11694594f8ec
