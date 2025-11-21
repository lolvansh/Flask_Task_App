# imprrorts
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#my app
app = Flask(__name__)
Scss(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.String(100), default=0)
    created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"task {self.id}"
    

@app.route("/",methods=["POST","GET"])
def index():
    
    
    #add task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = Mytask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error:{e}")
            return (f"error:{e}")
        
        
    else:
        tasks = Mytask.query.order_by(Mytask.created).all()
        return render_template("index.html",tasks=tasks)




@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = Mytask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"error: {e}"

if __name__ in "__main__":
    
    with app.app_context():
        db.create_all();
        
    app.run(debug=True)