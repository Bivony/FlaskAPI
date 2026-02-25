from flask import *

#intialize the flask app
app=Flask(__name__)

#define the route
@app.route("/api/home")
def home():
    return jsonify( {"Message":"Welcome to home api"})

#create route for product
@app.route('/api/product')
def product():
    return jsonify({"Message":"Welcome to product Api"})

#create route for service
@app.route('/api/service')
def service():
    return jsonify({"Message":"Welcome to Our Services API"})

#creating an route to accept user input
@app.route("/api/calc",methods=["POST"])
def calc():
    num1=request.form["num1"]
    num2=request.form["num2"]

    SUM=int(num1)+int(num2)

    return jsonify({"answer":SUM})

#create route for 2 number multiply
@app.route("/api/mult",methods=["POST"])
def mult():
    num1=request.form["num1"]
    num2=request.form["num2"]

    mult=int(num1)*int(num2) 
    return jsonify({"answer":mult})

#floor 
@app.route("/api/floor",methods=["post"])
def floor():
    num1=request.form["num1"]
    num2=request.form["num2"]
    floor=int(num1)//int(num2)
    return jsonify({"answer":floor})

app.run(debug=True)

