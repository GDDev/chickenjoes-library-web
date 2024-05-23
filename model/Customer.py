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

    def add_email_to_emails(self, email):
        self.emails.append(email)

    def remove_email_from_emails(self, email):
        self.emails.remove(email)

    def add_number_to_numbers(self, number):
        self.numbers.append(number)

    def remove_number_from_numbers(self, number):
        self.numbers.remove(number)

    def add_fine_to_fines(self, fine):
        self.fines.append(fine)

    def remove_fine_from_fines(self, fine):
        self.fines.remove(fine)
