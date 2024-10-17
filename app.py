from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from flask_dance.contrib.google import make_google_blueprint, google
import os

app = Flask(__name__)
app.secret_key = '1234567890malone'  # Your specified secret key

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Usually 587 for TLS
app.config['MAIL_USERNAME'] = 'malonephillip779@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'jmre pwul hifx poao'  # Your generated app password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Set up Google OAuth
google_bp = make_google_blueprint(
    client_id='241936995125-uu83t6q7s7qb0e93b2l8pcpqqe2tv70u.apps.googleusercontent.com',
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET', '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'),
    redirect_to='google_login'
)
app.register_blueprint(google_bp, url_prefix='/google_login')

# List of recipients
recipients = [
    'Ayubkalama819@gmail.com',
    'Boazasami202@gmail.com',
    'eliusshukrani87@gmail.com',
    'AsamiOndenyo@gmail.com',
    'dankibettech@gmail.com'# Corrected email without spaces
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text
    session['user_name'] = resp.json()['displayName']  # Store user name in session
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        subject = request.form['subject']
        body = request.form['body']

        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=recipients)
        msg.body = body

        try:
            mail.send(msg)
            flash('Email sent successfully to all recipients!', 'success')
        except Exception as e:
            flash(f'Failed to send email: {e}', 'danger')

        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
