from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
import os


class FormularioJogo(FlaskForm):
    # uma variável para cada categoria
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria do Jogo', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Consoles', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

        return 'capa_padrao.jpg'


def deleta_imagem(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
