import hashlib
from db_configs.db_settings import execute_query, fetchone
from db_configs.queries import insert_user, select_user_by_username


def hash_password(password):
    '''Hashes the password using the sha256 algorithm.'''
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def register_user(username, password):
    '''Registers a new user, returns an error if the username already exists.'''
    existing_user = fetchone(select_user_by_username(), (username,))
    if existing_user:
        return 'Username already exists!'

    hashed_password = hash_password(password)
    try:
        execute_query(insert_user(), (username, hashed_password, 'user'))
        return 'User registered successfully!'
    except Exception as e:
        return {'error': str(e)}


def login_user(username, password):
    '''Login function that checks if the username and password are valid.'''
    user = fetchone(select_user_by_username(), (username,))
    if user and user[2] == hash_password(password):
        return 'Login successful!'
    else:
        return 'Invalid credentials!'


def check_admin(username, password):
    '''Function to check admin credentials.'''
    admin_username = 'admin'
    admin_password = 'admin'

    if username == admin_username and password == admin_password:
        return True
    return False
