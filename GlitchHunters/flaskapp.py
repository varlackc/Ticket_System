##########################################################
#  FLASK AND DATABASE     
##########################################################

# FLASK
from flask import Flask, render_template, url_for, flash, redirect, session, request

# Form Helper :)
from forms import RegistrationForm, LoginForm, AddProject, AddTicket

# Flask Session
from flask_session import Session

#SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# models.py
from models import Login, Ticket, Project, Employee

#Flask_SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

import json


##########################################################
#  CONFIGURATION         
##########################################################

#
# set the base
#
Base = declarative_base()

#
# set the ap variables
#
app = Flask(__name__)
app.config["SECRET_KEY"] = '5791628bb0b13ce0c676dfde280ba245'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///appdb.db"

#
# Database File Name (It is hard coded, but in case we decide to use the variable)
#
database_filename = "appdb.db"

#
# SQLAlchemy Object and DB Initialization
#
db = SQLAlchemy()
db.init_app(app)

#
# Create Engine
#
engine = create_engine("sqlite:///GlitchHunters/appdb.db", connect_args={"check_same_thread": False}, echo=True, future=True) 

#
# Create Meta Data
#
Base.metadata.create_all(bind=engine)

#
# Create DB Session
#
Session = sessionmaker(bind=engine)
connect = Session()

#
# Check if a user is logged in
#
def loggedIn():
    if not session.get("login"):
        return 0
    if session["login"] != 1:
        return 0
    return 1

##########################################################
#  TICKETS         
##########################################################

#
# Tickets Page
#
@app.route("/tickets")
def tickets():
    
    # Check if user is logged in
    if not loggedIn():
        return redirect("/login")
    
    rows = connect.query(Ticket).order_by(Ticket.ticketID.asc())
    
    # Load the tickets.html Template
    return render_template('tickets.html', title='Tickets', data=rows)

#
# Ticket Details Page
#
@app.route("/ticket_detail")
def ticket_detail():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    id = request.args.get('id')
    
    ticket = connect.query(Ticket).where(Ticket.ticketID==id).order_by(Ticket.ticketID.asc()).first()
    tpid = ticket.projectID
    project = connect.query(Project).where(Project.projectID==tpid).order_by(Project.projectID.asc()).first()
    projectName = project.projectName
    employee = connect.query(Employee).where(Employee.employeeID==ticket.employeeID).order_by(Employee.employeeID.asc()).first()
    employeeName = employee.employeeName

    # Load the ticket_detail.html Template
    return render_template('ticket_detail.html', t=ticket, projectName=projectName, employeeName=employeeName )

#
# Add Ticket
#
@app.route("/add_ticket", methods=['GET', 'POST'])
def add_ticket():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    form = AddTicket()
    
    if(request.method == "POST"):
        if form.validate_on_submit():
            # Get new Ticket ID
            targetRow = connect.query(Ticket).order_by(Ticket.ticketID.desc()).first()
            newID = targetRow.ticketID + 1
            
            # New Ticket Object
            #self, ticketID, ticketName, ticketDescription, projectID, employeeID, priority, status
            print(form.status.data)
            newTicket = Ticket(int(newID), form.ticketName.data, form.ticketDescription.data, form.projectID.data, form.employeeID.data, form.priority.data, form.status.data)
            
            # Insert Ticket Into Database
            connect.add(newTicket)
            connect.commit()
            
            return redirect("/tickets")
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(err, 'danger')

    return render_template('add_ticket.html', title="Add Ticket", form=form)

##########################################################
#  PROJECTS         
##########################################################

#
# Projects Page
#
@app.route("/projects")
def projects():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    rows = connect.query(Project).order_by(Project.projectID.asc())
        
    # Load the projects.html Template
    return render_template('projects.html', title='Projects', data=rows)

#
# Project Details
#
@app.route("/project_detail")
def project_detail():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    id = request.args.get('id')
    
    project = connect.query(Project).where(Project.projectID==id).order_by(Project.projectID.asc()).first()
    #tpid = ticket.projectID
    #project = connect.query(Project).where(Project.projectID==tpid).order_by(Project.projectID.asc()).first()
    #projectName = project.projectName
    #employee = connect.query(Employee).where(Employee.employeeID==ticket.employeeID).order_by(Employee.employeeID.asc()).first()
    #employeeName = employee.employeeName
    
    # Load the project_detail.html Template
    return render_template('project_detail.html', p=project)

#
# Add Project
#
@app.route("/add_project", methods=['GET', 'POST'])
def add_project():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    form = AddProject()
    
    if(request.method == "POST"):
        if form.validate_on_submit():
            # Get new Ticket ID
            targetRow = connect.query(Project).order_by(Project.projectID.desc()).first()
            newID = targetRow.projectID + 1
            
            # New Project Object
            # (projectID, projectName, projectNumber, projectDescription, projectManager, customerID, projectClient, projectStatus)
            newProject = Project(int(newID), form.projectName.data, 0, form.projectDescription.data, form.projectManager.data, form.customerID.data, "", form.projectStatus.data)
            
            # Insert Ticket Into Database
            connect.add(newProject)
            connect.commit()
            
            return redirect("/projects")
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(err, 'danger')

    return render_template('add_project.html', title="Add Project", form=form)
##########################################################
#  REGISTRATION         
##########################################################

#
# Create New Account
#
@app.route("/register", methods=['GET', 'POST'])
def register():
    
    if loggedIn():
        return redirect("/projects")
    
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        
        # Get new Login ID Object
        targetRow = connect.query(Login).order_by(Login.loginID.desc()).first()
        newID = targetRow.loginID + 1
        
        # New Login Object
        newLogin = Login(int(newID), form.username.data, form.password.data, form.firstname.data, form.lastname.data, "Demo")
        
        # Insert User Into Database
        connect.add(newLogin)
        connect.commit()

        flash('Your Account has been created! you are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


##########################################################
#  LOGIN / LOGOUT    
##########################################################

#
# Login
#
@app.route("/login", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def login():
    
    if loggedIn():
        return redirect("/projects")
    
    form = LoginForm()
    if form.validate_on_submit():
        if(request.method == "POST"):
            targetRow = connect.query(Login).where(Login.userName==form.username.data,Login.password==form.password.data).order_by(Login.loginID.desc()).first()
            if(targetRow):
                if targetRow.loginID > 0:
                    session["login"] = 1
                    return redirect(url_for('projects'))
            else:
                flash('Login Failed. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#
# Logout
#
@app.route("/logout")
def logout():
    session["login"] = 0
    return redirect("/login")

# setup so that we don't have to manually set environmental variables
if __name__ == '__main__':
    app.run(debug=True)