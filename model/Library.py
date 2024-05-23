class Library:
    # list of customers?, list of employees?, list of books, list of authors, list of bookings?, list of check-outs?, list of returnings?, stock
    customers = []
    books = []
    authors = []
    bookings = []
    checkouts = []
    devolutions = []

    def create_customer(self, customer):
        self.customers.append(customer)
    def delete_customer(self, customer):
        self.customers.remove(customer)

    def create_book(self, book):
        self.books.append(book)
    def delete_book(self, book):
        self.books.remove(book)

    def create_author(self, author):
        self.authors.append(author)
    def delete_author(self, author):
        self.authors.remove(author)

    def create_booking(self, booking):
        self.bookings.append(booking)
    def delete_booking(self, booking):
        self.bookings.remove(booking)

    def create_checkout(self, checkout):
        self.checkouts.append(checkout)
    def delete_checkout(self, checkout):
        self.checkouts.remove(checkout)
    
    def create_devolution(self, devolution):
        self.devolutions.append(devolution)
    def delete_devolution(self, devolution):
        self.devolutions.remove(devolution)
    