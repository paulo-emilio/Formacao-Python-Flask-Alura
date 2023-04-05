from flask import Flask, render_template


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


# Variável onde será colocada a aplicação
app = Flask(__name__)  # __name__ faz uma referência ao próprio arquivo, ele garante que vai rodar a aplicação


# Criando uma rota
@app.route('/inicio')
def ola():
    jogo1 = Jogo('Donkey Kong', 'Plataforma', 'Nintendo')
    jogo2 = Jogo('Mortal Kombat', 'Luta', 'PS2')
    jogo3 = Jogo('Dark Souls', 'RPG de ação', 'Xbox 360')
    jogo4 = Jogo('Red Dead Redemption', 'Ação e Aventura', 'Xbox 360')

    lista = [jogo1, jogo2, jogo3, jogo4]
    return render_template('lista.html',
                           titulo='Jogos',
                           jogos=lista)


@app.route('/novo')
def novo():
    return render_template('novo.html',
                           titulo='Novo Jogo')


app.run()
