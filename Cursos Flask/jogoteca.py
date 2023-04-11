from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy


# Instancia para criar algum jogo que será adicionado na Jogoteca
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo('Mario', 'Plataforma', 'Nintendo')
jogo2 = Jogo('Dark Souls', 'RPG de ação', 'Xbox 360')
jogo3 = Jogo('Red Dead Redemption 2', 'Aventura', 'PS4')
lista = [jogo1, jogo2, jogo3]


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario('Darth', 'darth', 'darth1')
usuario2 = Usuario('Loki', 'loki', 'loki1')
usuario3 = Usuario('Gandalf', 'gandalf', 'gandalf1')
usuarios = {usuario1.nickname: usuario1,
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3}


# Definindo inicialização do programa com Flask
app = Flask(__name__)
app.secret_key = 'curso_flask'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='admin',
        servidor='localhost',
        database='jogoteca'
    )

db = SQLAlchemy(app)


class Jogos(db.Model):
    id = db.Column(db.Integer(11), primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Usuarios(db.Model):
    nome = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(8), nullable=False, primary_key=True)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


# Tela inicial
@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)


# Tela de adicionar jogos
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        # não está logado
        return redirect(url_for('login', proxima=url_for('novo')))
    # logado
    return render_template('novo.html', titulo='Novo Jogo')


# Adionando jogo '/novo' à lista
@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))


# Tela de login
@app.route('/login')
def login():
    proxima = request.args.get('proxima')  # query que vem de '/novo'
    return render_template('login.html', proxima=proxima)


# Autenticando login
@app.route('/autenticar', methods=['POST', ])
def autenticar():
    # autenticando nick
    if request.form['usuario'] in usuarios:  # verificando se o usuário informado está no dicionario
        usuario = usuarios[request.form['usuario']]  # nickname
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            # mensagem
            flash(usuario.nickname + ' logado com sucesso!')
            # redirect
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        # senha incorreta
        flash('Usuário ou Senha Incorretos!')
        return redirect(url_for('login'))


# Fazendo logout
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário desconectado!')
    return redirect(url_for('index'))


# Executando o programa
app.run(debug=True)  # debug para ficar sempre atualizado no navegador
