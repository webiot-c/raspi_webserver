from flask import *
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html");

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
            address = request.form["address"]
            with sqlite3.conect("employee.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Employees (name, email, address) values (?,?,?)",(name,email,address))
                con.commit()
                msg = "EMployee successfully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"

        finally:
            return render_template("success.html", msg = msg)
            con.close()

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/deleterecord", methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("employee.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Employees where id = ?", id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)

if __name__ == "__main__":
    app.run(debug =True)