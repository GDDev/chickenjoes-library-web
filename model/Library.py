from .Author import Author
from .Book import Book

class Library:
    # list of customers?, list of employees?, list of books, list of authors, list of bookings?, list of check-outs?, list of returnings?, stock
    customers = []
    books = []
    authors = []
    bookings = []
    checkouts = []
    devolutions = []

    def __init__(self):
        # TODO: get all info from DB
        pass

    def create_author(self, name, nacionality, education, description):
        author = Author(name, nacionality, education, description)
        # TODO: deal with DB insertion
        self.authors.append(author)

        return author

    def find_authors_by_name(self, name):
        found_authors = []
        for author in self.authors:
            if name == author.name: found_authors.append(author)
        return found_authors
    
    def delete_author(self, author):
        self.authors.remove(author)

    def validate_authors_in_args(self, authors):
        if authors != ():
            for author in authors:
                if not isinstance(author, Author): return False
            return True
        return False

    def create_book(self, inside_code, title, language, publication_date, edition_date, pages, size, publisher, isbn, edition_number, *args):
        authors = args
        if self.validate_authors_in_args(authors):
            book = Book(inside_code, title, language, publication_date, edition_date, pages, size, publisher, isbn, edition_number)
            for author in authors:
                book.add_author_to_book(author)
            # TODO: deal with DB insertion
            self.books.append(book)
            return book
        elif args == ():
            print('Você precisa inserir pelo menos um autor para o livro.')
        else:
            print('Você deve informar um objeto Autor')
            return None

    def delete_book(self, book):
        self.books.remove(book)

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

    def create_customer(self, customer):
        self.customers.append(customer)
    def delete_customer(self, customer):
        self.customers.remove(customer)
    