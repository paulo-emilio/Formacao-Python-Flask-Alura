from flask import Flask, render_template

# Variável onde será colocada a aplicação
app = Flask(__name__)  # __name__ faz uma referência ao próprio arquivo, ele garante que vai rodar a aplicação


# Criando uma rota
@app.route('/inicio')
def ola():
    lista = ['Dark Souls', 'Donkey Kong', 'Red Dead Redemption']
    return render_template('lista.html',
                           titulo='Jogos',
                           jogos=lista)


app.run(host='0.0.0.0', port=8080)
