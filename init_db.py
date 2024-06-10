# FILE GENERATED WITH CHATGPT

from pymongo import MongoClient
from datetime import date, datetime
from book.models import Author, Book
from utils.dbconnect import connect
from bson import ObjectId
import random

def init_db():
    db = connect()

    # Dummy data for books and authors
    # Since some fields are generated automatically, have to create Objects

    authors, books = [], []

    for i in range(0, 5):
        authors.append(
            Author(
                name=f'Autor #{i+1}', 
                nacionality='Brasileiro', 
                education='PHD em Escrever', 
                description=f'Autor #{i+1} é um ótimo autor.'
            )
        )

    for i in range(0, 10):
        rand_year = random.randrange(2000, 2025)
        rand_month = random.randrange(1, 13)
        rand_day = random.randrange(1, 28)
        books.append(
            Book(
                title=f'Livro #{i+1}', 
                language='Pt-Br', 
                publication_date=f'{date(rand_year, rand_month, rand_day)}', 
                pages=random.randrange(50, 1000), 
                size='12 x 19', 
                publisher='Super Editora', 
                isbn=f'{random.randrange(11111111111, 100000000000)}', 
                description=f'Livro #{i+1} é um ótimo livro.', 
                edition_number=random.randrange(1, 30)
            )
        )

    authors = [
        {
            "name": author.name, 
            "nacionality": author.nacionality, 
            "education": author.education, 
            "description": author.description
        } for author in authors
    ]

    books = [ 
        {
            "inside_code": book.inside_code,
            "availability": book.availability, 
            "title": book.title,
            "description": book.description,
            "language": book.language,
            "publication_date": book.publication_date,
            "edition_date": book.edition_date,
            "pages": book.pages,
            "size": book.size,
            "publisher": book.publisher,
            "edition_number": book.edition_number,
            "isbn": book.isbn,
            "image": book.image,
            "slug": book.slug
        } for book in books
    ]

    author_ids = db.authors.insert_many(authors).inserted_ids
    books_ids = db.books.insert_many(books).inserted_ids

    associations = []
    for book_id in books_ids:
        choosen_authors = random.choices(author_ids, k=random.randrange(1, 6))

        for author_id in choosen_authors:
            if not isinstance(book_id, ObjectId): ObjectId(book_id)
            if not isinstance(author_id, ObjectId): ObjectId(author_id)
            add_author = {
                "book_id": book_id,
                "author_id": author_id
            }
            if add_author not in associations:
                associations.append(add_author)

    db.book_author_associations.insert_many(associations)


if __name__ == "__main__":
    init_db()
