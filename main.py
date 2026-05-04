from flask import Flask , render_template,request,redirect,url_for,flash,session
from database import get_deliveries,insert_deliveries,insert_user,check_user_exists
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)

brycpt = Bcrypt(app)


app.secret_key = '99dnjc8uinh8chbw88dnasskls0'


@app.route('/') 
def home():
    return  render_template('index.html')

def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected

@app.route('/deliveries')
@login_required
def deliveries():
    deliveries_data = get_deliveries()
    return render_template("deliveries.html",deliveries_data = deliveries_data)


@app.route('/add_deliveries',methods=['GET','POST'])
def add_deliveries():
    if request.method == 'POST':
        item_name = request.form['i_name']
        quantity_required = request.form['qty_req']
        quantity_delivered = request.form['qty_delivered']
        procuring_entity = request.form['proc_entity']
        receiver_name = request.form['r_name']
        receiver_contacts = request.form['r_contacts']
        new_deliveries = (item_name,quantity_required,quantity_delivered,procuring_entity,receiver_name,receiver_contacts)
        insert_deliveries(new_deliveries)
        flash("Delivery added successfully",'success')
    return redirect(url_for('deliveries'))

@app.route("/login")
def login():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = check_user_exists(email)
        if not existing_user:
            flash("User doesn't exist, please register",'danger')
        else:
            if bcrycpt.check_password_hash(existing_user[-1],password):
                session['email'] = email
                flash("Login successful",'success')
                return redirect(url_for('dashboard'))
            else:
                flash("Password incorrect",'danger')
    return render_template("login.html")


@app.route('/register',methods=['GET','POST'])
def regsiter():
    if request.method == 'POST':
        full_name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone']
        password = request.form['password']

        existing_user = check_user_exists(email)
        if not existing_user:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = (full_name,email,phone_number,hashed_password)
            insert_user(new_user)
            flash("User created successfully",'success')
        else:
            flash("User exists already ,please login",'danger')
    return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop('email',None)
    flash("User logged out successfully","success")
    return redirect(url_for('login'))

app.run(debug=True)