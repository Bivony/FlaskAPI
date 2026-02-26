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













































app.run(debug=True)