from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'yoursecretkey'

# Sample users
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "teacher1": {"password": "teach123", "role": "teacher"}
}

# Materials data: {name, quantity, consumable}
materials = [
    {"name": "Microscope", "quantity": 5, "consumable": False},
    {"name": "Beaker", "quantity": 20, "consumable": False},
    {"name": "Test Tube", "quantity": 100, "consumable": True}
]

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html", materials=materials, role=users[session['username']]['role'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials"
    return '''
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/checkout/<int:item_id>', methods=['POST'])
def checkout(item_id):
    qty = int(request.form['quantity'])
    if materials[item_id]['quantity'] >= qty:
        materials[item_id]['quantity'] -= qty
    return redirect(url_for('home'))

@app.route('/return_item/<int:item_id>', methods=['POST'])
def return_item(item_id):
    qty = int(request.form['quantity'])
    if not materials[item_id]['consumable']:
        materials[item_id]['quantity'] += qty
    return redirect(url_for('home'))

@app.route('/add_item', methods=['POST'])
def add_item():
    if users[session['username']]['role'] != "admin":
        return "Unauthorized", 403
    name = request.form['name']
    qty = int(request.form['quantity'])
    consumable = request.form['consumable'] == "yes"
    materials.append({"name": name, "quantity": qty, "consumable": consumable})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
