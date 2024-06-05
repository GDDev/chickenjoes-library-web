from django.forms import ValidationError
from utils.validacpf import valida_cpf
from utils.dbconnect import connect

db = connect()

class UserProfile():
    def __init__(self, inside_code, birth_date, cpf, first_name, last_name, username, email, password, image=None, id=None):
        self.inside_code = inside_code
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.user_type ='customer'
        self.birth_date = birth_date
        self.cpf = cpf
        self.image = image
        self.id = id

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
            'image': self.image,
            'user_type': self.user_type
        }
    
        db.users.replace_one({'_id':self.id}, user_data, upsert=True)

    # TODO: encrypt password
    @staticmethod
    def authenticate_user(username, password):
        # print(db.users.find_one({'username': username} and {'password': password}))
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
        
    # class Meta:
    #     verbose_name = 'User'
    #     verbose_name_plural = 'Users'
        