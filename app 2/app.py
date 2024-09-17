from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy data for users
users = {'admin': 'password123'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('You need to login first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/dashboard')
@login_required
def dashboard():
    partitions = ['Partition 1', 'Partition 2', 'Partition 3']
    return render_template('dashboard.html', partitions=partitions)

@app.route('/visualize')
@login_required
def visualize():
    # Dummy data for visualization
    data = [25, 40, 35]
    labels = ['Category A', 'Category B', 'Category C']
    return render_template('visualize.html', data=data, labels=labels)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
