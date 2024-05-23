from datetime import datetime

class Phone:
    # phone number, creation date
    def __init__(self, number, creation_date = datetime.now()) -> None:
        self.number = number
        self.creation_date = creation_date
