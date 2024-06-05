from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
from utils.validacpf import valida_cpf

class UserProfile(models.Model):
    inside_code = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=15, default='customer', editable=False)
    birth_date = models.DateField()
    cpf = models.CharField(max_length=11)
    image = models.ImageField(upload_to='media/users/%Y/%m/', blank=True)

    def __str__(self) -> str:
        return f'{self.user}'
        
    def clean(self) -> None:
        error_messages = {}

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido.'
        if error_messages:
            raise ValidationError(error_messages)
        
    # class Meta:
    #     verbose_name = 'User'
    #     verbose_name_plural = 'Users'
        