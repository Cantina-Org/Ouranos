from flask import Flask, render_template, redirect, url_for, request
from Utils.database import DataBase
from Utils.step_1 import createDatabaseStep1

app = Flask(__name__)
db = None
toolToInstall = []


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
        return render_template('step1.html')


@app.route('/step2', methods=["POST", "GET"])
def step2():
    global toolToInstall
    if request.method == "POST":
        try:
            # Check value pour savoir quelle étape afficher ensuite.
            print(request.form["nephelees"])
            if request.form['nephelees'] == "on":
                toolToInstall.append({"name": "nephelees", "config": {}})
            if request.form['hermes'] == "on":
                toolToInstall.append({"name": "hermes", "config": {}})
            return redirect(url_for('install_nephelees'))
        except Exception as e:
            print(e)
            return redirect(url_for('step2', error="error_db"))
    else:
        return render_template('step2.html')


@app.route('/step2/config/nephelees', methods=['POST', 'GET'])
def install_nephelees():
    if request.method == "POST":
        print("")
    else:
        print(toolToInstall)
        for item in toolToInstall:
            if item["name"] == "nephelees":
                return render_template('install_nephelees.html')

        return redirect(url_for("step3"))


@app.route('/step3')
def step3():
    return toolToInstall


if __name__ == '__main__':
    app.run()
