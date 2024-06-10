from bson import ObjectId
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from book.models import Book
from .models import BookBooking, Booking

from utils.dbconnect import connect

db = connect()

class DispatchLoginRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.session.get('logged_user'):
            return redirect('userprofile:createuser')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = super().get_queryset()  # type: ignore
        qs = qs.filter(usuario=self.request.session['logged_user'])
        return qs

class SaveBooking(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.session.get('logged_user')
        if not user:
            messages.error(
                self.request,
                'Você precisa efetuar o login.'
            )
            return redirect('userprofile:login')
        
        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Não há livros para reservar.'
            )
            return redirect('book:listbooks')
        
        cart = self.request.session.get('cart') or {}

        for book in cart.values():
            id = book['book_id']
            out_of_stock = []
            book = db.books.find_one({'_id': ObjectId(id)})
            if book: 
                if not book['availability']:
                    title = book['title']
                    out_of_stock.append(f'Não há mais estoque para o livro: {title}.')
                    del self.request.session['cart'][id]
                    self.request.session.save()

                if out_of_stock:
                    for error in out_of_stock: 
                        messages.error(
                            self.request,
                            error
                        )
                    return redirect('book:cart')

        booking = Booking(ObjectId(user.get('_id')))
        booking.save()

        for book in cart.values():
            BookBooking(booking_id=booking.id, book_id=ObjectId(book['book_id'])).save()
            Book(book['book_title'], book['book_language'], book['book_publication_date'], book['book_pages'], book['book_size'], book['book_publisher'], book['book_isbn'], book['book_inside_code'], False, book['book_edition_date'], book['book_description'], book['book_edition_number'], slug=book['book_slug'], _id=book['book_id']).save()
        
        del self.request.session['cart']
        return redirect('booking:list')

class Detail(DispatchLoginRequiredMixin, View):
    context_object_name = 'booking'
    template_name = 'booking/detail.html'
    pk_url_kwarg = 'id'

    def get(self, request, id):
        data = db.bookings.find_one({'_id': ObjectId(id)})
        if not data:
            return redirect('booking:list')
        else:
            books_ids = db.book_in_booking.find({'booking_id': data['_id']})
            booking = Booking(
                data['customer_id'], 
                data['protocol'], 
                data['estimated_checkout_date'], 
                data['booking_date'], 
                data['checkout_date'], 
                data['estimated_return_date'], 
                data['return_date'], 
                data['status'], 
                data['_id']
            )
            books = [db.books.find_one({'_id': ObjectId(book['book_id'])}) for book in books_ids]

            return render(request, 'booking/detail.html', {'booking': booking, 'books': books})

class CheckOut(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.session.get('logged_user')
        if not user:
            messages.error(
                self.request,
                'Você precisa efetuar o login.'
            )
            return redirect('userprofile:login')
        
        booking_id = self.request.GET.get('booking_id')
        data = db.bookings.find_one({'_id': ObjectId(booking_id)})
        if data:
            booking = Booking(
                data['customer_id'], 
                data['protocol'], 
                data['estimated_checkout_date'], 
                data['booking_date'], 
                data['checkout_date'], 
                data['estimated_return_date'], 
                data['return_date'], 
                data['status'], 
                data['_id']
            )
            booking = booking.checkout()

        return redirect('booking:list')

class Return(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.session.get('logged_user')
        if not user:
            messages.error(
                self.request,
                'Você precisa efetuar o login.'
            )
            return redirect('userprofile:login')
        
        booking_id = self.request.GET.get('booking_id')
        data = db.bookings.find_one({'_id': ObjectId(booking_id)})
        books_ids = db.book_in_booking.find({'booking_id': ObjectId(booking_id)})
        books = [db.books.find_one({'_id': ObjectId(book['book_id'])}) for book in books_ids]
        for book in books:
            if book:
                Book(
                    book['title'], 
                    book['language'], 
                    book['publication_date'], 
                    book['pages'], 
                    book['size'], 
                    book['publisher'], 
                    book['isbn'], 
                    book['inside_code'], 
                    True, 
                    book['edition_date'], 
                    book['description'], 
                    book['edition_number'], 
                    image=book['image'], 
                    slug=book['slug'], 
                    _id=book['_id']
                ).save()
        if data:
            booking = Booking(
                data['customer_id'], 
                data['protocol'], 
                data['estimated_checkout_date'], 
                data['booking_date'], 
                data['checkout_date'], 
                data['estimated_return_date'], 
                data['return_date'], 
                data['status'], 
                data['_id']
            )
            booking = booking.returning(user['_id'])

        return redirect('booking:list')
    
class List(DispatchLoginRequiredMixin, View):
    context_object_name = 'bookings'
    template_name = 'booking/list.html'
    ordering = ['-id']
    
    def get(self, *args, **kwargs):
        data = db.bookings.find({'customer_id': ObjectId(self.request.session['logged_user']['_id'])})
        bookings = []        

        for booking in data:
            bookings.append(
                Booking(
                    booking['customer_id'], 
                    booking['protocol'], 
                    booking['estimated_checkout_date'], 
                    booking['booking_date'], 
                    booking['checkout_date'], 
                    booking['estimated_return_date'], 
                    booking['return_date'], 
                    booking['status'], 
                    booking['_id']
                )
            )

        context = {
            self.context_object_name: bookings,
        }
        return render(self.request, self.template_name, context)
