##########################################################
#  FLASK AND DATABASE     
##########################################################

# FLASK
from flask import Flask, render_template, url_for, flash, redirect, session, request

# Form Helper :)
#from forms import RegistrationForm, LoginForm, AddProject, AddTicket, AddCustomer

# Flask Session
from flask_session import Session

#SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# models.py
from models import Login, Ticket, Project, Employee, Customer

#Flask_SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

import json

#Form Stuff
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

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
engine = create_engine("sqlite:///appdb.db", connect_args={"check_same_thread": False}, echo=True, future=True) 

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

##################################################################################################################
# FORMS
##################################################################################################################
    
#
#  LOGIN FORM     
#
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
#
#  REGISTRATION FORM         
#
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    firstname = StringField('FirstName',
                        validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('LastName',
                        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
   
#
#  TICKET FORM         
# 
class AddTicket(FlaskForm):
    ticketName = StringField('Title', validators=[DataRequired()], )
    ticketDescription = TextAreaField('Description', validators=[DataRequired()])
    
    rows = connect.query(Project).order_by(Project.projectID.asc())
    projectIDs = [0]
    projectNames = [""]
    if(rows):
        for r in rows:
            projectIDs.append(r.projectID)
            projectNames.append(r.projectName)
    projects = list(zip(projectIDs, projectNames))
    
    rows = connect.query(Employee).order_by(Employee.employeeID.asc())
    employeeIDs = [0]
    employeeNames = [""]
    if(rows):
        for r in rows:
            employeeIDs.append(r.employeeID)
            employeeNames.append(r.employeeName + " " + r.employeeLastName)
    employees = list(zip(employeeIDs, employeeNames))
    
    projectID = SelectField('Project', choices=projects, coerce=int)
    employeeID = SelectField('Employee', choices=employees, coerce=int)
    
    priority = SelectField('Priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed')], validators=[DataRequired()])
    submit = SubmitField('Submit')

#
#  PROJECT FORM         
#
class AddProject(FlaskForm):
    projectName = StringField('Title', validators=[DataRequired()], )
    projectDescription = TextAreaField('Description', validators=[DataRequired()])
    
    rows = connect.query(Customer).order_by(Customer.customerID.asc())
    customerIDs = [0]
    customerNames = [""]
    if(rows):
        for r in rows:
            customerIDs.append(r.customerID)
            customerNames.append(r.customerName)
    customers = list(zip(customerIDs, customerNames))
    
    rows = connect.query(Employee).order_by(Employee.employeeID.asc())
    employeeIDs = [0]
    employeeNames = [""]
    if(rows):
        for r in rows:
            employeeIDs.append(r.employeeID)
            employeeNames.append(r.employeeName + " " + r.employeeLastName)
    employees = list(zip(employeeIDs, employeeNames))
    
    customerID = SelectField(u'Customer', choices=customers, coerce=int)
    projectManager = SelectField(u'Employee', choices=employees, coerce=int)
        
    submit = SubmitField('Submit')
    
#
#  CUSTOMERS FORM         
#
class AddCustomer(FlaskForm):
    customerName = StringField('FIrst Name', validators=[DataRequired()], )
    customerLastName = StringField('Last Name', validators=[DataRequired()])
    customerPhoneNumber = StringField('Phone Number', validators=[DataRequired()])
    customerAddress = StringField('Street Address', validators=[DataRequired()])
    customerEmail = StringField('Email', validators=[DataRequired()])   
    customerNotes = TextAreaField('Notes', validators=[DataRequired()])    
    submit = SubmitField('Submit') 
    
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
    
    #rows = connect.query(Ticket).order_by(Ticket.ticketID.asc())
    projects = {"dict": "create"}
    employees = {"dict": "create"}
    rows = connect.query(Ticket).order_by(Ticket.ticketID.asc())
    for r in rows:
        project = connect.query(Project).where(Project.projectID==r.projectID).order_by(Project.projectID.asc()).first()
        if(project):
            projects[r.ticketID] = project.projectName
        else:
            projects[r.ticketID] = ""
        
        employee = connect.query(Employee).where(Employee.employeeID==r.employeeID).order_by(Employee.employeeID.asc()).first()
        if(employee):
            employees[r.ticketID] = employee.employeeName
        else:
            employees[r.ticketID] = ""
    
    # Load the tickets.html Template
    return render_template('tickets.html', title='Tickets', data=rows, projects=projects, employees=employees)

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
    if(project):
        projectName = project.projectName
    else:
        projectName = ""
    employee = connect.query(Employee).where(Employee.employeeID==ticket.employeeID).order_by(Employee.employeeID.asc()).first()
    if(project):
        employeeName = employee.employeeName
    else:
        employeeName = ""

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
        
    if(request.args.get('id')):
        row = connect.query(Ticket).where(Ticket.ticketID==request.args.get('id')).order_by(Ticket.ticketID.desc()).first()
        form = AddTicket(obj=row)
        title="Edit Project"
        edit = "yes"
    else:
        form = AddTicket()
        title="Add Project"
        edit = "no"
        
    if(request.method == "POST"):
        if form.validate_on_submit():
            
            # If it is an update
            if(request.args.get('id') and request.args.get('edit')):
                if(request.args.get('edit') == "yes" ):
                    ticket = connect.query(Ticket).where(Ticket.ticketID==request.args.get('id')).order_by(Ticket.ticketID.desc()).first()
                    ticket.ticketName = form.ticketName.data
                    ticket.ticketDescription = form.ticketDescription.data
                    ticket.projectID = form.projectID.data
                    ticket.employeeID = form.employeeID.data
                    ticket.priority = form.priority.data
                    ticket.status = form.priority.data
                    connect.add(ticket)
                    connect.commit()
                    return redirect("/ticket_detail?id="+request.args.get('id'))                
            
            
            # Get new Ticket ID
            targetRow = connect.query(Ticket).order_by(Ticket.ticketID.desc()).first()
            if(targetRow):
                newID = targetRow.ticketID + 1
            else:
                newID = 1
            
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

    return render_template('add_ticket.html', title="Add Ticket", form=form, type="add_ticket", id=request.args.get('id'), edit = edit)

#
# Delete Ticket
#
@app.route("/delete_ticket", methods=['GET', 'POST'])
def delete_ticket():
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    if(request.args.get('id') and request.args.get('delete')):
        ticket = connect.query(Ticket).where(Ticket.ticketID==request.args.get('id')).order_by(Ticket.ticketID.desc()).first()
        connect.delete(ticket)
        connect.commit()
    return redirect("/tickets")

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
    
    customers = {"dict": "create"}
    employees = {"dict": "create"}
    rows = connect.query(Project).order_by(Project.projectID.asc())
    for r in rows:
        
        customer = connect.query(Customer).where(Customer.customerID==r.customerID).order_by(Customer.customerID.asc()).first()
        if(customer):
            customers[r.projectID] = customer.customerName
        else:
            customers[r.projectID] = ""
        
        employee = connect.query(Employee).where(Employee.employeeID==r.projectManager).order_by(Employee.employeeID.asc()).first()
        if(employee):
            employees[r.projectID] = employee.employeeName
        else:
            employees[r.projectID] = ""
            
    # Load the projects.html Template
    return render_template('projects.html', title='Projects', data=rows, customers=customers, employees=employees)

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
    cid = project.customerID
    customer = connect.query(Customer).where(Customer.customerID==cid).order_by(Customer.customerID.asc()).first()
    if(customer):
        customerName = customer.customerName
    else:
        customerName = ""
    employee = connect.query(Employee).where(Employee.employeeID==project.projectManager).order_by(Employee.employeeID.asc()).first()
    if(employee):
        employeeName = employee.employeeName
    else:
        employeeName = ""
        
    # Load the project_detail.html Template
    return render_template('project_detail.html', p=project, customerName=customerName, employeeName=employeeName)

#
# Add Project
#
@app.route("/add_project", methods=['GET', 'POST'])
def add_project():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    if(request.args.get('id')):
        row = connect.query(Project).where(Project.projectID==request.args.get('id')).order_by(Project.projectID.desc()).first()
        form = AddProject(obj=row)
        title="Edit Project"
        edit = "yes"
    else:
        form = AddProject()
        title="Add Project"
        edit = "no"
        
    if(request.method == "POST"):
        if form.validate_on_submit():
            
            # If it is an update
            if(request.args.get('id') and request.args.get('edit')):
                if(request.args.get('edit') == "yes" ):
                    project = connect.query(Project).where(Project.projectID==request.args.get('id')).order_by(Project.projectID.desc()).first()
                    project.projectName = form.projectName.data
                    project.projectDescription = form.projectDescription.data
                    project.projectManager = form.projectManager.data
                    project.customerID = form.customerID.data
                    connect.add(project)
                    connect.commit()
                    return redirect("/project_detail?id="+request.args.get('id'))                
            
            # Get new Ticket ID
            targetRow = connect.query(Project).order_by(Project.projectID.desc()).first()
            if(targetRow):
                newID = targetRow.projectID + 1
            else:
                newID = 1
            
            # New Project Object
            # (projectID, projectName, projectNumber, projectDescription, projectManager, customerID, projectClient, projectStatus)
            newProject = Project(int(newID), form.projectName.data, 0, form.projectDescription.data, form.projectManager.data, form.customerID.data, "", "")
            
            # Insert Ticket Into Database
            connect.add(newProject)
            connect.commit()
            
            return redirect("/projects")
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(err, 'danger')

    return render_template('add_project.html', title=title, form=form, type="add_project", id=request.args.get('id'), edit = edit)

#
# Delete Project
#
@app.route("/delete_project", methods=['GET', 'POST'])
def delete_project():
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    if(request.args.get('id') and request.args.get('delete')):
        project = connect.query(Project).where(Project.projectID==request.args.get('id')).order_by(Project.projectID.desc()).first()
        connect.delete(project)
        connect.commit()
    return redirect("/projects")
    
##########################################################
#  CUSTOMERS         
##########################################################

#
# Customers Page
#
@app.route("/customers")
def customers():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    rows = connect.query(Customer).order_by(Customer.customerID.asc())
        
    # Load the customers.html Template
    return render_template('customers.html', title='Customers', data=rows)

#
# Customer Details
#
@app.route("/customer_detail")
def customer_detail():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    id = request.args.get('id')
    
    customer = connect.query(Customer).where(Customer.customerID==id).order_by(Customer.customerID.asc()).first()
    
    # Load the project_detail.html Template
    return render_template('customer_detail.html', c=customer)

#
# Add Customer
#
@app.route("/add_customer", methods=['GET', 'POST'])
def add_customer():
    
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    form = AddCustomer()
    
    if(request.args.get('id')):
        row = connect.query(Customer).where(Customer.customerID==request.args.get('id')).order_by(Customer.customerID.desc()).first()
        form = AddCustomer(obj=row)
        title="Edit Customer"
        edit = "yes"
    else:
        form = AddCustomer()
        title="Add Customer"
        edit = "no"
    
    if(request.method == "POST"):
        if form.validate_on_submit():
            
            # If it is an update
            if(request.args.get('id') and request.args.get('edit')):
                if(request.args.get('edit') == "yes" ):
                    customer = connect.query(Customer).where(Customer.customerID==request.args.get('id')).order_by(Customer.customerID.desc()).first()
                    customer.customerName = form.customerName.data
                    customer.customerLastName = form.customerLastName.data
                    customer.customerAddress = form.customerAddress.data
                    customer.customerEmail = form.customerEmail.data
                    customer.customerPhoneNumber = form.customerPhoneNumber.data
                    customer.customerNotes = form.customerNotes.data
                    connect.add(customer)
                    connect.commit()
                    return redirect("/customer_detail?id="+request.args.get('id'))                
            
            
            # Get new Ticket ID
            targetRow = connect.query(Customer).order_by(Customer.customerID.desc()).first()
            if(targetRow):
                newID = targetRow.customerID + 1
            else:
                newID = 1
            
            # New Project Object
            # (projectID, projectName, projectNumber, projectDescription, projectManager, customerID, projectClient, projectStatus)
            newCustomer = Customer(int(newID), form.customerName.data, form.customerLastName.data, form.customerPhoneNumber.data, form.customerAddress.data, form.customerEmail.data, "", "", form.customerNotes.data)
            
            # Insert Ticket Into Database
            connect.add(newCustomer)
            connect.commit()
            
            return redirect("/customers")
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(err, 'danger')

    return render_template('add_customer.html', title=title, form=form, type="add_customer", id=request.args.get('id'), edit = edit)

#
# Delete Customer
#
@app.route("/delete_customer", methods=['GET', 'POST'])
def delete_customer():
    # Check if logged in
    if not loggedIn():
        return redirect("/login")
    
    if(request.args.get('id') and request.args.get('delete')):
        customer = connect.query(Customer).where(Customer.customerID==request.args.get('id')).order_by(Customer.customerID.desc()).first()
        connect.delete(customer)
        connect.commit()
    return redirect("/customers")

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
  
