from datetime import datetime

from .Author import Author
from .Book import Book
from .Customer import Customer

# Class to manage the Library itself
class Library:
    # list of customers?, list of employees?, list of books, list of authors, list of bookings?, list of check-outs?, list of returnings?, stock
    customers = []
    books = []
    bookings = []
    checkouts = []
    devolutions = []

    def __init__(self):
        # TODO: get all info from DB
        pass

    def generate_new_inside_code_for_author(self):
        pass

    def validate_new_book_code(self, new_code):
        pass

    def generate_new_inside_code_for_book(self):
        pass

    def validate_new_customer_code(self, new_code):
        while True:
            for customer in self.customers:
                if new_code == customer.inside_code:
                    new_code += str(1)
                else:
                    return True

    def generate_new_inside_code_for_customer(self):
        code = f'CUS{datetime.now().year}{(datetime.now().timestamp())}'
        return code

    # Defines a function to create an author
    def create_author(self, name, nacionality, education, description):
        author = Author(name, nacionality, education, description)
        # TODO: deal with DB insertion
        return author

    # Defines a function to get all existing authors
    def get_all_authors(self):
        all_authors = []
        for book in self.books:
            for author in book.authors:
                if author not in all_authors: all_authors.append(author)
        return all_authors

    # Defines a function to find all authors by a name
    def find_authors_by_name(self, name):
        found_authors = []
        authors = self.get_all_authors()
        for author in authors:
            if name == author.name: found_authors.append(author)
        return found_authors
    
    # Defines a funtion to delete an author
    def delete_author(self, author):
        for book in self.books:
            if book.author == author: book.remove_author_from_book(author)

    # Defines a function to validate if the authors passed thru args are legit
    def validate_authors_in_args(self, authors):
        if authors != ():
            for author in authors:
                if not isinstance(author, Author): return False
            return True
        return False

    # Defines a funtion to create a book
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

    # Defines a funtion to delete a book
    def delete_book(self, book):
        # TODO: deal with DB
        self.books.remove(book)

    def check_customer_open_bookings(self, customer):
        pass

    def check_customer_open_checkouts(self, customer):
        pass

    def check_customer_unpaid_fines(self, customer):
        pass

    def check_if_customer_can_be_deleted(self, customer):
        return self.check_customer_open_bookings(customer) and self.check_customer_open_checkouts(customer) and self.check_customer_unpaid_fines(customer)

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

    # Defines a function to create a new customer
    def create_customer(self, cpf, username, name, birth_date):
        inside_code = self.generate_new_inside_code_for_customer()
        customer = Customer(inside_code, cpf, username, name, birth_date)
        self.customers.append(customer)

    def delete_customer(self, customer):
        if self.check_if_customer_can_be_deleted(customer): self.customers.remove(customer)
    