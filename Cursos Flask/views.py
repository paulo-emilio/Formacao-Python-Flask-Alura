from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogos, Usuarios
from jogoteca import app, db
from helpers import recupera_imagem


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
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    # incluindo no bd, instanciado pelo SQLAlchemy
    db.session.add(novo_jogo)  # db = SQLAlchemy(app)
    # comitando para o banco
    db.session.commit()

    # Imagens
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}.jpg')

    return redirect(url_for('index'))


# Tela de editar jogos
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # não está logado
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    # logado
    # query para pegar o objeto 'jogo'
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id=id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo)


# Atualizando jogo '/editar' na lista
@app.route('/atualizar', methods=['POST', ])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()  # guardando o objeto do bd que tem id fornecido
    # alterando os valores
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    # adicionando e comitando para o bd pelo SQLAlchemy
    db.session.add(jogo)
    db.session.commit()

    # Imagens
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{jogo.id}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        # não está logado
        return redirect(url_for('login'))

    # deletando
    Jogos.query.filter_by(id=id).delete()
    # commit para o banco
    db.session.commit()
    flash('Jogo deletado com sucesso!')
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

# Imagem
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
     return send_from_directory('uploads', nome_arquivo)


