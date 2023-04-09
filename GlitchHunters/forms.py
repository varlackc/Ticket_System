from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class AddTicket(FlaskForm):
    ticketName = StringField('Title', validators=[DataRequired()], )
    ticketDescription = StringField('Description', validators=[DataRequired()])
    projectID = StringField('Project', validators=[DataRequired()])
    
    # NEED TO PULL SELECT OPTIONS FROM DB FOR THESE TWO FIELDS
    projectID = SelectField(u'Project', choices=[('1', 'Example'), ('2', 'Test'), ('3', 'Demo')], validators=[DataRequired()])
    employeeID = SelectField(u'Employee', choices=[('1', 'John'), ('2', 'Jane'), ('3', 'Rob')], validators=[DataRequired()])
    
    priority = SelectField('Priority', choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('open', 'Open'), ('progress', 'In Progress'), ('closed', 'Closed')], validators=[DataRequired()])
    submit = SubmitField('Add')
    
class AddProject(FlaskForm):
    projectName = StringField('Title', validators=[DataRequired()], )
    projectDescription = StringField('Description', validators=[DataRequired()])
    
    # NEED TO PULL SELECT OPTIONS FROM DB FOR THESE TWO FIELDS
    customerID = SelectField(u'Customer', choices=[('1', 'Customer 1'), ('2', 'Customer 2'), ('3', 'Customer 3')], validators=[DataRequired()])
    projectManager = SelectField(u'Employee', choices=[('1', 'John'), ('2', 'Jane'), ('3', 'Rob')], validators=[DataRequired()])
    
    projectStatus = SelectField('Status', choices=[('open', 'Open'), ('progress', 'In Progress'), ('closed', 'Closed')], validators=[DataRequired()])
    submit = SubmitField('Add')   
