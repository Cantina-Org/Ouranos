from flask import Flask, render_template, redirect, url_for, request
from Utils.database import DataBase
from Utils.step_1 import createDatabaseStep1

app = Flask(__name__)
db = None


@app.route('/')
def home():
    return redirect(url_for("step1"))


@app.route('/step1', methods=["POST", "GET"])
def step1():
    global db
    if request.method == "POST":
        try:
            db = DataBase(user=request.form["username_db"], password=request.form["password_db"],
                          host=request.form["address_db"], port=int(request.form["port_db"]))
            db.connection()
            createDatabaseStep1(database=db)
            return redirect(url_for("step2"))
        except Exception as e:
            return redirect(url_for('step1', error="error_db"))
    else:
        return render_template('install.html')


@app.route('/step2')
def step2():
    return ""


if __name__ == '__main__':
    app.run()
