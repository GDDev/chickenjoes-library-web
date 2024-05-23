class Book:
    # inside code, title, language, publication date, edition date, pages number, size, publisher, edition number, isbn, list of the authors
    authors = []

    def __init__(self, inside_code, title, language, publication_date, edition_date, pages, size, publisher, isbn, edition_number = 'N/A'):
        self.inside_code = inside_code
        self.title = title
        self.language = language
        self.publication_date = publication_date
        self.edition_date = edition_date if edition_date else publication_date
        self.pages = pages
        self.size = size
        self.publisher = publisher
        self.edition_number = edition_number
        self.isbn = isbn

    def add_author_to_book(self, author):
        self.authors.append(author)    
