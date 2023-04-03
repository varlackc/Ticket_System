# Import the flask class
from flask import Flask, render_template, url_for

# set the ap variables
app = Flask(__name__)

# App.route decorator sets the root of the website "Home Page"
@app.route("/")
@app.route("/home")
def home():
    # return the template home.html inside the template folder
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

# setup so that we don't have to manually set environmental variables
if __name__ == '__main__':
    app.run(debug=True)