from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import redirect
from flask import Flask, render_template, url_for
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tododo.db'
db = SQLAlchemy(app)



class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listinfo = db.Column(db.String(300), nullable=False)

    def __rep__(self):
        return '<Task %r>' % self.id

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        task_listinfo = request.form['listinfo']
        new_task = ToDo(listinfo=task_listinfo)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Problem adding task'

    else:
        tasks = ToDo.query.all()
        return render_template("index.html", tasks=tasks)



@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        task.listinfo = request.form['listinfo']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Problem updating task'

    else:
        return render_template('update.html', task=task)



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem deleting task'
