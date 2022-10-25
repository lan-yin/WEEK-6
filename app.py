from flask import Flask, request, redirect, render_template, session, url_for
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root@2022",
    database = "website"
)
mycursor = mydb.cursor()

app = Flask(__name__, static_folder="public", static_url_path="/")  
app.secret_key = "noOneKnows"


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/signup', methods = ['POST', "GET"])
def signup():
    name = request.form["name"]
    user = request.form["user"]
    password = request.form["password"]

    if checkUser(user):
        return redirect("/error?message=帳號已經被註冊")
    else:
        addUser(name, user, password)
        session["username"] = user
        return redirect("/member")
    

@app.route("/signin", methods = ["POST", "GET"])
def signin():
    user = request.form["user"]
    password = request.form["password"]
    if checkMember(user, password):
        session["username"] = user
        name = getName(user)
        return redirect("/member")
    else:
        return redirect("/error?message=帳號、或密碼輸入錯誤")

@app.route("/member")
def member():
    if "username" in session:
        username = session["username"]
        if checkUser(username):
            name = getName(username)
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
    return redirect("/")



def checkUser(user):
    mycursor.execute("SELECT username FROM member")
    myData = mycursor.fetchall()
    user_list = []
    for x in myData:
        user_list.extend(x)
    if user in user_list:
        return True
    else:
        return False

def addUser(name, user, password):
    sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
    val = (name, user, password)
    mycursor.execute(sql, val)
    mydb.commit()


def checkMember(user, password):
    if checkUser(user):
        mycursor.execute("SELECT username, password FROM member WHERE username='"+ user +"'")
        myresult = mycursor.fetchone()
        if password == myresult[1]:
            return True
    else:
        return False

def getName(user):
    mycursor.execute("SELECT name FROM member WHERE username='"+ user +"'")
    myresult = mycursor.fetchone()
    return myresult[0]

# 啟動網站伺服器
app.run(port=3000)



