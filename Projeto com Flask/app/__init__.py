from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

# Cria a instância da aplicação
app = Flask(__name__)
# Configura a aplicação conforme os atributos do objeto importado do módulo config
app.config.from_object(Config)
# Cria a instância do banco de dados em relação à aplicação criada
db = SQLAlchemy(app)
# Gerenciador de login que permite que a aplicação trabalhe junto com o flask_login
login = LoginManager()
# Configuração para efetuar o login
login.init_app(app)

# Não importa no início do arquivo pelo fato de necessitar que as instâncias estejam criadas
from app import routes
from app import models
from app import form