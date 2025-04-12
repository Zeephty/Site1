import json
import os

DATABASE_PATH = 'static/json/database.json'


def load_data():
    try:
        with open(DATABASE_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'users': []}


def get_user_count():
    data = load_data()
    return len(data.get('users', []))


def is_login_taken(login):
    data = load_data()
    return any(user['login'] == login for user in data.get('users', []))


def is_email_taken(email):
    data = load_data()
    return any(user['email'] == email for user in data.get('users', []))


def get_user_by_login(login):
    data = load_data()
    for user in data.get('users', []):
        if user['login'] == login:
            return user
    return None


def save_user_data(user_data):
    try:
        data = load_data()
        data['users'].append(user_data)
        
        with open(DATABASE_PATH, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False