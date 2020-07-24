from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


#To setup the application
app = Flask('__name__') #It references this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #3 slashes is for relative path.4 is for exact path.Then is the name of the db. 
db = SQLAlchemy(app) #db will be initialized with the settings of our app.Initialization.

class Todo(db.Model): #Creating a table in the database
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): #To return a string everytime we create a new element
        return '<Task %r>' %self.id #%r is the id of the task that has been created


#Creating an index route. In flask we use @app.route decorator to do so. Pass the URL string of the route
@app.route('/',methods=['POST','GET'])

def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue in adding you task!'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error deleting that Task.'

@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error in updating'
    else:
        return render_template('update.html', task = task)

if __name__ == "__main__":
    app.run(debug=True)