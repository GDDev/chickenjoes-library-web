from datetime import datetime, timedelta

from bson import ObjectId
from utils.dbconnect import connect

db = connect()
class Booking:
    def create_protocol(self):
        return f'EMP{datetime.now().timestamp()}AT{datetime.now().year}{datetime.now().day}'
    
    def create_estimated_checkout_date(self):
        return self.booking_date + timedelta(days=7)

    def __init__(self, customer_id, protocol=None, estimated_checkout_date=None, booking_date=datetime.now(), checkout_date=None, estimated_return_date=None, return_date=None, status='reservado', _id=None):
        self.customer_id = customer_id
        # TODO: auto-generate protocol
        self.protocol = protocol or self.create_protocol()
        self.status = status
        self.booking_date = booking_date
        self.estimated_checkout_date = estimated_checkout_date or self.create_estimated_checkout_date()
        self.checkout_date = checkout_date
        self.estimated_return_date = estimated_return_date
        self.return_date = return_date
        self.id = _id or ObjectId()

    def save(self):
        booking_data = {
            '_id': self.id,
            'customer_id': self.customer_id,
            'protocol': self.protocol,
            'status': self.status,
            'booking_date': self.booking_date,
            'estimated_checkout_date': self.estimated_checkout_date,
            'checkout_date': self.checkout_date,
            'estimated_return_date': self.estimated_return_date,
            'return_date': self.return_date,
        }
        db.bookings.replace_one({'_id': self.id}, booking_data, upsert=True)

    @staticmethod
    def get_total_user_books(user_id):
        bookings = db.bookings.find({'status': 'reservado'} or {'status': 'retirado'} and {'customer_id': user_id})
        total = 0
        for booking in bookings:
            books = db.book_in_booking.find({'booking_id': booking.get('_id')}) or []
            for book in books:
                total += 1
        return total

    def __str__(self) -> str:
        return self.protocol

class BookBooking:
    def __init__(self, booking_id, book_id, _id=None):
        self.booking_id = booking_id
        self.book_id = book_id
        self.id = _id or ObjectId()

    def save(self):
        book_booking = {
            '_id': self.id,
            'booking_id': self.booking_id,
            'book_id': self.book_id
        }

        db.book_in_booking.replace_one({'_id':self.id}, book_booking, upsert=True)

    def __str__(self) -> str:
        return f'{self.id}'
