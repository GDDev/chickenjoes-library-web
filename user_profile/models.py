from datetime import datetime
from bson import ObjectId
from django.forms import ValidationError
from book.models import Book
from utils.validacpf import valida_cpf
from utils.dbconnect import connect

db = connect()

class UserProfile:
    def create_inside_code(self):
        return f'CUS{datetime.now().year}{datetime.now().timestamp()}'

    def __init__(self, birth_date, cpf, first_name, last_name, username, email, password, inside_code=None, id=None):
        self.inside_code = inside_code or self.create_inside_code()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.user_type ='customer'
        self.birth_date = birth_date
        self.cpf = cpf
        self.id = id or ObjectId()

    @staticmethod
    def fine(user_id, booking_id):
        if not isinstance(user_id, ObjectId): user_id = ObjectId(user_id)
        if not isinstance(booking_id, ObjectId): booking_id = ObjectId(user_id)
        user = db.users.find_one({'_id': user_id})
        if user:
            fine = Fine(user_id, booking_id)
            fine.save()

    @staticmethod      
    def can_user_be_deleted(user_id):
        if not isinstance(user_id, ObjectId): user_id = ObjectId(user_id)
        bookings = list(db.bookings.find({'customer_id': user_id}))
        fines = list(db.fines.find({'customer_id': user_id}))
        error_msgs = []
        for booking in bookings:
            books_ids = list(db.book_in_booking.find({'booking_id': booking['_id']}))
            if booking['status'] == 'reservado':
                books = [db.books.find_one({'_id': book['book_id']}) for book in books_ids]
                for book in books:
                    if book:
                        db.books.update_one({'_id': book['_id']}, {'$set': {'availability': True}})
                db.bookings.delete_one({'_id': booking['_id']})
            elif booking['status'] == 'retirado':
                error_msgs.append('Você possui empréstimos em aberto, impossível deletar conta.')
                return (False, error_msgs)
        for fine in fines:
            if fine['status'] == 'a pagar':
                error_msgs.append('Você possui multas não pagas, impossível deletar conta.')
                return (False, error_msgs)
        return (True, error_msgs)

    def save(self):
        user_data = {
            '_id': self.id,
            'inside_code': self.inside_code,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'birth_date': self.birth_date,
            'cpf': self.cpf,
            'user_type': self.user_type
        }
    
        db.users.replace_one({'_id':self.id}, user_data, upsert=True)

    # TODO: encrypt password
    @staticmethod
    def authenticate_user(username, password):
        return db.users.find_one({'username': username} and {'password': password})

    @staticmethod
    def login(request, user):
        error_messages = {}
        if not request.session.get('logged_user'):
            user['_id'] = str(user.get('_id'))
            request.session['logged_user'] = user
            request.session.save()
        else:
            error_messages['login'] = 'Impossível fazer login. Usuário já logado.'
        if error_messages:
            raise ValidationError(error_messages)
        return request 

    @staticmethod
    def logout(request):
        if request.session.get('logged_user'):
            del request.session['logged_user']
            request.session.save()

    def __str__(self) -> str:
        return f'{self.username}'
        
    def clean(self) -> None:
        error_messages = {}

        sent_cpf = self.cpf or None
        db_cpf = None
        profile = db.users.find_one({'cpf': sent_cpf})

        if profile:
            db_cpf = profile['cpf']

            if db_cpf is not None and self.id != profile['_id']:
                error_messages['cpf'] = 'CPF já registrado.'

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido.'
        if error_messages:
            raise ValidationError(error_messages)
        
class Fine:
    def define_fine_value(self, customer_id):
        fine = 20.0
        if isinstance(customer_id, str):
            customer_id = ObjectId(customer_id)
        previous_fines = len({db.fines.find({'customer_id': customer_id})})
        if previous_fines > 0:
            fine *= previous_fines
        return fine

    def __init__(self, customer_id, booking_id, status='a pagar', created_date=datetime.now(), fine_value=None, _id=None):
        self.customer_id = customer_id
        self.booking_id = booking_id
        self.status = status
        self.created_date = created_date
        self.fine_value = fine_value or self.define_fine_value(self.customer_id)
        self.id = _id or ObjectId()

    def save(self):
        fine = {
            '_id': self.id,
            'customer_id': self.customer_id,
            'booking_id': self.booking_id,
            'status': self.status,
            'created_date': self.created_date,
            'fine_value': self.fine_value,
        }
        db.fines.replace_one({'_id': self.id}, fine, upsert=True)
