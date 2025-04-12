from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import os
import hashlib
from utils import save_user_data, get_user_count, is_login_taken, is_email_taken, get_user_by_login

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Ensure static/json directory exists
os.makedirs('static/json', exist_ok=True)

@app.route("/")
def index():
    user_count = get_user_count()
    return render_template("index.html", title="Древо поколений | Главная", user_count=user_count)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Пароли не совпадают!', 'error')
            return redirect(url_for('register'))
            
        if is_login_taken(login):
            flash('Этот логин уже занят!', 'error')
            return redirect(url_for('register'))
            
        if is_email_taken(email):
            flash('Этот email уже используется!', 'error')
            return redirect(url_for('register'))
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user_data = {
            'login': login,
            'email': email,
            'password_hash': password_hash
        }
        
        if save_user_data(user_data):
            session['user_login'] = login  # Автоматический вход
            flash('Регистрация и вход выполнены успешно!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Ошибка при сохранении данных!', 'error')
    
    return render_template("register.html", title="Древо поколений | Регистрация")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        
        user = get_user_by_login(login)
        if not user:
            flash('Неверный логин или пароль!', 'error')
            return redirect(url_for('login'))
        
        # Проверка хеша пароля
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user['password_hash'] != password_hash:
            flash('Неверный логин или пароль!', 'error')
            return redirect(url_for('login'))
        
        # Успешная авторизация
        session['user_login'] = user['login']
        flash('Вы успешно вошли в систему!', 'success')
        return redirect(url_for('index'))
    
    return render_template("login.html", title="Древо поколений | Вход")

@app.route("/logout")
def logout():
    session.pop('user_login', None)
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

@app.route("/toggle-theme")
def toggle_theme():
    current_theme = request.cookies.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    
    resp = make_response(redirect(request.referrer or url_for('index')))
    resp.set_cookie('theme', new_theme, max_age=30 * 24 * 60 * 60)  # 30 дней
    return resp

if __name__ == "__main__":
    app.run(debug=True)