from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.secret_key = 'colocara_alguna_coisa'

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/risco_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para a tabela de Risco
class Risco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    tipo_risco = db.Column(db.String(100), nullable=False)
    area_identificadora = db.Column(db.String(100), nullable=False)
    data_entrada = db.Column(db.Date, nullable=False)
    consequencia = db.Column(db.String(200), nullable=False)
    projeto = db.Column(db.String(100), nullable=False)
    metier = db.Column(db.String(100), nullable=False)
    jalon = db.Column(db.String(100), nullable=False)
    probabilidade = db.Column(db.String(100), nullable=False)
    impacto = db.Column(db.String(100), nullable=False)
    estrategia = db.Column(db.String(100), nullable=False)
    acao = db.Column(db.String(100), nullable=False)
    nome_piloto = db.Column(db.String(100), nullable=False)
    id_piloto = db.Column(db.String(100), nullable=False)
    data_resposta = db.Column(db.Date, nullable=False)
    data_alerta = db.Column(db.Date, nullable=False)
    comentarios = db.Column(db.String(200), nullable=True)
    probabilidade_residual = db.Column(db.String(100), nullable=False)
    impacto_residual = db.Column(db.String(100), nullable=False)
    acao_validacao = db.Column(db.String(100), nullable=False)
    risco_validacao = db.Column(db.String(100), nullable=False)
    data_resolucao = db.Column(db.Date, nullable=False)
    capitalizacao = db.Column(db.String(100), nullable=False)

# Criação do banco de dados
with app.app_context():
    db.create_all()

USUARIO = "admin"
SENHA = "admin"

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']

        if usuario == USUARIO and senha == SENHA:
            session['user'] = usuario  # Armazena o usuário na sessão
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard
        else:
            erro = 'Usuário ou senha incorretos. Tente novamente.'
            return render_template('login.html', erro=erro)
    return render_template('login.html')
123

@app.route('/dashboard')
def dashboard():
    nome_usuario = USUARIO
    if 'user' in session:
        return render_template('dashboard.html', nome_usuario=nome_usuario)
    else:
        return redirect(url_for('login'))

@app.route('/cadastro_risco', methods=['GET', 'POST'])
def cadastro_risco():
    if 'user' in session:
        if request.method == 'POST':
            try:
                # Validação de campos obrigatórios
                required_fields = ['descricao', 'tipo_risco', 'area_identificadora', 'data_entrada', 'consequencia',
                                   'projeto', 'metier', 'jalon', 'probabilidade', 'impacto', 'estrategia', 
                                   'acao', 'nome_piloto', 'id_piloto', 'data_resposta', 'data_resolucao', 
                                   'data_alerta', 'probabilidade_residual', 'impacto_residual', 
                                   'acao_validacao', 'risco_validacao', 'capitalizacao']
                
                for field in required_fields:
                    if field not in request.form or request.form[field] == '':
                        flash(f'O campo {field} é obrigatório!', 'danger')
                        return render_template('cadastro_risco.html')

                # Convertendo datas
                data_resposta = datetime.strptime(request.form['data_resposta'], '%Y-%m-%d').date()
                data_resolucao = datetime.strptime(request.form['data_resolucao'], '%Y-%m-%d').date()

                # Criando novo risco
                nova_risco = Risco(
                    descricao=request.form['descricao'],
                    tipo_risco=request.form['tipo_risco'],
                    area_identificadora=request.form['area_identificadora'],
                    data_entrada=request.form['data_entrada'],
                    consequencia=request.form['consequencia'],
                    projeto=request.form['projeto'],
                    metier=request.form['metier'],
                    jalon=request.form['jalon'],
                    probabilidade=request.form['probabilidade'],
                    impacto=request.form['impacto'],
                    estrategia=request.form['estrategia'],
                    acao=request.form['acao'],
                    nome_piloto=request.form['nome_piloto'],
                    id_piloto=request.form['id_piloto'],
                    data_resposta=data_resposta,
                    data_alerta=request.form['data_alerta'],
                    comentarios=request.form['comentarios'],
                    probabilidade_residual=request.form['probabilidade_residual'],
                    impacto_residual=request.form['impacto_residual'],
                    acao_validacao=request.form['acao_validacao'],
                    risco_validacao=request.form['risco_validacao'],
                    data_resolucao=data_resolucao,
                    capitalizacao=request.form['capitalizacao']
                )
                db.session.add(nova_risco)
                db.session.commit()
                flash('Risco cadastrado com sucesso!', 'success')
                return redirect(url_for('dashboard'))
            except ValueError as e:
                flash('Formato de data inválido. Por favor, utilize o formato AAAA-MM-DD.', 'danger')
                return render_template('cadastro_risco.html')
            except Exception as e:
                flash('Erro ao cadastrar risco: {}'.format(str(e)), 'danger')
                return render_template('cadastro_risco.html')
        return render_template('cadastro_risco.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)

    return redirect(url_for('login'))

@app.route('/configuracao')
def configuracao():
    pass

if __name__ == '__main__':
    app.run(debug=True)
