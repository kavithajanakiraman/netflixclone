from flask import Flask, render_template, request,url_for,redirect
import sqlite3 as sql
from pytube import extract

app = Flask(__name__)
PIN = "8055"

@app.route('/')
def desktop():
    return render_template("index.html")

@app.route('/user')
def user():
    return render_template("user.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/submit", methods=["POST"])
def submit():
    input_PIN = request.form["PIN"]
    if input_PIN == PIN:
        return redirect(url_for("netflix"))
    else:
        return redirect(url_for("incorect_password"))

@app.route('/incorect_password')
def incorect_password():
    return render_template("incorrect.html")


@app.route('/netflix')
def netflix():
     conn=sql.connect("netflix.db")
     conn.row_factory=sql.Row
     cur=conn.cursor()
     cur.execute("select * from user")
     data=cur.fetchall()
     return render_template("netflix.html",data=data)


@app.route('/background')
def background():
     conn=sql.connect("netflix.db")
     conn.row_factory=sql.Row
     cur=conn.cursor()
     cur.execute("select * from user")
     data=cur.fetchall()
     return render_template("background.html",data=data)


@app.route('/videoplayer/<var>')
def videoplayer(var):
    return render_template("videoplayer.html",VAR=var)

@app.route('/upload', methods=(["POST","GET"]))
def upload():
    if request.method=="POST":
        vurl=request.form.get("vurl")
        videoid=extract.video_id(vurl)
        thumb=request.form.get("thumb")
        name=request.form.get("name")
        conn=sql.connect("netflix.db")
        cur=conn.cursor()
        cur.execute('insert into user(vurl,thumb,name)values(?,?,?)',(videoid,thumb,name))
        conn.commit()
        return redirect(url_for("netflix"))
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)