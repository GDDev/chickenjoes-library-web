from datetime import datetime

from .Book import Book
from .Status import *

class Booking:
    # status, protocol, booking date, estimated check-out date, customer id, list of booked books
    booked_books = []

    # TODO: calculate the estimated check-out date
    def __init__(self, status, protocol, estimated_checkout_date, customer, booking_date = datetime.now()):
        self.status = validate_status_enum(status)
        self.protocol = protocol
        self.booking_date = booking_date
        self.estimated_checkout_date = estimated_checkout_date
        self.customer = customer

    def verify_customers_book_limit(self, customer):
        total_books = 0
        for booking in customer.bookings:
            if booking.status == Status.BOOKED: total_books += len(booking.booked_books)
        for checkout in customer.checkouts:
            if checkout.status == Status.CHECKEDOUT: total_books += len(checkout.checkedout_books)
        return True if total_books < 5 else False

    def add_book_to_booked_books(self, book):
        if isinstance(book, Book) and self.verify_customers_book_limit(self.customer):
            self.booked_books.append(book)

    def remove_book_from_booked_books(self, book):
        if book in self.booked_books: self.booked_books.remove(book)
