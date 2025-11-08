# TODO: add five more unit test cases
#Lab 8 Tests
def test_signup_page_loads(client):
    """Test that signup page loads"""
    response = client.get('/signup')
    assert response.status_code == 200


def test_success_page_loads(client):
    """Test that success page loads"""
    response = client.get('/success')
    assert response.status_code == 200


def test_error_page_loads(client):
    """Test that error page loads"""
    response = client.get('/error')
    assert response.status_code == 200


def test_invalid_last_name(client):
    """Test signup validation for invalid last name"""
    response = client.post('/signup', data={
        'FirstName': 'John',
        'LastName': '123',  # invalid - contains numbers
        'Email': 'john@test.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    assert b'Last name can only contain letters' in response.data


def test_missing_form_fields(client):
    """Test signup when required form fields are missing"""
    response = client.post('/signup', data={
        'FirstName': '',
        'LastName': '',
        'Email': '',
        'PhoneNumber': '',
        'Password': ''
    })
    assert response.status_code in (200, 500)

def test_home_page(client):
    """Test that home page loads"""
    response = client.get('/')
    assert response.status_code == 200

def test_login_page(client):
    """Test that home page loads"""
    response = client.get('/login')
    assert response.status_code == 200

def test_users_page(client):
    """Test that users page loads"""
    response = client.get('/users')
    assert response.status_code == 200

def test_invalid_first_name(client):
    """Test signup validation for invalid first name"""
    response = client.post('/signup', data={
        'FirstName': '123',  # invalid - contains numbers
        'LastName': 'Doe',
        'Email': 'test@test.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    assert b'First name can only contain letters' in response.data

def test_invalid_phone_number(client):
    """Test signup validation for invalid phone number"""
    response = client.post('/signup', data={
        'FirstName': 'John',
        'LastName': 'Doe',
        'Email': 'test@test.com',
        'PhoneNumber': '123',  # invalid - not 10 digits
        'Password': 'password123'
    })
    assert b'Phone number must be exactly 10 digits' in response.data