from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)

db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/task.db"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)

    def __repr__(self):
        return '<User %r>' % self.content

@app.route('/')
def home():
    task = Task.query.all()
    return render_template('index.html',task=task)


@app.route('/add',methods=["POST"])
def add():
    new_task = Task(content=request.form["content"], done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    Task.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect ("/")


@app.route('/done/<int:id>')
def done(id):
    task = Task.query.filter_by(id=id).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect ("/")

@app.route('/update/<int:id>',methods=["POST","GET"])
def update(id):
    message = None
    task = Task.query.filter_by(id=id).first()

    if request.method == "POST":
        if not request.form['content']:
            message = "ERROR, TASK EMPTY"
            return render_template('update.html',task=task,message=message)

        task.content = request.form['content']
        db.session.commit()
        return redirect("/")

    return render_template("update.html",task=task,message=message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
