from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados SQLite persistente
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo Paciente
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Paciente {self.nome}>"

def cadastrar_paciente(paciente):
    db.session.add(Paciente(nome=paciente))
    db.session.commit()

def deletar_paciente(paciente):
    paciente = Paciente.query.filter_by(nome=paciente).first()
    if paciente:
        db.session.delete(paciente)
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        acao = request.form.get('acao')
        if nome and acao == 'cadastrar':
            cadastrar_paciente(nome)
        if nome and acao == 'deletar':
            deletar_paciente(nome)

        return redirect(url_for('index'))

    pacientes = Paciente.query.all()
    return render_template('home.html', pacientes=pacientes)

@app.route('/api/pacientes', methods=['GET'])
def listar_pacientes():
    pacientes = Paciente.query.all()
    lista = [{"id": p.id, "nome": p.nome} for p in pacientes]
    return jsonify(lista)

@app.route('/api/pacientes', methods=['POST'])
def registro_paciente():
    data = request.get_json()
    nome = data['nome']
    if nome:
        cadastrar_paciente(nome)
        return jsonify({"mensagem": "Paciente criado"}), 201

    return jsonify({"erro": "Nome inválido"}), 400


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria o banco e as tabelas se não existirem

    app.run(debug=True)
