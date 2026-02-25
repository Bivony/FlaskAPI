from flask import*
import pymysql


#intialize flask

app=Flask(__name__)
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















app.run(debug=True)