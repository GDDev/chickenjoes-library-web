from bson import ObjectId
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
import copy
from utils.dbconnect import connect
from booking.views import DispatchLoginRequiredMixin
from .models import Fine, UserProfile
from . import forms

db = connect()

class BasePerfil(View):
    template_name = 'user_profile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
    
        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.user = None

        if self.request.session.get('logged_user'):
            self.user = db.users.find_one({'_id': self.request.session['logged_user']})

            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None, instance=self.user)
            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None)
            }
    
        self.userform = self.context['userform']

        if self.request.session.get('logged_user'):
            self.template_name = 'user_profile/update.html'

        self.renderizar = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.renderizar

class Create(BasePerfil):
    def post(self, *args, **kwargs): 
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        confirm_password = self.request.POST.get('confirm_password')
        email = self.request.POST.get('email')
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        cpf = self.request.POST.get('cpf')
        birth_date = self.request.POST.get('birth_date')

        # TODO: encryption
        if not password == confirm_password:
            messages.error(
                self.request,
                'As senhas não são iguais'
            )
            return redirect('userprofile:createuser')
        
        user = UserProfile(
            birth_date=birth_date, 
            cpf=cpf, 
            first_name=first_name, 
            last_name=last_name, 
            username=username, 
            email=email, 
            password=password
        )
        user.save()

        user = UserProfile.authenticate_user(username, password)
        if user:
            UserProfile.login(self.request, user=user)
            messages.success(
                self.request,
                'Seu cadastro foi efetuado com sucesso.'
            )

        self.request.session['cart'] = self.cart
        self.request.session.save()
        return redirect('book:listbooks')

class Update(DispatchLoginRequiredMixin, BasePerfil):
    def post(self, *args, **kwargs):        
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        confirmPassword = self.request.POST.get('confirmPassword')
        email = self.request.POST.get('email')
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')

        if self.request.session.get('logged_user'):
            user = db.users.find_one({'username': username})
            if user:
                if password:
                    if confirmPassword and password == confirmPassword:
                        # TODO: encrypt password
                        user['password'] = password
                    else:
                        return redirect('userprofile:update')
                if confirmPassword and not password:
                    return redirect('userprofile:update')    
                                    
                user['email'] = email
                user['first_name'] = first_name
                user['last_name'] = last_name
                self.request.session['logged_user'] = user
                self.request.session['logged_user']['_id'] = str(user.get('_id'))
                self.request.session.save()

                user = UserProfile(
                    user['inside_code'],
                    user['birth_date'],
                    user['cpf'],
                    first_name,
                    last_name,
                    username,
                    email,
                    user['password'],
                    id=ObjectId(user.get('_id'))                  
                )
                user.save()                

        user = UserProfile.authenticate_user(username, password)
        if user:
            UserProfile.login(self.request, user=user)
            messages.success(
                self.request,
                'Seu cadastro foi atualizado com sucesso.'
            )

        self.request.session['cart'] = self.cart
        self.request.session.save()
        return redirect('userprofile:update')

class Delete(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        if self.request.session.get('logged_user'):
            user = self.request.session['logged_user']['_id']

            (it_can, errors) = UserProfile.can_user_be_deleted(user)
            if errors:
                for error in errors:
                    messages.error(
                        self.request,
                        error
                    )
                return redirect('userprofile:update')
            if it_can:
                if not isinstance(user, ObjectId): user = ObjectId(user)
                db.users.delete_one({'_id': user})
                UserProfile.logout(self.request)
                messages.success(
                    self.request,
                    'Conta deletada com sucesso.'
                )
                
        return redirect('userprofile:createuser')

class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Usuário e Senha são campos obrigatórios.'
            )
            return redirect('userprofile:createuser')
        
        user = UserProfile.authenticate_user(username, password)
        if user:
            UserProfile.login(self.request, user=user)
            messages.success(
                self.request,
                'Login efetuado com sucesso.'
            )
        else:
            messages.error(
                self.request,
                'Usuário ou senha inválidos.'
            )
            return redirect('userprofile:createuser')

        return redirect('book:cart')

class Logout(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        if self.request.session.get('logged_user'):
            if self.request.session.get('cart'):
                cart = copy.deepcopy(self.request.session.get('cart'))
                UserProfile.logout(self.request)
                self.request.session['cart'] = cart
                self.request.session.save()
            else:
                UserProfile.logout(self.request)
        
        return redirect('book:listbooks')

class ListFines(DispatchLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        if self.request.session.get('logged_user'):
            user = self.request.session['logged_user']['_id']
            fines = list(db.fines.find({'customer_id': ObjectId(user)}))
            fines = [
                Fine(
                    _id=fine['_id'], 
                    customer_id=fine['customer_id'], 
                    booking_id=fine['booking_id'], 
                    status=fine['status'],
                    created_date=fine['created_date'], 
                    fine_value=fine['fine_value']
                ) for fine in fines
            ]

        context = {
            'fines': fines
        }
        return render(self.request, 'user_profile/fines.html', context)
