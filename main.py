from flask import Flask , render_template,request,redirect,url_for,flash
from database import get_deliveries,insert_deliveries

app = Flask(__name__)


app.secret_key = '99dnjc8uinh8chbw88dnasskls0'


@app.route('/') 
def home():
    return  render_template('index.html')

@app.route('/deliveries')
def deliveries():
    deliveries_data = get_deliveries()
    return render_template("deliveries.html",deliveries_data = deliveries_data)


@app.route('/add_deliveries',methods=['GET','POST'])
def add_deliveries():
    if request.method == 'POST':
        items_name = request.form['i_name']
        quantity_required = request.form['qty_req']
        quantity_delivered = request.form['qty_delivered']
        procuring_entity = request.form['proc_entity']
        receiver_name = request.form['r_name']
        receiver_contacts = request.form['r_contacts']
        new_deliveries = (items_name,quantity_required,quantity_delivered,procuring_entity,receiver_name,receiver_contacts)
        insert_deliveries(new_deliveries)
        flash("delivery added successfully",'success')
    return redirect(url_for('deliveries'))

@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")

app.run(debug=True)