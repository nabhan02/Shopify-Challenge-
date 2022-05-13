from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Inventory %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        item = request.form['content']

        new_item = Inventory(content=item)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding yuour task'
    else:
        items = Inventory.query.order_by(Inventory.date_created).all()
        return render_template('index.html', items=items)


@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Inventory.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Inventory.query.get_or_404(id)

    if request.method == 'POST':
        item.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue updating your task'
    else:
        return render_template('update.html', item=item)

if __name__ == "__main__":
    app.run(debug=True)

