from bson import ObjectId
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User

import copy

from utils.dbconnect import connect

from .models import UserProfile
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
        
        user = UserProfile(birth_date=birth_date, cpf=cpf, first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.save()

        messages.success(
            self.request,
            'Seu cadastro foi efetuado com sucesso.'
        )

        self.request.session['cart'] = self.cart
        self.request.session.save()
        return redirect('book:listbooks')

class Update(BasePerfil):
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

        UserProfile.login(self.request, user=user)

        messages.success(
            self.request,
            'Seu cadastro foi atualizado com sucesso.'
        )

        self.request.session['cart'] = self.cart
        self.request.session.save()
        return redirect('userprofile:update')

# TODO: Delete User

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

class Logout(View):
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
