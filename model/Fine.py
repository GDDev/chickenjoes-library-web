from datetime import datetime

class Fine:
    def __init__(self, amount, fine_emition_date = datetime.now(), fine_payment_date = None):
        self.amount = amount
        self.fine_emition_date = fine_emition_date
        self.fine_payment_date = fine_payment_date
    