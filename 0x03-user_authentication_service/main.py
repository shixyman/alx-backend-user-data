import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

def register_user(email: str, password: str) -> None:
    """Register a new user"""
    response = requests.post('http://localhost:5000/register', data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'User created'}

def log_in_wrong_password(email: str, password: str) -> None:
    """Try to log in with a wrong password"""
    response = requests.post('http://localhost:5000/login', data={'email': email, 'password': password})
    assert response.status_code == 401
    assert response.json() == {'error': 'Unauthorized access'}

def log_in(email: str, password: str) -> str:
    """Log in with a valid email and password"""
    response = requests.post('http://localhost:5000/login', data={'email': email, 'password': password})
    assert response.status_code == 200
    assert 'session_id' in response.json()
    return response.json()['session_id']

def profile_unlogged() -> None:
    """Try to access the profile page without being logged in"""
    response = requests.get('http://localhost:5000/profile')
    assert response.status_code == 403
    assert response.json() == {'error': 'Forbidden'}

def profile_logged(session_id: str) -> None:
    """Access the profile page while being logged in"""
    headers = {'X-Session-ID': session_id}
    response = requests.get('http://localhost:5000/profile', headers=headers)
    assert response.status_code == 200
    assert response.json() == {'email': EMAIL}

def log_out(session_id: str) -> None:
    """Log out the user"""
    headers = {'X-Session-ID': session_id}
    response = requests.delete('http://localhost:5000/logout', headers=headers)
    assert response.status_code == 200
    assert response.json() == {'message': 'Logged out'}

def reset_password_token(email: str) -> str:
    """Request a password reset token"""
    response = requests.post('http://localhost:5000/reset_password', data={'email': email})
    assert response.status_code == 200
    assert 'reset_token' in response.json()
    return response.json()['reset_token']

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password with a valid reset token"""
    response = requests.put('http://localhost:5000/reset_password', data={'email': email, 'reset_token': reset_token, 'new_password': new_password})
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'Password updated'}

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)