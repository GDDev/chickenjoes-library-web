from django.db import models
from django.contrib.auth.models import User
from book.models import Book

class Booking(models.Model):
    status = models.CharField(
        default='BOOKED',
        max_length=50,
        choices=(
            ('BOOKED', 'reservado'),
            ('CHECKEDOUT', 'retirado'),
            ('RETURNED', 'devolvido'),
            ('CANCELED', 'cancelado'),
            ('EXPIRED', 'expirado'),
        )
    )
    protocol = models.CharField(max_length=2000)
    booking_date = models.DateTimeField()
    estimated_checkout_date = models.DateTimeField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.protocol

class BookBooking(models.Model):
    booking = models.ForeignKey(Booking, related_name='books', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='bookings', on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return f'{self.book.title} em {self.booking}'
