from flask import Flask, request, session, redirect, render_template
from pymongo import MongoClient
from werkzeug.security import check_password_hash , generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key="@2006#alvin"


MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["taskmanager"]
users = db["users"]


@app.route('/')
def home():
    return render_template("home.html")



@app.route("/register", methods=["POST","GET"])
def signup():
    if(request.method=="POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        if(users.find_one({"username":username})):
            return render_template("error.html",error="The user already Exits ! Please Log In")
        hashpassword = generate_password_hash(password)
        user = {"username":username , "Password":hashpassword}
        users.insert_one(user)
        return redirect("/login")
    else:
        return render_template("register.html")



@app.route("/login",methods=["POST","GET"])
def login():
        if(request.method=="POST"): 
            username = request.form.get('username')
            password = request.form.get('password')
            user = users.find_one({"username": username})
            if user and check_password_hash(user["Password"],password):
                session["username"]=username
                return redirect('/dashboard')
            else:
                return render_template("error.html",error="Invaild username or password !")
        else:
            return render_template("login.html")


@app.route("/dashboard")
def dash():
    if("username"in session):
        return render_template("dashboard.html",name=session["username"])
    else:
        return redirect("/login")
    
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return redirect("/")    


@app.route("/reset",methods=["POST","GET"])
def resetpassword():
        if(request.method=="POST"):
            username = request.form.get("username")
            user = users.find_one({"username":username})
            if (user):
                newpassword = request.form.get("newpassword")
                newhash_password = generate_password_hash(newpassword)
                users.update_one(
                {"username": username},
                {"$set": {"Password": newhash_password}}
                )
                return redirect("/login")
            else:
                return render_template("error.html",error="Usernmae Not found !")
        else:    
            return render_template("resetpassword.html")    



if(__name__=="__main__"):
    app.run(debug=True)