from werkzeug.utils import secure_filename
from os import system


def install_nephelees_back(db, step2data: dict, step1data: dict):
    db.insert("""CREATE DATABASE IF NOT EXISTS cantina_nephelees""")
    db.insert("CREATE TABLE IF NOT EXISTS cantina_nephelees.file_sharing(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, "
              "file_name TEXT, file_owner text, file_short_name TEXT, login_to_show BOOL DEFAULT 1, password TEXT,"
              "date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")

    db.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""", ("nephelees",
                                                                                            step2data["web_addr"]))

    system(f"cd {step2data['custom_path']} && git clone https://github.com/Cantina-Org/Nephelees.git")

    json_data = {
        "database": [{
            "database_username": step1data['username_db'],
            "database_password": step1data['password_db'],
            "database_addresse": step1data['address_db'],
            "database_port": step1data['port_db']
        }],
        "port": 3002
    }
    with open(step2data['custom_path'] + '/Nephelees/config.json', "w") as outfile:
        outfile.write(dumps(json_data, indent=4))

    system("touch /etc/systemd/system/cantina-nephelees.service")
    system(f"""echo '[Unit]
    Description=Cantina Néphélées
    [Service]
    User=cantina
    WorkingDirectory={step2data['custom_path']}/Nephelees
    ExecStart=python3 app.py
    [Install]
    WantedBy=multi-user.target' >> /etc/systemd/system/cantina-nephelees.service""")
    system(f"chown cantina:cantina {step2data['custom_path']}/*/*/*")
    system("systemctl enable cantina-nephelees")
    system("systemctl start cantina-nephelees")


def install_hermes_back():
    # TODO: fonction hermes
    pass


def install_olympe_back(db, step2data: dict, step1data: dict):
    db.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""", ("olympe",
                                                                                            step2data["web_addr"]))

    system(f"cd {step2data['custom_path']} && git clone https://github.com/Cantina-Org/Olympe.git")

    json_data = {
        "database": [{
            "database_username": step1data['username_db'],
            "database_password": step1data['password_db'],
            "database_addresse": step1data['address_db'],
            "database_port": step1data['port_db']
        }],
        "port": 3000
    }
    with open(step2data['custom_path'] + '/Olympe/config.json', "w") as outfile:
        outfile.write(dumps(json_data, indent=4))

    system("touch /etc/systemd/system/cantina-olympe.service")
    system(f"""echo '[Unit]
        Description=Cantina Olympe
        [Service]
        User=cantina
        WorkingDirectory={step2data['custom_path']}/Olympe
        ExecStart=python3 app.py
        [Install]
        WantedBy=multi-user.target' >> /etc/systemd/system/cantina-olympe.service""")
    system(f"chown cantina:cantina {step2data['custom_path']}/*/*/*")
    system("systemctl enable cantina-olympe")
    system("systemctl start cantina-olympe")


def install_cerbere_back(db, step2data: dict, step1data: dict):
    db.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""", ("cerbere",
                                                                                            step2data["web_addr"]))

    system(f"cd {step2data['custom_path']} && git clone https://github.com/Cantina-Org/Cerbere.git")

    json_data = {
        "database": [{
            "database_username": step1data['username_db'],
            "database_password": step1data['password_db'],
            "database_addresse": step1data['address_db'],
            "database_port": step1data['port_db']
        }],
        "port": 3001
    }
    with open(step2data['custom_path'] + '/Cerbere/config.json', "w") as outfile:
        outfile.write(dumps(json_data, indent=4))

    system("touch /etc/systemd/system/cantina-cerbere.service")
    system(f"""echo '[Unit]
        Description=Cantina Cerbere
        [Service]
        User=cantina
        WorkingDirectory={step2data['custom_path']}/Cerbere
        ExecStart=python3 app.py
        [Install]
        WantedBy=multi-user.target' >> /etc/systemd/system/cantina-cerbere.service""")
    system(f"chown cantina:cantina {step2data['custom_path']}/*/*/*")
    system("systemctl enable cantina-cerbere")
    system("systemctl start cantina-cerbere")
