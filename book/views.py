from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models

class ListBooks(ListView):
    model = models.Book
    template_name = 'book/listbooks.html'
    context_object_name = 'books'
    paginate_by = 20

class DetailBook(DetailView):
    model = models.Book
    template_name = 'book/detail.html'
    context_object_name = 'book'
    slug_url_kwarg = 'slug'

class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('book:listbooks'))
        print(self.request)
        id = self.request.GET.get('id')
        if not id:
            messages.error(
                self.request,
                f'Livro não encontrado.{self.request.GET}'
            )
            return redirect(http_referer)
        book = get_object_or_404(models.Book, id=id)

        book_id = book.pk
        book_inside_code = book.inside_code
        book_title = book.title
        book_description = book.description
        book_language = book.language
        book_publication_date = str(book.publication_date)
        book_edition_date = str(book.edition_date)
        book_pages = book.pages
        book_size = book.size
        book_publisher = book.publisher
        book_edition_number = book.edition_number
        book_isbn = book.isbn
        book_authors = book.authors
        book_image = book.image
        book_slug = book.slug

        book_image = book_image.name if book_image else ''

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        # if id in cart:
        #     cart_qtt = cart[id]['quantity']
        #     cart_qtt += 1
        # else:
        cart[id] = {
            'book_id': book_id,
            'book_inside_code': book_inside_code,
            'book_title': book_title,
            'book_description': book_description,
            'book_language': book_language,
            'book_publication_date': book_publication_date,
            'book_edition_date': book_edition_date,
            'book_pages': book_pages,
            'book_size': book_size,
            'book_publisher': book_publisher,
            'book_edition_number': book_edition_number,
            'book_isbn': book_isbn,
            'book_authors': book_authors,
            'book_image': book_image,
            'book_slug': book_slug,
        }

        self.request.session.save()

        # return redirect(http_referer)
        return HttpResponse(self.request.session['cart'])

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
        # contexto = {
        #     'carrinho': self.request.session.get('carrinho', {})
        # }
        # return render(self.request, 'produto/carrinho.html', contexto)
        return HttpResponse(self.request.session['cart'])
