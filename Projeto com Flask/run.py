from app import app
from app import db
import os

if __name__ == "__main__":
    #Cria o banco de dados se ele ainda não existir
    if not os.path.exists('db.sqlite'):
        db.create_all()
    #Roda a aplicação 
    app.run(debug=True)