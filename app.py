from flask import Flask, render_template_string, request, redirect, url_for, flash, session, Response

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Allowed credentials
USER_CREDENTIALS = {"username": "scit", "password": "hackopop"}

# Dummy account data
accounts = {
    "dummy": {"balance": 5000, "account_number": "1111111111", "name": "Ravi Patel", "status": "active"},
}

@app.route('/robots.txt')
def robots_txt():
    robots_content = """
    User-agent: *
    Disallow: /admin
    Disallow: /hiddenlog
    """
    return Response(robots_content, mimetype="text/plain")


@app.route('/hiddenlog')
def hidden_log():
    # The encoded value 'c2NpdDpoYWNrb3BvcA==' corresponds to 'scit:hackopop'
    hidden_log_content = "c2NpdDpoYWNrb3BvcA=="
    return Response(hidden_log_content, mimetype="text/plain")


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid username or password. Please try again.")

    # Show the login page with the challenge message
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sign In</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .container { text-align: center; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); max-width: 400px; width: 90%; }
            h1 { margin-bottom: 20px; font-size: 24px; color: #007bff; }
            input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
            button { padding: 10px 20px; background: #007bff; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
            button:hover { background: #0056b3; }
            .error { color: red; margin-top: 10px; }
            .challenge { font-size: 18px; color: #ff5733; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Sign In to Your Bank Account 🏦</h1>
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Sign In</button>
            </form>
            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    <div class="error">{{ messages[0] }}</div>
                {% endif %}
            {% endwith %}
            <div class="challenge">
                <p>Your challenge is to get into the bank's admin account and increase Ravi Patel's balance to $50,000. Good luck!</p>
            </div>
        </div>
    </body>
    </html>
    """)


@app.route('/admin/dummy', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            new_balance = int(request.form['balance'])
            accounts['dummy']['balance'] = new_balance
            if new_balance == 50000:
                flash("CTF{BankHacklolrobots3}")  # The flag is shown as a flash message
            else:
                flash("Balance updated successfully but no flag. Try again!")
        except ValueError:
            flash("Invalid input. Please enter a valid number.")
    
    # Render the admin dashboard
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 20px; }
            .dashboard { max-width: 800px; margin: 0 auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
            h1 { text-align: center; color: #28a745; }
            .account { margin-bottom: 20px; padding: 15px; border: 1px solid #ccc; border-radius: 4px; background: #f9f9f9; }
            .account h3 { margin: 0 0 10px; color: #007bff; }
            .account p { margin: 5px 0; font-size: 14px; }
            button { padding: 8px 16px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #218838; }
            input[type="number"] { padding: 5px; width: 100%; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
            .alert { color: red; font-size: 16px; margin-top: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <h1>Admin Dashboard</h1>
            <form action="/admin/dummy" method="POST">
                <div class="account">
                    <h3>Ravi Patel (Account No: 1111111111)</h3>
                    <p>Current Balance: ${{ accounts['dummy']['balance'] }}</p>
                    <input type="number" name="balance" value="{{ accounts['dummy']['balance'] }}" required>
                    <button type="submit">Update Balance</button>
                </div>
            </form>
            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    <div class="alert">{{ messages[0] }}</div>
                {% endif %}
            {% endwith %}
        </div>
    </body>
    </html>
    """, accounts=accounts)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
