class Devolution:
    # status, devolution date, check-out id, list of returned book
    returned_books = []

    def __init__(self, status, devolution_date, checkout_id):
        self.status = status
        self.devolution_date = devolution_date
        self.checkout_id = checkout_id

    def add_book_to_returned_books(self, book):
        self.returned_books.append(book)

    def remove_book_from_returned_books(self, book):
        self.returned_books.remove(book)
