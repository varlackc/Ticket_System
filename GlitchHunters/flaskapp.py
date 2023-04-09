# Import the flask class
from flask import Flask, render_template, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
#import models

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# login table model
class Login(Base):
    __tablename__ = "login"
    __table_args__ = {"sqlite_autoincrement": True}  # this should add auto increment
        
#    loginID = Column("loginID", Integer, index=True, unique=True, primary_key=True, autoincrement=True)
    loginID = Column("loginID", Integer, unique=True, primary_key=True)
    userName = Column("userName", String, nullable=False)
    password = Column("password", String, nullable=False)
    firstName = Column("firstName", String)
    lastName = Column("lastName", String)
    loginType = Column("loginType", String)
        
#    def __init__(self, userName, password, firstName, lastName, loginType):
    def __init__(self, loginID, userName, password, firstName, lastName, loginType):
        self.loginID = loginID
        self.userName = userName
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.loginType = loginType
            
    def __repr__(self):
        return f"({self.loginID}) {self.userName} {self.password} {self.firstName} {self.lastName} {self.loginType}"
#        return f"( {self.userName} {self.password} {self.firstName} {self.lastName} {self.loginType}"

# set the ap variables
app = Flask(__name__)
app.config["SECRET_KEY"] = '5791628bb0b13ce0c676dfde280ba245'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

database_filename = "appdb.db"

#app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_filename}"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///appdb.db"

db = SQLAlchemy(app)
db.init_app(app)

engine = create_engine("sqlite:///appdb.db", echo=True) 

Base.metadata.create_all(bind=engine)

#Session(app)

Session = sessionmaker(bind=engine)
session = Session()

#login1 = Login("", "user1", "password", "user1", "lastName1", "Demo")

# inserting new user data into database
# targetRow = session.query(Login).order_by(Login.loginID.desc()).first()
# newID = targetRow.loginID + 1
# login1 = Login(newID, "user1", "password", "user1", "lastName1", "Demo")
# session.add(login1)
# session.commit()

def loggedIn():
    if not session.get("login"):
        return 0
    if session["login"] != 1:
        return 0
    return 1

# App.route decorator sets the root of the website "Tickets"
@app.route("/tickets")
def tickets():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    # return the template home.html inside the template folder
    return render_template('tickets.html', title='Tickets')

# App.route decorator sets the root of the website "Ticket Details"
@app.route("/ticket_detail")
def ticket_detail():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    # return the template home.html inside the template folder
    return render_template('ticket_detail.html')


# App.route decorator sets the root of the website "Tickets"
@app.route("/projects")
def projects():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
        
    # return the template home.html inside the template folder
    return render_template('projects.html', title='Projects')

# App.route decorator sets the root of the website "Ticket Details"
@app.route("/project_detail")
def project_detail():
    # return the template home.html inside the template folder
    return render_template('project_detail.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        # post the new information into the database server
        #newLogin = Login(2, userName=form.username, firstName=form.firstname, lastName=form.lastname, password=form.password, loginType="User")
        #newLoginID = 
        #db.session.add(newLogin)
        #db.session.commit()
        
        # get the new loginID for the database object
        targetRow = session.query(Login).order_by(Login.loginID.desc()).first()
        newID = targetRow.loginID + 1
        
        # setup a new Login object to update the database
        newLogin = Login(int(newID), form.username.data, form.password.data, form.firstname.data, form.lastname.data, "Demo")
        
        # inserting new user data into database
        session.add(newLogin)
        session.commit()

        flash('Your Account has been created! you are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # NEED TO VALIDATE WITH DATABASE
        if form.username.data == 'demo' and form.password.data == 'demo':
            flash('You have been logged in!', 'success')
            session["login"] = 1
            
            return redirect(url_for('projects'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session["login"] = 0
    return redirect("/login")

# setup so that we don't have to manually set environmental variables
if __name__ == '__main__':
    app.run(debug=True)
