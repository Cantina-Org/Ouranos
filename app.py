from flask import Flask, render_template, redirect, url_for, request
from Utils.database import DataBase
from Utils.step_1 import createDatabaseStep1
from Utils.step3 import *
from argon2 import PasswordHasher
from os import geteuid

app = Flask(__name__)
ph = PasswordHasher()
db = None
toolToInstall = []
step1Info = {}


@app.route('/')
def home():
    return redirect(url_for("step1"))


@app.route('/step1', methods=["POST", "GET"])
def step1():
    global db, step1Info
    if request.method == "POST":
        try:
            db = DataBase(user=request.form["username_db"], password=request.form["password_db"],
                          host=request.form["address_db"], port=int(request.form["port_db"]))
            db.connection()
            createDatabaseStep1(database=db)
            # Sauvegarde des infos données dans le formulaire.
            for i in request.form:
                step1Info[i] = request.form[i]

            return redirect(url_for("step2"))

        except Exception as e:
            print(e)
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

        return redirect(url_for("install_cerbere"))
    else:
        return render_template("install_olympe.html")


@app.route('/step2/config/cerbere', methods=['POST', 'GET'])
def install_cerbere():
    global toolToInstall
    if request.method == "POST":
        config = {}
        if "custom_path_switch" in request.form and "custom_path_input" in request.form:
            config['custom_path'] = request.form["custom_path_input"]
        config["web_addr"] = request.form["web_addr"]

        toolToInstall.append({"name": "cerbere", "config": config})

        return redirect(url_for("step3"))
    else:
        return render_template("install_cerbere.html")


@app.route('/step3')
def step3():
    # Création de l'utilisateur linux
    system("sudo adduser cantina --system")
    system("sudo addgroup cantina")
    system("sudo usermod -a -G cantina cantina")

    # Création de l'utilisateur
    new_uuid = str(uuid3(uuid1(), str(uuid1())))
    new_salt = new('sha256').hexdigest()

    db.insert('''INSERT INTO cantina_administration.user(token, user_name, salt, password, admin) VALUES 
    (%s, %s, %s, %s, %s)''', (new_uuid, step1Info["name"], new_salt, ph.hash(step1Info["passw"]), 1))

    for item in toolToInstall:
        if item["name"] == "nephelees":
            if item["config"]["custom_path"]:
                install_nephelees_back(db, item["config"], step1Info)
            else:
                item["config"]["custom_path"] = "/home/cantina/"
                install_nephelees_back(db, item["config"], step1Info)

        elif item["name"] == "hermes":
            if item["config"]["custom_path"]:
                install_hermes_back(db, item["config"], step1Info)
            else:
                install_hermes_back(db, item["config"], step1Info)

        elif item["name"] == "olympe":
            if item["config"]["custom_path"]:
                install_olympe_back(db, item["config"], step1Info)
            else:
                item["config"]["custom_path"] = "/home/cantina/"
                install_olympe_back(db, item["config"], step1Info)

        elif item["name"] == "cerbere":
            if item["config"]["custom_path"]:
                install_cerbere_back(db, item["config"], step1Info)
            else:
                item["config"]["custom_path"] = "/home/cantina/"
                install_cerbere_back(db, item["config"], step1Info)

    return "En théorie c'est bon"


if __name__ == '__main__':
    if geteuid() != 0:
        exit("Vous devez avoir les privilèges de root pour exécuter ce script.\nVeuillez réessayer, en utilisant cette "
             "fois 'sudo'.")
    app.run()
