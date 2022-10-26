from flask import Flask, request, redirect, render_template, session, url_for
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "website"
)
mycursor = mydb.cursor()

app = Flask(__name__, static_folder="public", static_url_path="/")  
app.secret_key = "noOneKnows"
# 這是註解

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/signup', methods = ['POST', "GET"])
def signup():
    name = request.form["name"]
    user = request.form["user"]
    password = request.form["password"]

    sql = "SELECT username FROM member WHERE username = %s"
    val = (user,)
    mycursor.execute(sql, val)
    myResult = mycursor.fetchone()
    if myResult == None:
        sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
        val = (name, user, password)
        mycursor.execute(sql, val)
        mydb.commit()
        session["username"] = user
        session["name"] = name
        return redirect("/member")
        
    else:
        return redirect("/error?message=帳號已經被註冊")
        
    

@app.route("/signin", methods = ["POST", "GET"])
def signin():
    user = request.form["user"]
    password = request.form["password"]
    if user == "" or password == "":
        return redirect("/error?message=帳號、或密碼輸入錯誤")

    sql = "SELECT username, password, name FROM member WHERE username = %s"
    val = (user,)
    mycursor.execute(sql, val)
    myResult = mycursor.fetchone()

    if myResult == None:
        return redirect("/error?message=帳號、或密碼輸入錯誤")
    
    if password == myResult[1]:
        session["username"] = user
        session["name"] = myResult[2]
        return redirect("/member")
    else:
        return redirect("/error?message=帳號、或密碼輸入錯誤")

        

@app.route("/member")
def member():
    if "username" in session:
        name = session["name"]
        return render_template("member.html", name = name)
    else:
        return redirect("/")

@app.route("/error")
def error():
    mseg = request.args.get("message")
    return render_template("error.html", message = mseg)


@app.route("/signout")
def signout():
    session.pop("username", None)
    session.pop("name", None)
    return redirect("/")



# 啟動網站伺服器
app.run(port=3000)



