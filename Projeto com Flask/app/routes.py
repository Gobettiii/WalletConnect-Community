from app import app, login, db
from flask import render_template, request, redirect, url_for, flash
from app.models import User, Contact
from app.form import UserLoginForm, UserRegisterForm, ContactForm
from flask_login import logout_user, login_required, login_user, current_user


# Rota da primeira página que será renderizada da aplicação
@app.route("/", methods=["POST", "GET"])
# Função para realizar o cadastro de um novo usuário
def register_user():
    # Instância do formulário de cadastro
    form = UserRegisterForm()
    # Validação das informações inseridas no cadastro
    if form.validate_on_submit():
        # Criação de um novo usuário
        new_user = User(form.username.data, form.password.data)
        # Adiciona o usuário novo no banco de dados
        db.session.add(new_user)
        db.session.commit()
        # Se o usuário for criado, ele será redirecionado para a página de login
        return redirect(url_for('log_in_user'))
    # Se não entrar no if para criar um usuário novo, a página de cadastro será renderizada novamente
    return render_template("register.html", form=form)


# Rota para um usuário já existente realizar login
@app.route('/login', methods=['POST', 'GET'])
def log_in_user():
    # Instância do formulário para um usuário realizar login
    form = UserLoginForm()
    # Validação das informações inseridas no formulário
    if form.validate_on_submit():
        # Criação de um usuário logado que conterá os dados de um usuário que foi cadastrado com sucesso
        user = User.query.filter_by(username=form.username.data).first()
        # Se o usuário que está tentando logar existir, o programa vai chamar a função verify_password do BD
        if user is not None:
            # Se a senha informada for igual a senha do BD, o login será efetuado e o usuário irá ser redirecionado pra página de menu
            if user.verify_password(form.password.data):
                login_user(user)
                return redirect(url_for("list_contacts"))     
        else:
            return render_template("login.html", form=form)
    # Caso não entre na condição inicial, a página de login será renderizada novamente
    return render_template("login.html", form=form)


# Carrega o usuário existente
@login.user_loader
def upload_user(username):
    # Filtra o usuário através do nome de usuáro definido
    return User.query.filter_by(username=username).first()


# Rota para realizar a ação de logout do usuário
@app.route('/logout')
# Usuário logado é requerido
@login_required
def log_out_user():
    # Função que permite o usuário deslogar
    logout_user()
    # Renderiza a página de cadastro após o usuário deslogar
    return redirect('/')


# Rota para adicionar novos contatos e necessita de um usuário vinculado
@app.route("/add_contacts/<username>", methods=['POST', 'GET'])
# Requere o login para realizar a função implementada abaixo
@login_required
def add_contacts(username):
    # Instância do formulário para adicionar contatos
    form = ContactForm()
    # Cria uma instância para o usuário logado que retrona erro 404 para entradas ausentes
    user = User.query.get_or_404(username)
    # Validação das informações inseridas no formulário
    if form.validate_on_submit():
        # Criação de um novo contato
        new_contact = Contact(form.name.data, form.number.data)
        # Adiciona um contato no relacionamento entre as tabelas User e Contato
        user.contacts.append(new_contact)
        db.session.commit()
        # Se o contato for criado, o usuário será redirecionado para a página de visualização dos contatos
        return redirect(url_for('list_contacts'))
    # Se não entrar no if para criar um novo contato, a página de adicionar contatos será renderizada novamente
    return render_template("add_contacts.html", form=form)


# Rota para a visualização dos contatos
@app.route("/all_contacts", methods=["POST", "GET"])
def list_contacts():
    # Instância do usuário que se encontra logado
    username = current_user.username
    """
    Instância que lista todos os contatos vinculados ao usuário homologado;
    foreign_key é a chave estrangeira da tabela contatos
    """
    all_contacts = Contact.query.filter_by(foreign_key=username)
    # Renderiza a página de visualização dos contatos
    return render_template("menu.html", all_contacts=all_contacts)


# Rota para atualizar algum contato já existente e necessita do id do contato em questão
@app.route("/update_contacts/<int:id>", methods=['POST', 'GET'])
# É requerido que um usuário esteja logado
@login_required
def update_contacts(id):
    # Instância do contato que será atualizado e que retorna erro 404 para entradas ausentes
    contact_for_update = Contact.query.get_or_404(id)
    # Instância do formulário para adicionar um contato
    form = ContactForm()
    # Se o método realizado for um POST vai-se entrar na condição descrita abaixo
    if request.method == "POST":
        # Condição para validação dos novos dados inseridos para um contato que já existe
        if form.validate_on_submit():
            contact_for_update.contact_name = form.name.data
            contact_for_update.contact_number = form.number.data
            # Atualiza o contato no banco de dados
            db.session.commit()
            # Se for bem sucedido, o usuário será redirecionado para a página de visualização dos contatos
            return redirect(url_for('list_contacts'))
    # Caso o método for um GET, vai aparecer para o usuário os dados atuais do contato
    elif request.method == 'GET':
        form.name.data = contact_for_update.contact_name
        form.number.data = contact_for_update.contact_number
    # Se o contato não for atualizado, vai ser renderizado a página de atualizar os contatos para o usuário ativo
    return render_template("update_contacts.html", form=form, contact_for_update=contact_for_update)


# Rota para deletar algum contato já existente e necessita da id do contato em questão
@app.route("/delete_contacts/<int:id>", methods=['POST', 'GET'])
# Requere um usuário logado para realizar a função implementada logo abaixo
@login_required
def delete_contacts(id):
    # Instância do contato que será deletado que retorna erro 404 para entradas ausentes
    contact_for_delete = Contact.query.get_or_404(id)
    # Realiza uma tentativa de deletar o contato
    try:
        db.session.delete(contact_for_delete)
        db.session.commit()
        # Redireciona para a página de visualização dos contatos
        return redirect(url_for('list_contacts'))
    # Se a tentativa der errado, retornará uma mensagem de erro
    except:
        flash("Aconteceu algum imprevisto, não foi possível excluir o contato")
        return redirect(url_for('list_contacts'))