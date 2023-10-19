from os import system, getcwd, geteuid
from json import dumps
from Utils.database import DataBase

db_data = {}


print('''  ______     ___      .__   __. .___________. __  .__   __.      ___      
 /      |   /   \     |  \ |  | |           ||  | |  \ |  |     /   \     
|  ,----'  /  ^  \    |   \|  | `---|  |----`|  | |   \|  |    /  ^  \    
|  |      /  /_\  \   |  . `  |     |  |     |  | |  . `  |   /  /_\  \   
|  `----./  _____  \  |  |\   |     |  |     |  | |  |\   |  /  _____  \  
 \______/__/     \__\ |__| \__|     |__|     |__| |__| \__| /__/     \__\ ''')

print("Bienvenue dans l'installateur de Cantina Cerbere!")

if geteuid() == 0:
    exit("Le script doit être lancée avec une permission d'administrateur!")

print('''
------------------------------------------------------------------------------------------------------------------------
''')
db_data["username"] = input("Quel est le nom d'utilisateur de la base de données : ")
db_data["password"] = input("Quel est le mot de passe de la base de données : ")
db_data["address"] = input("Quelle est l'addresse de la base de données : ")
db_data["port"] = int(input("Quel est le port d'accès de la base de données : "))

database = DataBase(host=db_data["address"], port=db_data["port"], user=db_data["username"],
                    password=db_data['password'])
try:
    database.connection()
except ConnectionRefusedError:
    exit('Une erreur est survenue lors de la connexion à MariaDB/MySQL!')

data = database.select('SHOW DATABASES')
existing_instance = False

for db in data:
    if db[0] == 'cantina_administration':
        existing_instance = True
        break
    else:
        existing_instance = False
        exit("Merci de d'abord installer l'outil Olympe !")

print("Une instance de Cantina a été retrouvée dans la base de données. Poursuite de la procédure...")


print('''
------------------------------------------------------------------------------------------------------------------------
''')

web_address = input("Quelle est l'adresse internet de Cantina Cerbere ? (example.example.com) ")
custom_path = input("Quel est le répertoire de stockage de Cerbere ? (Enter = répertoire actuelle + '/Cerbere/') "
                    "\nUn répertoire sera créé dans tout les cas!\n")

database.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""",
                ("cerbere", web_address))

if custom_path == '':
    custom_path = getcwd()
    print(custom_path)

system(f"cd {custom_path} && git clone https://github.com/Cantina-Org/Cerbere.git")

json_data = {
        "database": [{
            "database_username": db_data["username"],
            "database_password": db_data["password"],
            "database_addresse": db_data["address"],
            "database_port": db_data["port"]
        }],
        "port": 3002
    }

with open(custom_path + '/Cerbere/config.json', "w") as outfile:
    outfile.write(dumps(json_data, indent=4))

system(f"""echo '[Unit]
    Description=Cantina Cerbere
    [Service]
    User=cantina
    WorkingDirectory={custom_path}/Cerbere
    ExecStart=python3 app.py
    [Install]
    WantedBy=multi-user.target' >> /etc/systemd/system/cantina-cerbere.service""")

system(f"chown cantina:cantina {custom_path}/*/*/*")
system("systemctl enable cantina-cerbere")
system("systemctl start cantina-cerbere")
