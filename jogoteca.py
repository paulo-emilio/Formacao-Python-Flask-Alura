from flask import Flask, render_template, request


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo('Donkey Kong', 'Plataforma', 'Nintendo')
jogo2 = Jogo('Mortal Kombat', 'Luta', 'PS2')
jogo3 = Jogo('Dark Souls', 'RPG de ação', 'Xbox 360')
jogo4 = Jogo('Red Dead Redemption', 'Ação e Aventura', 'Xbox 360')

lista = [jogo1, jogo2, jogo3, jogo4]


# Variável onde será colocada a aplicação
app = Flask(__name__)  # __name__ faz uma referência ao próprio arquivo, ele garante que vai rodar a aplicação


# Criando uma rota
@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return render_template('lista.html', titulo='Jogos', jogos=lista)


app.run(debug=True)
