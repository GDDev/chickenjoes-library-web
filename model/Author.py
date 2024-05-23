class Author:
    #name, nacionality, education, description, list of book
    books = []

    def __init__(self, name, nacionality, education, description):
        self.name = name
        self.nacionality = nacionality
        self.education = education
        self.description = description

    def add_book_to_author(self, book):
        self.books.append(book)

    def remove_book_from_author(self, book):
        if book in self.books: self.books.remove(book)
