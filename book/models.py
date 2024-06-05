from django.db import models
from utils.dbconnect import connect
from bson.objectid import ObjectId
import os
from PIL import Image
from django.conf import settings
from django.utils.text import slugify

# book_collection = db['Book']
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

class Book:
    def __init__(self, inside_code, title, language, publication_date, pages, size, publisher, isbn, availability=True, edition_date=None, description='Just another book.', edition_number='N/A', authors=[], image=None, slug=None, _id=None):
        self.inside_code = inside_code
        self.availability = availability
        self.title = title
        self.description = description
        self.language = language
        self.publication_date = publication_date
        self.edition_date = edition_date or publication_date
        self.pages = pages
        self.size = size
        self.publisher = publisher
        self.edition_number = edition_number
        self.isbn = isbn
        self.authors = authors or []
        self.image = image
        self.slug = slug or slugify(title)
        self._id = _id or ObjectId()

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

        book_data = {
            '_id': self._id or ObjectId(),
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
        db.books.replace_one({'_id': self._id}, book_data, upsert=True)

    @staticmethod
    def find_book_by_id(book_id):
        return db.books.find_one({'_id': book_id})
    
    @staticmethod
    def find_book_by_search(search):
        found_books = [book for book in Book.find_available_books() if search in book['title'] or search in book['isbn']]
        # for book in Book.find_available_books():
        #     if search in book['title'] or search in book['isbn']:
        #         found_books.append(book)
        return found_books

    @staticmethod
    def find_all_books():
        return db.books.find()
    
    @staticmethod
    def find_available_books():
        available_books = [book for book in Book.find_all_books() if book['availability']]
        return available_books
    
    @staticmethod
    def find_exclusive_books():
        available_books = Book.find_available_books()
        one_timer = []
        for book in available_books:
            for one_book in one_timer:
                if book['title'] == one_book['title'] and book['edition_number'] == one_book['edition_number']:
                    one_timer.pop()
            one_timer.append(book)
        return one_timer

    def __str__(self) -> str:
        return self.title
    
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
    def find_books_by_author(author_id):
        return db.book_author_associations.find({'author_id': author_id})

    @staticmethod
    def find_authors_by_book(book_id):
        return db.book_author_associations.find({'book_id': book_id})
