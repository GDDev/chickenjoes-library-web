from datetime import datetime

class Booking:
    # status, protocol, booking date, estimated check-out date, customer id, list of booked books
    booked_books = []

    # TODO: calculate the estimated check-out date
    def __init__(self, status, protocol, estimated_checkout_date, customer_id, booking_date = datetime.now()):
        self.status = status
        self.protocol = protocol
        self.booking_date = booking_date
        self.estimated_checkout_date = estimated_checkout_date
        self.customer_id = customer_id

    def add_book_to_booked_books(self, book):
        # TODO: limit the amount of books being booked to 5 per customer
        self.booked_books.append(book)

    def remove_book_from_booked_books(self, book):
        self.booked_books.remove(book)
