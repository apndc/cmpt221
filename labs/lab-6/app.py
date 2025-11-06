"""app.py: render and route to webpages"""

import os
import bcrypt
import logging 
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from db.query import get_all
from db.server import init_database
from db.schema import Users
from db.query import insert, get_one, get_all

# load environment variables from .env
load_dotenv()

# database connection - values set in .env
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"


def create_app():
    """Create Flask application and connect to your DB"""
    # create flask app
    app = Flask(__name__, 
                template_folder=os.path.join(os.getcwd(), 'templates'), 
                static_folder=os.path.join(os.getcwd(), 'static'))
    
    # connect to db
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    
    # Initialize database
    with app.app_context():
        if not init_database():
            print("Failed to initialize database. Exiting.")
            exit(1)

    # ===============================================================
    # routes
    # ===============================================================

    # create a webpage based off of the html in templates/index.html
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        """Sign up page: enables users to sign up"""
        error: str = None
        is_valid: bool = False
        #TODO: implement sign up logic here
        print(request.method)
        if request.method == 'POST':
                try:
                    firstname=request.form["FirstName"].strip()
                    lastname=request.form["LastName"].strip()
                    email=request.form["Email"].strip()
                    phonenumber=request.form["PhoneNumber"].strip()
                    password=request.form["pwd"].strip()

                    #insert_stmt = insert(User).values(request.form)

                    if request.form["FirstName"].isalpha():
                        print(f'Input: {request.form["FirstName"]} is valid.')
                        is_valid = True
                    else: 
                        error_msg = f'Input: {request.form["FirstName"]} is invalid! First name can only contain letters.'
                        print(f'Input: {request.form["FirstName"]} is invalid!')
                        error = error_msg

                    if request.form["LastName"].isalpha():
                        print(f'Input: {request.form["LastName"]} is valid.')
                        is_valid = True
                    else:
                        error_msg = f'Input: {request.form["FirstName"]} is invalid! Last name can only contain letters.'
                        print(f'Input: {request.form["FirstName"]} is invalid')
                        error = error_msg
                    
                    if is_valid:
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        hashed_password = hashed_password.decode('utf-8')

                        user=Users(FirstName=firstname,
                        LastName=lastname,
                        Email=email,
                        PhoneNumber=phonenumber,
                        Password=hashed_password)
                        insert(user)

                    return redirect(url_for('index'))
            
                except Exception as e:
                    print("Error inserting user:", e)
                    return render_template('error.html', error=str(e))

        #return redirect(url_for('signup'))
        return render_template('signup.html')
    
    @app.route('/login', methods=["GET", "POST"])
    def login():
        """Log in page: enables users to log in"""
        # TODO: implement login logic here
        if request.method == 'POST':
            email = request.form.get("Email")
            password = request.form.get("pwd")
            try:
                user = get_one(Users, Email=email)

                if user and user.Password == password:
                    return redirect(url_for('success'))
                #else:
                    #return render template('login.html', error="Invalid email or password.")

            except Exception as e:
                print("Error during login:", e)
                return render_template('error.html', error=str(e))
        return render_template('login.html')

    @app.route('/users')
    def users():
        """Users page: displays all users in the Users table"""
        all_users = get_all(Users)
        
        return render_template('users.html', users=all_users)

    @app.errorhandler(Exception)
    def handle_exception(e):
        print("An unexpected error occurred:")
        traceback.print_exc()
        return render_template('error.html', error=str(e)), 500

    @app.route('/success')
    def success():
        """Success page: displayed upon successful login"""

        return render_template('success.html')
        

    #Logger
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Configure a rotating log file (max 1MB per file, keep 3 backups)
    log_handler = RotatingFileHandler('logs/app.log', maxBytes=1_000_000, backupCount=3)
    log_handler.setLevel(logging.ERROR)  # only log errors and above

    # Define the log format
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] in %(module)s: %(message)s'
    )
    log_handler.setFormatter(formatter)

    # Attach the handler to the Flask app logger
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.ERROR)

    
    return app

if __name__ == "__main__":
    app = create_app()
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)