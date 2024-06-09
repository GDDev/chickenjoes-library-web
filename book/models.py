from datetime import datetime
import pprint
from utils.dbconnect import connect
from bson.objectid import ObjectId
import os
from PIL import Image
from django.utils.text import slugify

db = connect()

class Author:
    def __init__(self, name, nacionality, education, description, _id=None):
        self.name = name
        self.nacionality = nacionality
        self.education = education
        self.description = description
        self.id = _id or ObjectId()

    def save(self):
        author_data = {
            '_id': self.id,
            'name': self.name,
            'nacionality': self.nacionality,
            'education': self.education,
            'description': self.description,
        }
    
        db.authors.replace_one({'_id':self.id}, author_data, upsert=True)

    def __str__(self) -> str:
        return self.name

class SuggestedAuthor(Author):
    def __init__(self, name, nacionality, education, description, _id=None):
        super().__init__(name, nacionality, education, description, _id)

    def save(self):
        author_data = {
            '_id': self.id,
            'name': self.name,
            'nacionality': self.nacionality,
            'education': self.education,
            'description': self.description,
        }
    
        db.suggested_authors.replace_one({'_id':self.id}, author_data, upsert=True)

class Book:
    @staticmethod
    def create_inside_code(isbn):
        return f'LIV{datetime.now().year}{isbn}{datetime.now().timestamp()}'

    def __init__(self, title, language, publication_date, pages, size, publisher, isbn, inside_code=None, availability=True, edition_date=None, description=None, edition_number=None, image=None, slug=None, _id=None):
        self.inside_code = inside_code or self.create_inside_code(isbn)
        self.availability = availability
        self.title = title
        self.description = description or 'Just another book.'
        self.language = language
        self.publication_date = publication_date
        self.edition_date = edition_date or publication_date
        self.pages = pages
        self.size = size
        self.publisher = publisher
        self.edition_number = edition_number or 'N/A'
        self.isbn = isbn
        self.image = image
        self.slug = slug or slugify(inside_code) if inside_code else slugify(self.create_inside_code(isbn))
        self.id = _id or ObjectId()

    def __eq__(self, other):
        return self.title == other.title and self.edition_number == other.edition_number and self.isbn == other.isbn if isinstance(other, Book) else False
    
    def __hash__(self):
        return hash((self.title, self.edition_number, self.isbn))

    @staticmethod
    def resize_image(img_path, new_height):
        img_pil = Image.open(img_path)
        original_width, original_height = img_pil.size

        if original_height > new_height:
            new_width = round((new_height * original_width) / original_height)
            img_pil.resize((new_width, new_height), Image).save(img_path, optimize=True, quality=50)
        else:
            img_pil.close()


    def save(self):
        if self.image:
            img_path = os.path.join('media', self.image)
            self.resize_image(img_path, 150)

        if isinstance(self.id, str):
            self.id = ObjectId(self.id)

        book_data = {
            '_id': self.id,
            'inside_code': self.inside_code,
            'availability': self.availability,
            'title': self.title,
            'description': self.description,
            'language': self.language,
            'publication_date': self.publication_date,
            'edition_date': self.edition_date,
            'pages': self.pages,
            'size': self.size,
            'publisher': self.publisher,
            'edition_number': self.edition_number,
            'isbn': self.isbn,  
            'image': self.image,
            'slug': self.slug,
        }
        db.books.replace_one({'_id': self.id}, book_data, upsert=True)
    
    @staticmethod
    def find_book_by_search(search):
        found_books = [book for book in Book.find_available_books() if search in book.title or search in book.isbn]
        return found_books

    @staticmethod
    def find_all_books():
        return list([
            Book(
                title=book['title'], 
                language=book['language'], 
                publication_date=book['publication_date'], 
                pages=book['pages'], 
                size=book['size'], 
                publisher=book['publisher'], 
                isbn=book['isbn'], 
                inside_code=book['inside_code'], 
                availability=book['availability'], 
                edition_date=book['edition_date'], 
                description=book['description'], 
                edition_number=book['edition_number'], 
                slug=book['slug'], 
                _id=book['_id']
            ) for book in db.books.find()
        ])
    
    @staticmethod
    def find_available_books():
        available_books = [book for book in Book.find_all_books() if book.availability]
        return available_books
    
    @staticmethod
    def find_exclusive_books():
        available_books = Book.find_available_books()
        one_timer = list(set(available_books))
        return sorted(one_timer, key=lambda book: (book.title.lower(), book.edition_number))

    def __str__(self) -> str:
        return self.title
    
class SuggestedBook(Book):
    def __init__(self, title, language, publication_date, pages, size, publisher, isbn, inside_code=None, availability=True, edition_date=None, description=None, edition_number=None, image=None, slug=None, _id=None):
        super().__init__(title, language, publication_date, pages, size, publisher, isbn, inside_code, availability, edition_date, description, edition_number, image, slug, _id)

    def save(self):
        if self.image:
            img_path = os.path.join('media', self.image)
            self.resize_image(img_path, 150)

        book_data = {
            '_id': self.id,
            'inside_code': self.inside_code,
            'availability': self.availability,
            'title': f'(Suggested) {self.title}',
            'description': self.description,
            'language': self.language,
            'publication_date': self.publication_date,
            'edition_date': self.edition_date,
            'pages': self.pages,
            'size': self.size,
            'publisher': self.publisher,
            'edition_number': self.edition_number,
            'isbn': self.isbn,  
            'image': self.image,
            'slug': self.slug,
        }
        db.suggested_books.replace_one({'_id': self.id}, book_data, upsert=True)
    
class BookAuthorAssociation:
    def __init__(self, book_id, author_id, _id=None):
        self.book_id = book_id
        self.author_id = author_id
        self._id = _id or ObjectId()

    def save(self):
        association_data = {
            '_id': self._id,
            'book_id': self.book_id,
            'author_id': self.author_id,
        }
        db.book_author_associations.replace_one({'_id': self._id}, association_data, upsert=True)

    @staticmethod
    def find_books_by_author(author_id, show_suggested):
        if isinstance(author_id, str): author_id = ObjectId(author_id)
        return list(db.suggested_book_author_associations.find({'author_id': author_id})) if show_suggested else list(db.book_author_associations.find({'author_id': author_id}))

    @staticmethod
    def find_authors_by_book(book_id):
        return db.book_author_associations.find({'book_id': book_id})
    
class SuggestedBookAuthorAssociation(BookAuthorAssociation):
    def __init__(self, book_id, author_id, _id=None):
        super().__init__(book_id, author_id, _id)

    def save(self):
        association_data = {
            '_id': self._id,
            'book_id': self.book_id,
            'author_id': self.author_id,
        }
        db.suggested_book_author_associations.replace_one({'_id': self._id}, association_data, upsert=True)
