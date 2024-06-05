from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User

import copy

from utils.dbconnect import connect

from . import models
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
        if not self.userform.is_valid():
            messages.error(
                self.request,
                'Campos obrigatórios não preenchidos corretamente.'
            )
            return self.renderizar
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        if self.request.session.get('logged_user'):
            user = db.users.find_one({'username': self.request.POST.get('username')})
            if user:
                user['username'] = username
                if password:
                    # TODO: encrypt password
                    user['password'] = password
                    
                user['email'] = email
                user['first_name'] = first_name
                user['last_name'] = last_name
                user.save()

                # if not self.user_profile:
                #     self.userform.cleaned_data['user'] = user
                #     profile = models.UserProfile(**self.userform.cleaned_data)
                #     profile.save()
                # else:
                #     profile = self.userform.save(commit=False)
                #     profile.user = user
                #     profile.save()
            
        else:
            user = self.userform.save(commit=False)
            User.set_password(user, password)
            user.save()

            profile = self.userform.save(commit=False)
            profile.usuario = user
            profile.save()

        if password:
            authenticated = models.UserProfile.authenticate_user(username=username, password=password)
            
            if authenticated:
                models.UserProfile.login(self.request, user=user)

        messages.success(
            self.request,
            'Seu cadastro foi criado/atualizado com sucesso.'
        )

        self.request.session['cart'] = self.cart
        self.request.session.save()
        return redirect('user_profile:createuser')

# class Atualizar(View):
#     ...

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
        
        user = models.UserProfile.authenticate_user(username, password)
        if user:
            print(user)
            models.UserProfile.login(self.request, user=user)
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
                models.UserProfile.logout(self.request)
                self.request.session['cart'] = cart
                self.request.session.save()
            else:
                models.UserProfile.logout(self.request)
        
        return redirect('book:listbooks')
