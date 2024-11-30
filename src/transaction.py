import hashlib

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.hash = self.compute_hash()

    def compute_hash(self):
        transaction_string = f"{self.sender}{self.recipient}{self.amount}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def validate(self):
        # Here, you could add logic to verify signatures, etc.
        return self.amount > 0
