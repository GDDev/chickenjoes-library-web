from datetime import datetime

from .Status import Status

class Customer:
    # inside code, cpf, username, user type, name, birth date, sign-up date, last access, list of e-mails, list of phone numbers, list with the fines
    emails = []
    numbers = []
    fines = []

    bookings = []
    checkouts = []
    devolutions = []
    
    def __init__(self, inside_code, cpf, username, name, birth_date, signup_date = datetime.now(), last_access = datetime.now()):
        self.inside_code = inside_code
        self.cpf = cpf
        self.username = username
        self.user_type = 'customer'
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

    def check_customer_open_bookings(self):
        for booking in self.bookings:
            if booking.status == Status.BOOKED: return False
        return True

    def check_customer_open_checkouts(self):
        for checkout in self.checkouts:
            if checkout.status == Status.CHECKEDOUT: return False
        return True

    def check_customer_unpaid_fines(self):
        for fine in self.fines:
            if fine.fine_payment_date == None: return False
        return True

    def check_if_customer_can_be_deleted(self):
        return self.check_customer_open_bookings() and self.check_customer_open_checkouts() and self.check_customer_unpaid_fines()
