from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import aliased
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost/gerencia_bar'
db = SQLAlchemy(app)

class Mesa(db.Model):
    id_mesa = db.Column(db.Integer, primary_key=True)
    num_mesa = db.Column(db.Integer)

class Produto(db.Model):
    cod = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20))
    valor = db.Column(db.Integer)

class ItemMesa(db.Model):
    id_item = db.Column(db.Integer, primary_key=True)
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesa.id_mesa'))
    cod_produto = db.Column(db.Integer, db.ForeignKey('produto.cod'))
    quantidade = db.Column(db.Integer)

    mesa = db.relationship('Mesa', backref=db.backref('itens_mesa', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('itens_mesa', lazy=True))

class Venda(db.Model):
    id_venda = db.Column(db.Integer, primary_key=True)
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesa.id_mesa'))
    valor_total = db.Column(db.Integer)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)

    mesa = db.relationship('Mesa', backref=db.backref('vendas', lazy=True))

@app.route('/')
def index():
    mesas = Mesa.query.all()
    return render_template('index.html', mesas=mesas)

@app.route('/mesa/<int:id_mesa>', methods=['GET', 'POST'])
def mesa(id_mesa):
    if request.method == 'POST':
        cod_produto = int(request.form['cod_produto'])
        quantidade = int(request.form['quantidade'])
        item_mesa = ItemMesa(id_mesa=id_mesa, cod_produto=cod_produto, quantidade=quantidade)
        db.session.add(item_mesa)
        db.session.commit()

    produtos = Produto.query.all()

    item_mesa_alias = aliased(ItemMesa)

    itens_mesa = (
        db.session.query(Produto.nome, Produto.valor, ItemMesa.quantidade, ItemMesa.id_item)
        .join(item_mesa_alias, Produto.cod == item_mesa_alias.cod_produto)
        .filter(item_mesa_alias.id_mesa == id_mesa)
        .all()
    )

    valor_total = sum([item[1] * item[2] for item in itens_mesa])

    if request.method == 'POST':
        if 'fechar_mesa' in request.form:
            mesa = Mesa.query.get(id_mesa)

            if mesa:
                valor_total = sum([item[1] * item[2] for item in itens_mesa])

                venda = Venda(id_mesa=id_mesa, valor_total=valor_total, data_venda=datetime.utcnow())

                db.session.add(venda)
                db.session.commit()

                return redirect(url_for('mesa', id_mesa=id_mesa))

    return render_template('mesa.html', id_mesa=id_mesa, itens_mesa=itens_mesa, valor_total=valor_total, produtos=produtos)


@app.route('/mesa/<int:id_mesa>/editar/<int:id_item>', methods=['GET', 'POST'])
def editar_item(id_mesa, id_item):
    item_mesa = ItemMesa.query.get(id_item)

    if item_mesa:
        if request.method == 'POST':
            nova_quantidade = int(request.form['nova_quantidade'])
     
            item_mesa.quantidade = nova_quantidade
            db.session.commit()

            return redirect(url_for('mesa', id_mesa=id_mesa))

        item = (item_mesa.produto.nome, item_mesa.produto.valor, item_mesa.quantidade, item_mesa.id_item)
        return render_template('editar_item.html', id_mesa=id_mesa, item=item)

    return "Item não encontrado", 404


@app.route('/mesa/<int:id_mesa>/excluir/<int:id_item>')
def excluir_item(id_mesa, id_item):
   
    item_mesa = ItemMesa.query.get(id_item)

    if item_mesa:
        db.session.delete(item_mesa)
        db.session.commit()

    return redirect(url_for('mesa', id_mesa=id_mesa))

@app.route('/mesa/<int:id_mesa>/fechar', methods=['POST'])
def fechar_mesa(id_mesa):
    mesa = Mesa.query.get(id_mesa)

    if mesa:
        item_mesa_alias = aliased(ItemMesa)

        itens_mesa = (
            db.session.query(ItemMesa)
            .filter(item_mesa_alias.id_mesa == id_mesa)
            .all()
        )

        valor_total = sum(item.quantidade * item.produto.valor for item in itens_mesa)

        venda = Venda(id_mesa=id_mesa, valor_total=valor_total, data_venda=datetime.utcnow())

        db.session.add(venda)
        db.session.commit()

        for item in itens_mesa:
            db.session.delete(item)

        mesa.status = 'fechada'

        db.session.commit()

        return redirect(url_for('mesa', id_mesa=id_mesa))

    return "Mesa não encontrada", 404



@app.route('/relatorio')
def relatorio():
    vendas = Venda.query.all()
    return render_template('relatorio.html', vendas=vendas)

if __name__ == '__main__':
    app.run(debug=True)
