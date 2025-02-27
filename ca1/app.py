from flask import Flask, render_template,session, request, make_response, g, redirect, url_for
import form
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'MYKEY'
Session(app)
app.teardown_appcontext(close_db)

@app.before_request
def load_user():
    g.user = session.get('user_id', None)


def log_check(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next = request.url))
        return view(*args, **kwargs)
    return wrapped_view


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shopping')
@log_check
def shopping():
    pass


@app.route('/login', methods=['GET,POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get.db()
        user_check = db.execute('''
            SELECT * FROM users
            WHERE user_id = ?''',(user_id,)).fetchone()
        if user_check is None:
            form.user_id.errors.append('''User doesn't exist!''')
        elif not check_password_hash(
                        user_check['password'], password):
            form.password.errors.append('Incorrect password!')
        else:
            session.clear()
            session['user_id'] = user_id
            session.modified = True
                next_page = request.args.get('next')
                if not next_page:
                    next_page = url_for('index')
                return redirect(next_page)
    return render_template('login.html', form = form)


@app_route('/password_reset/IDCheck', methods=['GET,POST'])
def pass_reset1():
    form = SecurityForm1()
    securityQ = ''
    if form.validate_on_submit():
        user_id = form.user_id.data
        db = get.db()
        user_check = db.execute('''
            SELECT * FROM users
            WHERE user_id = ?''',(user_id,)).fetchone()
        if user_check is None:
            form.user_id.errors.append('''User doesn't exist!''')
        else:
            securityQ_get = db.execute('''
                                        SELECT securityQ FROM users
                                        WHERE user_id = ?)''',(user_id,)).fetchone()
            securityA_get = db.execute('''
                                        SELECT securityA FROM users
                                        WHERE user_id = ?)''',(user_id,)).fetchone()
            form = SecurityForm2()
            securityQ = securityQ_get
            if form.validate_on_submit():
                if session['error_count'] not in session:
                    session['error_count'] = 0
                if session['freeze_time'] not in session:
                    session['freeze_time'] = None
                if datetime.now() > session['freeze_time']:
                    securityA = form.securityA.data
                    if not check_password_hash(
                            securityA_get['securityA'], password):
                        session['error_count'] += 1
                        chance_left = 3 - session['error_count']
                        if session['error_count'] < 3:
                            form.securityA.errors.append('Incorrect answer! You have %i chances left'%(chance_left))
                        else:
                            now = datetime.now(.strftime('%Y-%m-%d %H:%M:%S'))
                            session['freeze_time'] += timedelta(days = 1)
                            return redirect(url_for('reset_error'))
                            
                    else:
                        session['error_count'] = 0
                        form = ResetPassForm()
                        securityQ = ''
                        if form.validate_on_submit():
                            password = form.password.data
                            password_reset = db.execute('''UPDATE users
                                                SET password = ?
                                                WHERE user_id = ?''',(password,user_id))
                            password_reset.commit()
                            return redirect(url_for('login'))
                else:
                    return redirect(url_for('reset_error'))

    return render_template('password_reset.html', form = form, securityQ = securityQ)


@app.route('/reset_error')
def reset_error():
    freeze_time = session['freeze_time']
    return render_template('reset_error.html',freeze_time = freeze_time)

