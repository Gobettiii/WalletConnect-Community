import os.path
#Pega o diretorio absoluto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    #Padrão flask
    SECRET_KEY = "my secret key"
    #Caminho do banco de dados
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bank.db')
    #Possibilita a modifcação por meio da IDE
    SQLALCHEMY_TRACK_MODIFICATIONS = True