from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, EqualTo, ValidationError
from app.models import User, Contact

#Classe do formulário para adicionar um novo contato
#o validators define que é necessário inserir um dado
class ContactForm(FlaskForm):
    name = StringField("Nome do contato:",
                            validators=[InputRequired(
                                        message="É necessário preencher este campo com um dado válido")])
    number = StringField("Numero de telefone:",
                            validators=[InputRequired(
                                        message="É necessário preencher este campo com um dado válido")])
    submit = SubmitField("Adicionar")


#Classe do formulário para cadastrar um novo usuário
class UserRegisterForm(FlaskForm):
    username = StringField("Nome de usuário desejado:",
                            validators=[InputRequired(
                                        message="É necessário preencher este campo com um dado válido")])
    password = PasswordField("Senha:",
                            validators=[InputRequired(
                                        message="É necessário preencher este campo com um dado válido")])
    check_password = PasswordField("Confirme sua senha:",
                            validators=[InputRequired(
                                        message="É necessário preencher este campo com um dado válido"),
                                        EqualTo('password', message='Senha incorreta')])
    submit = SubmitField("Cadastrar")


    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("Usuário já existente, tente novamente")

#Classe do formulário que possibilta o login de um usuário
class UserLoginForm(FlaskForm):
    username = StringField("Nome de usuario:", 
                            validators=[InputRequired(
                                        message="É necessário preencher este campo com um dado válido")])
    password = PasswordField("Senha:",
                            validators=[InputRequired(
                                        message="É necessário preencher este campo com um dado válido")])
    submit = SubmitField("Logar")

    def validate_username(self, username):
        false_user = User.query.filter_by(username=username.data).all()
        if false_user:
            pass
        else:
            raise ValidationError("Usuário inexistente")