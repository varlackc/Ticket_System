from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from models import Login
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
    projectID = SelectField('Project', coerce=int)
    employeeID = SelectField('Employee', coerce=int)
    priority = SelectField('Priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed')], validators=[DataRequired()])
    submit = SubmitField('Submit')

#
#  PROJECT FORM         
#
class AddProject(FlaskForm):
    projectName = StringField('Title', validators=[DataRequired()], )
    projectDescription = TextAreaField('Description', validators=[DataRequired()])
    customerID = SelectField(u'Customer', coerce=int)
    projectManager = SelectField(u'Employee', coerce=int)
        
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