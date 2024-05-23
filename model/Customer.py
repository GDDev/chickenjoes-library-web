from datetime import datetime

class Customer:
    # inside code, cpf, username, user type, name, birth date, sign-up date, last access, list of e-mails, list of phone numbers, list with the fines
    emails = []
    numbers = []
    fines = []
    
    def __init__(self, inside_code, cpf, username, name, birth_date, signup_date = datetime.now(), last_access = datetime.now(), user_type = 'customer'):
        self.inside_code = inside_code
        self.cpf = cpf
        self.username = username
        self.user_type = user_type
        self.name = name
        self.birth_date = birth_date
        self.signup_date = signup_date
        self.last_access = last_access

