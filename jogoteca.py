from flask import Flask, render_template, request, redirect, session, flash


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

# Definindo inicialização do programa com Flask
app = Flask(__name__)
app.secret_key = 'curso_flask'


# Tela inicial
@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)


# Tela de adicionar jogos
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        # não está logado
        return redirect('/login')
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
    return redirect('/')


# Tela de login
@app.route('/login')
def login():
    return render_template('login.html')


# Autenticando login
@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if '123' == request.form['senha']:
        # senha correta
        session['usuario_logado'] = request.form['usuario']  # salvando no navegador
        flash(session['usuario_logado'] + ' logado com sucesso!')
        return redirect('/')
    else:
        # senha incorreta
        flash('Usuário ou Senha Incorretos!')
        return redirect('/login')


# Fazendo logout
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário desconectado!')
    return redirect('/')


# Executando o programa
app.run(debug=True)  # debug para ficar sempre atualizado no navegador
