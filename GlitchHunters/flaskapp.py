# Import the flask class
from flask import Flask, render_template, url_for, request, flash, redirect, session
from forms import LoginForm, AddTicket, AddProject
from flask_session import Session
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
import os

# set the ap variables
app = Flask(__name__)
app.config["SECRET_KEY"] = '5791628bb0b13ce0c676dfde280ba245'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

database_filename = "appdb.db"

# create the extension
db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.app = app
db.init_app(app)

def loggedIn():
    if not session.get("login"):
        return 0
    if session["login"] != 1:
        return 0
    return 1
=======
# App.route decorator sets the root of the website "Home Page"
@app.route("/")
@app.route("/login")
def login():
    # return the template home.html inside the template folder
    return render_template('login.html')

# App.route decorator sets the root of the website "Tickets"
@app.route("/tickets")
def tickets():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    # return the template home.html inside the template folder
    return render_template('tickets.html')

# App.route decorator sets the root of the website "Ticket Details"
@app.route("/ticket_detail")
def ticket_detail():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    ticketID = request.args.get('id')
    ticketTitle = "Example"

    return render_template('ticket_detail.html', title=ticketTitle, id=ticketID)

# App.route decorator sets the root of the website "Ticket Details"
@app.route("/add_ticket", methods=['GET', 'POST'])
def add_ticket():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    form = AddTicket()
    
    if(request.method == "POST"):
        if form.validate_on_submit():
            # NEED TO VALIDATE WITH DATABASE
            return redirect(url_for('tickets'))
        else:
            flash('Unsuccessful! Please retry.', 'danger')

    return render_template('add_ticket.html', title="Add Ticket", form=form)


# App.route decorator sets the root of the website "Tickets"
@app.route("/projects")
def projects():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
        
    # return the template home.html inside the template folder
    return render_template('projects.html')

# App.route decorator sets the root of the website "Ticket Details"
@app.route("/project_detail")
def project_detail():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    projectID = request.args.get('id')
    projectTitle = "Example"
    
    return render_template('project_detail.html', title=projectTitle, id=projectID)

# App.route decorator sets the root of the website "Add Project"
@app.route("/add_project", methods=['GET', 'POST'])
def add_project():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    form = AddProject()
    
    if(request.method == "POST"):
        if form.validate_on_submit():
            # NEED TO VALIDATE WITH DATABASE
            return redirect(url_for('projects'))
        else:
            flash('Unsuccessful! Please retry.', 'danger')

    return render_template('add_project.html', title="Add Project", form=form)

# App.route decorator sets the root of the website "Tickets"
@app.route("/customers")
def customers():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
        
    # return the template home.html inside the template folder
    return render_template('customers.html', title='Customers')

@app.route("/login", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    

    if form.validate_on_submit():
        # NEED TO VALIDATE WITH DATABASE
        
        if form.username.data == 'admin' and form.password.data == 'password':
            #flash('You have been logged in!', 'success')
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
