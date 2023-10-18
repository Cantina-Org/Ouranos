from os import system, getcwd
from json import dumps
from Utils.database import DataBase

db_data = {}


print('''  ______     ___      .__   __. .___________. __  .__   __.      ___      
 /      |   /   \     |  \ |  | |           ||  | |  \ |  |     /   \     
|  ,----'  /  ^  \    |   \|  | `---|  |----`|  | |   \|  |    /  ^  \    
|  |      /  /_\  \   |  . `  |     |  |     |  | |  . `  |   /  /_\  \   
|  `----./  _____  \  |  |\   |     |  |     |  | |  |\   |  /  _____  \  
 \______/__/     \__\ |__| \__|     |__|     |__| |__| \__| /__/     \__\ ''')

print("Bienvenue dans l'installateur de Cantina Néphélees!")
print('''
------------------------------------------------------------------------------------------------------------------------
''')
db_data["username"] = input("Quelle est le nom d'utilisateur de la base de donnée : ")
db_data["password"] = input("Quelle est le mots de passe de la base de donnée : ")
db_data["address"] = input("Quelle est l'addresse de la base de donnée : ")
db_data["port"] = int(input("Quelle est le port d'accès de la base de donnée: "))

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
        exit("Merci de d'abords installer l'outils Olympe!")

print("Une instance de Cantina a été retrouvé dans la base de données. Poursuite de la procédure...")


print('''
------------------------------------------------------------------------------------------------------------------------
''')

web_address = input("Quelle est l'adresse internet de Cantina Néphélées ? (example.example.com) ")
custom_path = input("Quelle est le repertoire de stockage de Néphélées ? (Enter = répertoire actuelle + '/Nephelees/') "
                    "\nUn répertoire sera créer dans tout les cas!\n")

if custom_path == '':
    custom_path = getcwd()
    print(custom_path)

system(f"cd {custom_path} && git clone https://github.com/Cantina-Org/Nephelees.git")

json_data = {
        "database": [{
            "database_username": db_data["username"],
            "database_password": db_data["password"],
            "database_addresse": db_data["address"],
            "database_port": db_data["port"]
        }],
        "port": 3002
    }

with open(custom_path + '/Nephelees/config.json', "w") as outfile:
    outfile.write(dumps(json_data, indent=4))

system(f"""echo '[Unit]
    Description=Cantina Néphélées
    [Service]
    User=cantina
    WorkingDirectory={custom_path}/Nephelees
    ExecStart=python3 app.py
    [Install]
    WantedBy=multi-user.target' >> /etc/systemd/system/cantina-nephelees.service""")

system(f"chown cantina:cantina {custom_path}/*/*/*")
system("systemctl enable cantina-nephelees")
system("systemctl start cantina-nephelees")
