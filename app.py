from flask import*
import pymysql
import os         


#intialize flask

app=Flask(__name__)
if not os.path.exists("static/images"):
   os.makedirs("static/images")  
app.config["UPLOAD_FOLDER"]="static/images"
@app.route("/api/signup",methods=["POST"])
def signup():
    #request user input
    username=request.form["username"]
    email=request.form["email"]
    password=request.form["password"]
    phone=request.form["phone"]

    #create connection to database
    connection=pymysql.connect(host="localhost",user="root",password="",database="tembo_sokogarden_bivony")

    #create a cursor
    cursor=connection.cursor()

    # create sql statement to insert trhe data
    sql="insert into users(username,email,password,phone)values(%s,%s,%s,%s)"
    data=(username,email,password,phone)

    #execute/run
    cursor.execute(sql,data)
    #commit/save

    connection.commit()

    #response
    return jsonify({'Message':"Thank you for joining"})

#signin api 
#signin route
@app.route("/api/signin",methods=["POST"])
def signin():
    #request users input
    email=request.form['email']
    password=request.form['password']
    
    #create a connection
    Connection=pymysql.connect(host='localhost',user="root",password="",database="tembo_sokogarden_bivony")

    #create a cursor

    cursor=Connection.cursor(pymysql.cursors.DictCursor)

    #sql statement to check if user exists
    sql="select * from users where email=%s and password=%s"

    #prepare data
    data=(email,password)

    cursor.execute(sql,data)

    #response 
    if cursor.rowcount==0:
     return jsonify({"Message":"Login failed"})
    else:
       user=cursor.fetchone()
       user.pop("password",None)
       return jsonify({"Message":"Login success","user":user})

#add product api
@app.route("/api/add_product",methods=["POST"])
def add_product():
   #request user input
   product_name=request.form["product_name"]
   product_descripition=request.form["product_description"]
   product_cost=request.form["product_cost"]
   product_photo=request.files["product_photo"]

   #extract image name
   filename=product_photo.filename

   photo_path=os.path.join(app.config["UPLOAD_FOLDER"],filename)
   product_photo.save(photo_path)


   #create connection
   connection=pymysql.connect(host="localhost",user="root",password="",database="tembo_sokogarden_bivony")

   #create cursor
   cursor=connection.cursor()

   #sql statement to insert the records
   sql="insert into product_details(product_name,product_description,product_cost,product_photo)values(%s,%s,%s,%s)"

   #prepare data
   data=(product_name,product_descripition,product_cost,filename)

   #execute/run
   cursor.execute(sql,data)

   #commit/save
   connection.commit()

   #response
   return jsonify({"Message":"Product added successfully"})

 #api get product

 #create root
@app.route("/api/get_product")

 #create function
def get_product():

 #create connection to mysql database
   connection=pymysql.connect(host="localhost",user="root",password="",database="tembo_sokogarden_bivony")

 #create cursor
   cursor=connection.cursor(pymysql.cursors.DictCursor)

   #create sql statement
   sql="select*from product_details"

   #execute/run
   cursor.execute(sql)

 #fetch
   product=cursor.fetchall()

 #response
   return jsonify(product)






#mpesa api
# Mpesa Payment Route/Endpoint 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})









































app.run(debug=True)