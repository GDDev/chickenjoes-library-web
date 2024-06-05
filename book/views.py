from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from .models import Book, Author, BookAuthorAssociation
from django.core import serializers
from bson.objectid import ObjectId

import pprint
from django.db.models import Q

from utils.dbconnect import connect
db = connect()

class ListBooks(View):
    template_name = 'book/listbooks.html'
    context_object_name = 'books'

    def get(self, *args, **kwargs):
        books_data = Book.find_exclusive_books()
        books = []
        authors = []        

        for author in db.authors.find():
            authors.append(
                Author(
                    name=author['name'], 
                    nacionality=author['nacionality'], 
                    education=author['education'], 
                    description=author['description'], 
                    _id=author['_id']
                )
            )

        filters = self.request.GET.getlist('filter_by_author')
        search = self.request.GET.get('search')
        if filters:
            books_by_author = []
            for filter in filters:
                for assoc in BookAuthorAssociation.find_books_by_author(filter):
                    books_by_author.append(Book.find_book_by_id(assoc['book_id']))

            books_data = [book for book in books_by_author]
            filters = []
        elif search:
            books_data = Book.find_book_by_search(search)
            search = ''

        for book in books_data:
            books.append(
                Book(
                inside_code=book['inside_code'],
                availability=book['availability'],
                title=book['title'],
                description=book['description'],
                language=book['language'],
                publication_date=book['publication_date'],
                edition_date=book['edition_date'],
                pages=book['pages'],
                size=book['size'],
                publisher=book['publisher'],
                edition_number=book['edition_number'],
                isbn=book['isbn'],
                image=book.get('image'),
                slug=book['slug'],
                _id=book['_id']
                )
            )

        context = {
            self.context_object_name: books,
            'authors': authors,
        }
        return render(self.request, self.template_name, context)

class DetailBook(View):
    template_name = 'book/detail.html'
    context_object_name = 'book'
    slug_url_kwarg = 'slug'

    def get(self, request, slug):
        book_data = db.books.find_one({'slug': slug})
        if not book_data:
            return redirect('book:listbooks')
        else:
            book = Book(
                inside_code=book_data['inside_code'],
                availability=book_data['availability'],
                title=book_data['title'],
                description=book_data['description'],
                language=book_data['language'],
                publication_date=book_data['publication_date'],
                edition_date=book_data['edition_date'],
                pages=book_data['pages'],
                size=book_data['size'],
                publisher=book_data['publisher'],
                edition_number=book_data['edition_number'],
                isbn=book_data['isbn'],
                image=book_data.get('image'),
                slug=book_data['slug'],
                _id=book_data['_id']
            )
            return render(request, 'book/detail.html', {'book': book})


class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('book:listbooks'))
        id = self.request.GET.get('id')
        if not id:
            messages.error(
                self.request,
                f'Livro não encontrado.{self.request.GET}'
            )
            return redirect(http_referer)
        id_obj = ObjectId(id)
        book_data = db.books.find_one({'_id': id_obj})

        if not book_data:
            return redirect(http_referer)
        
        book = Book(
                inside_code=book_data['inside_code'],
                availability=book_data['availability'],
                title=book_data['title'],
                description=book_data['description'],
                language=book_data['language'],
                publication_date=book_data['publication_date'],
                edition_date=book_data['edition_date'],
                pages=book_data['pages'],
                size=book_data['size'],
                publisher=book_data['publisher'],
                edition_number=book_data['edition_number'],
                isbn=book_data['isbn'],
                image=book_data.get('image'),
                slug=book_data['slug'],
                _id=book_data['_id']
            )

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        if id in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart']

        # TODO: Limit user to 5 books
        # if id in cart:
        #     cart_qtt = cart[id]['quantity']
        #     cart_qtt += 1
        # else:
        cart[id] = {
            'book_id': id,
            'book_inside_code': book.inside_code,
            'book_availability': book.availability,
            'book_title': book.title,
            'book_description': book.description,
            'book_language': book.language,
            'book_publication_date': book.publication_date,
            'book_edition_date': book.edition_date,
            'book_pages': book.pages,
            'book_size': book.size,
            'book_publisher': book.publisher,
            'book_edition_number': book.edition_number,
            'book_isbn': book.isbn,
            'book_image': book.image,
            'book_slug': book.slug,
        }

        self.request.session.save()
        pprint.pp(self.request.session.get('cart'))
        print()
        return redirect(http_referer)

class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('book:listbooks'))
        id = self.request.GET.get('id')
        if not id or not self.request.session.get('cart'):
            return redirect(http_referer)
        if id not in self.request.session['cart']:
            return redirect(http_referer)
        
        del self.request.session['cart'][id]
        self.request.session.save()
        return redirect(http_referer)       

class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {})
        }
        return render(self.request, 'book/cart.html', context)
