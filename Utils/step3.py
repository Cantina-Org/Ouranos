import subprocess
from json import dumps
from os import system


def install_hermes_back(db, step2data: dict, step1data: dict):
    try:
        # Exécutez la commande "node -v" pour obtenir la version de Node.js
        subprocess.check_output(["node", "-v"])
        print("Node.js est installé.")
    except FileNotFoundError:
        return "Node.js n'est pas installé."
    except subprocess.CalledProcessError:
        return "Node.js est installé, mais une erreur s'est produite lors de l'exécution de la commande."

    db.create_table("""CREATE DATABASE IF NOT EXISTS cantina_hermes""")
    db.create_table("""CREATE TABLE IF NOT EXISTS cantina_hermes.messages_stats(author TEXT, public_message BIGINT, 
    private_message BIGINT, last_messages DATE NOT NULL DEFAULT current_timestamp)""")
    db.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""", ("hermes",
                                                                                            step2data["web_addr"]))

    system(f"cd {step2data['custom_path']} && git clone https://github.com/Cantina-Org/Hermes.git")
    system(f"cd {step2data['custom_path']}/Hermes && mkdir ./server/messages && "
           "mkdir ./server/messages/private-messages")
    system(f"cd {step2data['custom_path']}/Hermes && npm i")

    json_data = {
        "database": [{
            "database_username": step1data['username_db'],
            "database_password": step1data['password_db'],
            "database_addresse": step1data['address_db'],
            "database_port": step1data['port_db']
        }],
        "port": 3002
    }

    with open(step2data['custom_path'] + '/Hermes/server/config.json', "w") as outfile:
        outfile.write(dumps(json_data, indent=4))

    system(f"""echo '[Unit]
        Description=Cantina Hermes
        [Service]
        User=cantina
        WorkingDirectory={step2data['custom_path']}/Hermes/server
        ExecStart=python3 app.py
        [Install]
        WantedBy=multi-user.target' >> /etc/systemd/system/cantina-hermes.service""")
    system(f"chown cantina:cantina {step2data['custom_path']}/*/*/*/*")
    system("systemctl enable cantina-hermes")
    system("systemctl start cantina-hermes")

