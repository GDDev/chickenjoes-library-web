import pprint
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages

from booking.models import Booking
from .models import Book, Author, BookAuthorAssociation, SuggestedBook, SuggestedBookAuthorAssociation
from booking.views import DispatchLoginRequiredMixin
from bson.objectid import ObjectId

from utils.dbconnect import connect
db = connect()

class ListBooks(View):
    template_name = 'book/listbooks.html'
    context_object_name = 'books'

    def get(self, *args, **kwargs):
        books = []
        authors = []        
        show_suggested = self.request.GET.get('show_suggested') == 'true'        
        filters = self.request.GET.getlist('filter_by_author')
        search = self.request.GET.get('search')
        books_data = Book.find_exclusive_books()
        if show_suggested:
            books_data = list(db.suggested_books.find())

        authors = [
            Author(
                name=author['name'], 
                nacionality=author['nacionality'], 
                education=author['education'], 
                description=author['description'], 
                _id=author['_id']
            ) for author in db.authors.find()
        ]

        if filters:
            for filter in filters:
                books_data = [db.books.find_one({'_id': assoc['book_id']}) for assoc in BookAuthorAssociation.find_books_by_author(filter, show_suggested)]
            filters = []
        elif search:
            books_data = Book.find_book_by_search(search)
            search = ''

        books = books_data

        # for book in books_data:
        #     if book:
        #         books.append(
        #             Book(
        #             inside_code=book['inside_code'],
        #             availability=book['availability'],
        #             title=book['title'],
        #             description=book['description'],
        #             language=book['language'],
        #             publication_date=book['publication_date'],
        #             edition_date=book['edition_date'],
        #             pages=book['pages'],
        #             size=book['size'],
        #             publisher=book['publisher'],
        #             edition_number=book['edition_number'],
        #             isbn=book['isbn'],
        #             slug=book['slug'],
        #             _id=book['_id']
        #             )
        #         )

        context = {
            self.context_object_name: books,
            'authors': authors,
            'show_suggested': show_suggested,
            'filters': filters,
            'search': search,
        }
        return render(self.request, self.template_name, context)

class DetailBook(View):
    template_name = 'book/detail.html'
    context_object_name = 'book'
    slug_url_kwarg = 'slug'

    def get(self, request, slug):
        book_data = db.books.find_one({'slug': slug})
        book_is_suggestion = False 
        if not book_data:
            book_data = db.suggested_books.find_one({'slug': slug})
            book_is_suggestion = True
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
                slug=book_data['slug'],
                _id=book_data['_id']
            )

            if isinstance(book.id, str): book.id = ObjectId(book.id)

            authors = list(db.book_author_associations.find({'book_id': book.id})) or list(db.suggested_book_author_associations.find({'book_id': book.id}))
            authors = [db.authors.find_one({'_id': author['author_id']}) for author in authors]

            context = {
                'book': book,
                'authors': authors,
                'book_is_suggestion': book_is_suggestion
            }

            return render(request, 'book/detail.html', context)


class AddToCart(View):
    def get(self, *args, **kwargs):
        # http_referer = self.request.META.get('HTTP_REFERER', reverse('book:listbooks'))
        id = self.request.GET.get('id')
        id_obj = ObjectId(id)
        book_data = db.books.find_one({'_id': id_obj})
        if not id or not book_data:
            messages.error(
                self.request,
                f'Livro não encontrado.{self.request.GET}'
            )
            return redirect('book:listbooks')
        
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

        cart = self.request.session['cart']

        if id in cart:
            messages.warning(
                self.request,
                'Livro já no carrinho.'
            )
            return redirect('book:listbooks')
        
        if self.request.session.get('logged_user'):
            if Booking.get_total_user_books(self.request.session['logged_user']['_id']) + len(cart) >= 5:
                messages.error(
                self.request,
                'Limite máximo de livros atingido.'
                )
                return redirect('book:cart')      
        elif len(cart) >= 5:
            messages.error(
                self.request,
                'Limite máximo de livros atingido.'
            )
            return redirect('book:cart')

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
        return redirect('book:listbooks')

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
    
class SuggestBook(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'book/suggestbook.html')

    def post(self, *args, **kwargs):
        if not self.request.session.get('logged_user'):
            messages.error(
                self.request,
                'Você precisa estar logado para sugerir um livro.'
            )
            return redirect('userprofile:createuser')
        
        title = self.request.POST.get('title')
        description = self.request.POST.get('description')
        language = self.request.POST.get('language')
        publication_date = self.request.POST.get('publication_date')
        edition_date = self.request.POST.get('edition_date')
        pages = self.request.POST.get('pages')
        size = self.request.POST.get('size')
        publisher = self.request.POST.get('publisher')
        edition_number = self.request.POST.get('edition_number')
        isbn = self.request.POST.get('isbn')

        book_data = {
            'title': title,
            'description': description,
            'language': language,
            'publication_date': publication_date,
            'edition_date': edition_date,
            'pages': pages,
            'size': size,
            'publisher': publisher,
            'edition_number': edition_number,
            'isbn': isbn,
        }

        book = SuggestedBook(title=title, language=language, publication_date=publication_date, pages=pages, size=size, publisher=publisher, isbn=isbn, edition_date=edition_date, description=description, edition_number=edition_number)

        self.request.session['suggestion'] = book_data
        self.request.session.save()

        return redirect('book:assocauthor')

class SuggestAuthor(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return redirect('book:listbooks')
    
class AssocAuthor(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        if not self.request.session.get('suggestion'):
            messages.error(
                self.request, 
                'Não é possível associar autores à um livro sem um livro.'
            )
            return redirect('book:suggestbook')
        
        authors = db.authors.find()
        authors = {
            Author(
                _id=author['_id'], 
                name=author['name'], 
                nacionality=author['nacionality'], 
                education=author['education'], 
                description=author['description']
            ) for author in authors
        }
        suggested_authors = db.suggested_authors.find()

        context = {
            'authors': authors,
            'suggested_authors': suggested_authors,
        }

        return render(self.request, 'book/assocauthor.html', context)

class SendSuggestion(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        if not self.request.session.get('suggestion'):
            messages.error(
                self.request, 
                'Não é possível associar autores à um livro sem um livro.'
            )
            return redirect('book:suggestbook')

        if self.request.session.get('assocauthors'):
            book = self.request.session['suggestion']
            
            book = SuggestedBook(
                title=book['title'],
                language=book['language'],
                publication_date=book['publication_date'],
                pages=book['pages'],
                size=book['size'],
                publisher=book['publisher'],
                isbn=book['isbn'],
                edition_date=book['edition_date'],
                description=book['description'],
                edition_number=book['edition_number']
            )
            book.save()

            if book:
                for author in self.request.session['assocauthors']:
                    suggest = SuggestedBookAuthorAssociation(book_id=ObjectId(book.id), author_id=ObjectId(author))
                    suggest.save()

                messages.success(
                    self.request,
                    'Livro recomendado com sucesso.'
                )

                del self.request.session['suggestion']
                del self.request.session['assocauthors']

                return redirect('book:listbooks')

class AddAuthorToList(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        id = self.request.GET.get('select_authors')
        if not id:
            messages.error(
                self.request,
                f'Autor não encontrado.{self.request.GET}'
            )
            return redirect('book:assocauthor')

        id_obj = ObjectId(id)
        data_author = db.authors.find_one({'_id': id_obj}) or db.suggested_authors.find_one({'_id': id_obj})
        if not data_author:
            return redirect('book:assocauthor')

        if not self.request.session.get('assocauthors'):
            self.request.session['assocauthors'] = {}
            self.request.session.save()

        if id in self.request.session['assocauthors']:
            return redirect('book:assocauthor')
        authors = self.request.session['assocauthors']

        authors[id] = {
            'id': str(data_author['_id']),
            'name': data_author['name'],
            'nacionality': data_author['nacionality'],
            'education': data_author['education'],
            'description': data_author['description'],
        }

        self.request.session.save()
        return redirect('book:assocauthor')
    
class RemoveAuthorFromList(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        id = self.request.GET.get('id')
        if not id or not self.request.session.get('assocauthors'):
            return redirect('book:assocauthor')
        if id not in self.request.session['assocauthors']:
            return redirect('book:assocauthor')
        
        del self.request.session['assocauthors'][id]
        self.request.session.save()
        return redirect('book:assocauthor')   
    