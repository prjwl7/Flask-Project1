from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/tasks')
def tasks():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/delete/all', methods=['GET', 'POST'])
def delete_all_tasks():
    try:
        db.session.query(Todo).delete()
        db.session.commit()
        return redirect(url_for('tasks'))
    except Exception as e:
        print(e)
        return 'Error deleting tasks'

@app.route('/', methods=['POST', 'GET'])
def index():
    tasks = Todo.query.order_by(Todo.date_created).all()
    if request.method == 'POST':
        task_content = request.form['content']
        completed = 0
        date_created = datetime.now()
        due_date_str = request.form['due_date']
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')  # Parse due date string
        new_task = Todo(content=task_content, completed=completed, date_created=date_created, due_date=due_date)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            tasks = Todo.query.order_by(Todo.date_created).all()
            print(e)
            return 'There was an issue adding your task to the database'
    return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
