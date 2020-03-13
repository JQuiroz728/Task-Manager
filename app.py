from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    dateCreated = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Home Route
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        taskContent = request.form['content']
        newTask = Task(content = taskContent)

        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding task to database'

    else:
        tasks = Task.query.order_by(Task.dateCreated).all()
        return render_template('index.html', tasks = tasks)

# Delete Route
@app.route('/delete/<int:id>')
def delete(id):
    deleteTask = Task.query.get_or_404(id)

    try:
        db.session.delete(deleteTask)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting task'

# Update Route
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error updating task'

    else:
        return render_template('update.html', task = task)

if __name__ == "__main__":
    app.run(debug = True)