from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import login_user, logout_user, login_required, current_user, LoginManager, UserMixin

app = Flask(__name__)
app.secret_key = '1'


#connecting mysql to server
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudeapp'
mysql = MySQL(app)

#Login to stay log in shenanigens
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin):
    # This class inherits essential Flask-Login methods from UserMixin.
    def __init__(self, id, email, name, number, password):
        self.id = id
        self.email = email
        self.name = name
        self.number = number
        self.password = password

@login_manager.user_loader
def load_user(id):
    # This function is called by Flask-Login to load a user from the session cookie.
    cursor = mysql.connection.cursor()
    # Ensure all required fields for the User class are selected
    cursor.execute("SELECT id, email, name, number, password FROM accs WHERE id = %s", (id,))
    user_record = cursor.fetchone()
    cursor.close()

    if user_record:
        # Pass the fetched data to the User object constructor
        user_id, email, name, number, password = user_record
        return User(id=user_id, email=email, name=name, number=number, password=password)
    return None

#Secret Sauce for login
@app.context_processor
def inject_user():
    return dict(user=current_user)

#___________________________HOMEof Web_____________________________________________

@app.route('/')
def home():
    return render_template('home.html', user=current_user)

#INSIDE INDEX

@app.route('/index')
def index():

    cursor = mysql.connection.cursor() #to add query data to database
    cursor.execute('SELECT * FROM accs')
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', accounts=data, user=current_user)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        id_data = request.form['id'] #change from given id
        email = request.form['email']
        name = request.form['name']
        number = request.form['number']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE accs
        SET email = %s, name = %s, number = %s, password = %s 
        WHERE id = %s
        """, (email, name, number, password, id_data))

        flash('Account updated!')
        mysql.connection.commit()
    return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods=['GET', 'POST'])
def delete(id_data):

    flash("data Deleted Successfully")

    cursor = mysql.connection.cursor()
    cursor.execute("delete from accs WHERE id = %s", (id_data))
    mysql.connection.commit()
    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------
# CLI

@app.route('/cli', methods=['GET'])
def cli():
    cursor = mysql.connection.cursor()  # to add query data to database
    cursor.execute('SELECT * FROM accs')
    data = cursor.fetchall()
    cursor.close()

    modified_encoded_data = []

    for row in data:
        row_list = list(row) #list is the list in the db

        original_password = row_list[4] #4th row is the password btw
        encoded_data = enc(original_password)

        row_list[4] = encoded_data

        modified_encoded_data.append(row_list)

    return render_template('cli.html', accounts=modified_encoded_data, user=current_user)



def enc(text, key = 13):
    result = ""

    for c in text:
        if c.isalpha():
            start = ord('A') if c.isupper() else ord('a')
            addstart = ord(c) - start
            optkey = (addstart + key) % 26
            shift = chr(optkey + start)

            result += shift
        else:
            result += c
    return result


# -------------------------------------------------------------------------------------------
# LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email and not password:
            return redirect(url_for('cli'))

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT id, email, name, number, password FROM accs WHERE email = %s", (email, ) )

        user_record = cursor.fetchone()

        if user_record:

            user_id, user_email, name, number, stored_password = user_record

            if stored_password == password:

                user_obj = User(id=user_id, email=user_email, name=name, number=number, password=stored_password)
                login_user(user_obj)

                flash("Login Successful" , category='success')

                return redirect(url_for('index'))
            else:
                #
                flash('Incorrect password.', category='error')
        else:

            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST']) # get is retrieving data, post is if it sent (button pressed)
def signup():
    if request.method == 'POST': #if button is clicked
        email = request.form.get('email') # get function, to get data from the entered post
        name = request.form.get('name')
        number = request.form.get('number')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()

        #if email == email typa thingy
        cursor.execute("SELECT id FROM accs WHERE email = %s", (email, ) )
        user_exists = cursor.fetchone()


        if user_exists:
            flash('email already exist!', category='error')
        elif len(email) < 4:
            flash(' Email must be longer ', category='error') #flash
        elif len(name) < 0:
            flash(' Firstname must be longer ', category='error')
        elif len(password) < 6:
            flash(' BRUH ', category='error')
        else:

            cursor.execute("""
            INSERT INTO accs (email, name, number, password) 
            VALUES (%s, %s, %s, %s)""", (email, name, number, password))

            mysql.connection.commit()
            cursor.close()

            flash('Account Created!', category='l')
            return redirect(url_for('login'))

    return render_template("signup.html", user=current_user)


if __name__ == '__main__':
    app.run(debug=True)

