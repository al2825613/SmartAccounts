
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, os
from generate import generate_bulk_accounts

app = Flask(__name__)
app.secret_key = 'smartsecretkey'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '1234'

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    accounts = []
    if os.path.exists('logs.json'):
        with open('logs.json', encoding='utf-8') as f:
            accounts = json.load(f)
    accounts.reverse()
    return render_template('dashboard.html', accounts=accounts)

@app.route('/generate', methods=['POST'])
def generate():
    if 'user' not in session:
        return redirect(url_for('login'))

    platform = request.form['platform']
    quantity = int(request.form['quantity'])
    results = generate_bulk_accounts(platform, quantity)

    return render_template('dashboard.html', accounts=results, success=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='بيانات الدخول غير صحيحة')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
