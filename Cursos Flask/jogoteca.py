from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instancia para criar algum jogo que será adicionado na Jogoteca
'''class Jogo:
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
            usuario3.nickname: usuario3}'''

# Definindo inicialização do programa com Flask
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from views import *

# Executando o programa
if __name__ == '__main__':
    app.run(debug=True)  # debug para ficar sempre atualizado no navegador
