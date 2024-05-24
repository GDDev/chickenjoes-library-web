from .Status import validate_status_enum

class CheckOut:
    # status, check-out date, estimated devolution date, booking id, list of checked-out books

    checkedout_books = []

    # TODO: calculate the estimated devolution date based on the amount of books checked-out, their pages and an average of 3 min reading per page
    def __init__(self, status, checkout_date, estimated_devolution_date, booking_id):
        self.status = validate_status_enum(status)
        self.checkout_date = checkout_date
        self.estimated_devolution_date = estimated_devolution_date
        self.booking_id = booking_id

    def add_book_to_checkedout_books(self, book):
        self.checkedout_books.append(book)

    def remove_book_from_checkedout_books(self, book):
        self.checkedout_books.remove(book)
    