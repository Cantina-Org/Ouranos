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
        toolToInstall = []
        try:
            if "nephelees" in request.form:
                toolToInstall.append({"name": "nephelees", "config": {}})
            if "hermes" in request.form:
                toolToInstall.append({"name": "hermes", "config": {}})
            return redirect(url_for('install_nephelees'))
        except Exception as e:
            print(e)
            return redirect(url_for('step2', error="error_db"))
    else:
        return render_template('step2.html')


@app.route('/step2/config/nephelees', methods=['POST', 'GET'])
def install_nephelees():
    global toolToInstall
    if request.method == "POST":
        config = {}
        if "custom_path_switch" in request.form and "custom_path_input" in request.form:
            config['custom_path'] = request.form["custom_path_input"]
        config["web_addr"] = request.form["web_addr"]
        for item in toolToInstall:
            if item["name"] == "nephelees":
                item["config"] = config

        return redirect(url_for("install_hermes"))
    else:
        for item in toolToInstall:
            if item["name"] == "nephelees":
                return render_template('install_nephelees.html')

        return redirect(url_for("install_hermes"))


@app.route('/step2/config/hermes', methods=['POST', 'GET'])
def install_hermes():
    global toolToInstall
    if request.method == "POST":
        config = {}
        if "custom_path_switch" in request.form and "custom_path_input" in request.form:
            config['custom_path'] = request.form["custom_path_input"]
        config["web_addr"] = request.form["web_addr"]
        for item in toolToInstall:
            if item["name"] == "hermes":
                item["config"] = config

        return redirect(url_for("install_olympe"))
    else:
        for item in toolToInstall:
            if item["name"] == "hermes":
                return render_template('install_hermes.html')

        return redirect(url_for("install_olympe"))


@app.route('/step2/config/olympe', methods=['POST', 'GET'])
def install_olympe():
    global toolToInstall
    if request.method == "POST":
        config = {}
        if "custom_path_switch" in request.form and "custom_path_input" in request.form:
            config['custom_path'] = request.form["custom_path_input"]
        config["web_addr"] = request.form["web_addr"]

        toolToInstall.append({"name": "olympe", "config": config})

        return toolToInstall
    else:
        return render_template("install_hermes.html")


@app.route('/step3')
def step3():
    return toolToInstall


if __name__ == '__main__':
    app.run()
