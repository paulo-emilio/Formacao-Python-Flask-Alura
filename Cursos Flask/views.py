from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app, db
from models import Jogos, Usuarios


# Tela inicial
@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)  # pegando a lista de jogos do 'prepara_banco.py'
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
    # conferindo se já existe no BD:
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existe na lista!')
        return redirect(url_for('novo'))
    # incluindo novo jogo
    else:
        novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
        # incluindo no bd, instanciado pelo SQLAlchemy
        db.session.add(novo_jogo)  # db = SQLAlchemy(app)
        # comitando para o banco
        db.session.commit()
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
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:  # verificando se o usuário informado está no dicionario
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            # mensagem
            flash(usuario.nickname + ' logado com sucesso!')
            # redirect
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        # usuário ou senha incorreta
        flash('Usuário ou Senha Incorretos!')
        return redirect(url_for('login'))


# Fazendo logout
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário desconectado!')
    return redirect(url_for('index'))
