from flask import Flask, render_template, request

app = Flask(__name__)


# These routes render Jinja templates. If you don't
# want to make a separate frontend, you can use Flask
# templates to create a website!
# Read more here: https://flask.palletsprojects.com/en/2.0.x/quickstart/#rendering-templates


@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route('/hello/')
@app.route('/hello/<user_name>') # This route passes in a name to the hello method
def hello(user_name=None):
    return render_template('hello.html', name=user_name)


# This route returns info about a Pokemon
@app.route('/get_pokemon/', methods=['GET'])
def get_pokemon_data():
    data = {
        "name": "Chimchar",
        "id": 390,
        "region": "Sinnoh (the best one)"
    }
    if request.method == 'GET':
        return data