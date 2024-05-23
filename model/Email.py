from datetime import datetime

class Email:
    #e-mail, creation date
    def __init__(self, email, creation_date = datetime.now()):
        self.email = email
        self.creation_date = creation_date
        