# Import the flask class
from flask import Flask, render_template, url_for, flash, redirect, session
from forms import LoginForm
from flask_session import Session

# set the ap variables
app = Flask(__name__)
app.config["SECRET_KEY"] = '5791628bb0b13ce0c676dfde280ba245'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
