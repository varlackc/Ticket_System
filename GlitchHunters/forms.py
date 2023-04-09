from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

##########################################################
#  LOGIN FORM     
##########################################################
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
##########################################################
#  REGISTRATION FORM         
##########################################################
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
   
##########################################################
#  TICKET FORM         
########################################################## 
class AddTicket(FlaskForm):
    ticketName = StringField('Title', validators=[DataRequired()], )
    ticketDescription = StringField('Description', validators=[DataRequired()])
    
    projectID = SelectField(u'Project', choices=[('1', 'Example'), ('2', 'Test'), ('3', 'Demo')])
    employeeID = SelectField(u'Employee', choices=[('1', 'John'), ('2', 'Jane'), ('3', 'Rob')])
    
    priority = SelectField('Priority', choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')])
    status = SelectField('Status', choices=[('open', 'Open'), ('progress', 'In Progress'), ('closed', 'Closed')], validators=[DataRequired()])
    submit = SubmitField('Add')

##########################################################
#  PROJECT FORM         
##########################################################
class AddProject(FlaskForm):
    projectName = StringField('Title', validators=[DataRequired()], )
    projectDescription = StringField('Description', validators=[DataRequired()])
    
    # NEED TO PULL SELECT OPTIONS FROM DB FOR THESE TWO FIELDS
    customerID = SelectField(u'Customer', choices=[('1', 'Customer 1'), ('2', 'Customer 2'), ('3', 'Customer 3')], validators=[DataRequired()])
    projectManager = SelectField(u'Employee', choices=[('1', 'John'), ('2', 'Jane'), ('3', 'Rob')], validators=[DataRequired()])
    
    projectStatus = SelectField('Status', choices=[('open', 'Open'), ('progress', 'In Progress'), ('closed', 'Closed')], validators=[DataRequired()])
    submit = SubmitField('Add')   
