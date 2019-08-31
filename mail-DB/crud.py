from flask import *
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/savedetails", methods = ["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            print(name)
            print(email)
            print("sqlの部分")
            conn = sqlite3.connect('mail.db')
            c = conn.cursor()  # sql実行のためのcursorオブジェクト生成
            #c.execute("INSERT into data(?,?) VALUES(name, email)")
            p = "INSERT INTO data(name, email) VALUES(?, ?)"
            c.execute(p, (name, email))

            conn.commit()
            print("commit")
            msg = "データ保存しました。やったぜ！"
            conn.close()
            print("close")


        finally:
            return render_template("success.html", msg = msg)

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/deleterecord", methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("mail.db") as con:
        try:
            c = con.cursor()
            c.execute("delete from data where id = ?", id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)

if __name__ == "__main__":
    app.run(debug =True)