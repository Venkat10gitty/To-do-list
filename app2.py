#importing the Flask class
from flask import Flask ,render_template,request,redirect
#render_template used to generate output from a template file that is found in the application's templates folder.
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app2=Flask(__name__)
#app2.route() are nothing but they are pages of the website

#creating database
app2.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app2.config['SQLACHEMY_TRACK_MODIFICATIONS']=False
app2.config['SQLACHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app2)


#defining todo python class too define database schema
# (Model) is a Python class which represents the database table and its attributes map to the column of the table.
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    #this function is to mention about what to display when we print an todo object
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app2.route('/',methods=['GET','POST'])
def home_page():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        
        todo=Todo(title=title,desc=desc)#creating an row
        db.session.add(todo)#adding the row into database
        db.session.commit()

    allTodo=Todo.query.all()
   # print(allTodo)
    return render_template('index.html',allTodo=allTodo)#displaying the allTodo data in the html page using jinja2 looping

@app2.route('/delete/<int:sno>') #<int:sno> will return sno
def delete_fun(sno):#passing returned sno
    todo=Todo.query.filter_by(sno=sno).first()#filters the data according the returned sno and saves the first required row in todo
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app2.route('/update/<int:sno>',methods=['GET','POST'])
def update_fun(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)#adding the row into database
        db.session.commit()
        return redirect("/")

    todo=Todo.query.filter_by(sno=sno).first()#selecting the record according the sno
    return render_template('update.html',todo=todo)

    
#now we are asking app to run
if __name__=="__main__":
    app2.run(debug=True,port=7000)