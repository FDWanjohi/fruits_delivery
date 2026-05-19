import psycopg2
conn = psycopg2.connect(host='localhost',port=5432,user='postgres',password='Thrill254.',dbname='fruits_db')
cur = conn.cursor()

def get_deliveries():
    cur.execute("select * from deliveries")
    deliveries = cur.fetchall()
    return deliveries

def insert_deliveries(delivery_details):
    cur.execute("insert into deliveries(item_name,quantity_required,quantity_delivered,procuring_entity,receiver_name,receiver_contacts)values(%s,%s,%s,%s,%s,%s)",delivery_details)
    conn.commit()

def insert_user(user_details):
    cur.execute("insert into users(full_name,email,phone_number,password)values(%s,%s,%s,%s)",user_details)
    conn.commit()

def check_user_exists(email):
    cur.execute("select * from users where email = %s",(email,))
    user_data = cur.fetchone()
    return user_data


