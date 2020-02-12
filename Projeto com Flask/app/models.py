from app import app, db
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    username = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(128))
    # Relacionamento com a tabela Contato
    contacts = db.relationship("Contact", back_populates='user')

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self._authenticated = False
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Contact(db.Model):
    # Chave primária apenas criada para a aplicação não dar erro
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    contact_name = db.Column(db.String(40), nullable=False)
    contact_number = db.Column(db.String(40), nullable=False)
    foreign_key = db.Column(db.String(80), db.ForeignKey(User.username))
    # Relacionamento com a tabela User
    user = db.relationship("User", back_populates="contacts")

    def __init__(self, contact_name, contact_number):
        self.contact_name = contact_name
        self.contact_number = contact_number

    def get_id(self):
        return self.id