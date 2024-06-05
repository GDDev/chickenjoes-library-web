from django import forms
from django.contrib.auth.models import User
from utils.dbconnect import connect

db = connect()

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação da Senha'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'password2', 'email',)

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        username_data = data.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        username_db = db.users.find_one({'username': username_data})
        email_db = db.users.find_one({'email': email_data})

        error_msg_user_exists = 'Usuário já existe.'
        error_msg_email_exists = 'E-mail já está em uso.'
        error_msg_password_match = 'As senhas são diferentes.'
        error_msg_password_short = 'A senha deve ter no mínimo 6 caracteres.'
        error_msg_required_field = 'Este campo é obrigatório.'

        if self.user:
            if username_db:
                if username_data != username_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists
            
            if email_db:
                if email_data != email_db.email:               
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match
                
                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short
        else:
            if username_db:
                validation_error_msgs['username'] = error_msg_user_exists
        
            if email_db:               
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field
            else:
                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short

            if not password2_data:
                validation_error_msgs['password2'] = error_msg_required_field

            if password_data != password2_data:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password2'] = error_msg_password_match

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))
