import hashlib

class Authenticator:

    def __init__(self):
        self.users = {
            'admin': hashlib.sha256('secret'.encode()).hexdigest(),
            'observer': hashlib.sha256('telescope'.encode()).hexdigest()
        }
    
    def authenticate(self,username,password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        return self.users.get(username) == password_hash