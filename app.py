from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["user_database"]
collection = db["users"]

@app.route('/')
def index():
    return render_template('index.html')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = {
            "name": name,
            "email": email,
            "password": password
        }

        collection.insert_one(user)
        return redirect('/login')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = collection.find_one({
            "email": email,
            "password": password
        })

        if user:
            return "Login Successful"
        else:
            return "Invalid Credentials"

    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)