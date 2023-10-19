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

print("Bienvenue dans l'installateur de Cantina Olympe!")
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

if existing_instance:
    print("Une instance de Cantina a été trouvé dans la base de données.")
    wipe_db = input("Voullez vous supprimer les données de la base de données pour repartir de zéro? (Y/N)")
else:
    print("Aucune instance de Cantina a été trouvé. Poursuite de la procédure d'installation...")


print('''
------------------------------------------------------------------------------------------------------------------------
''')

web_address = input("Quelle est l'adresse internet de Cantina Olympe ? (example.example.com) ")
custom_path = input("Quelle est le repertoire de stockage de Olympe ? (Enter = répertoire actuelle + '/olympe/') "
                    "\nUn répertoire sera créer dans tout les cas!\n")

if custom_path == '':
    custom_path = getcwd()
    print(custom_path)

system(f"cd {custom_path} && git clone https://github.com/Cantina-Org/Olympe.git")

json_data = {
        "database": [{
            "database_username": db_data["username"],
            "database_password": db_data["password"],
            "database_addresse": db_data["address"],
            "database_port": db_data["port"]
        }],
        "port": 3000
    }

with open(custom_path + '/Olympe/config.json', "w") as outfile:
    outfile.write(dumps(json_data, indent=4))

system(f"""echo '[Unit]
    Description=Cantina Olympe
    [Service]
    User=cantina
    WorkingDirectory={custom_path}/Olympe
    ExecStart=python3 app.py
    [Install]
    WantedBy=multi-user.target' >> /etc/systemd/system/cantina-olympe.service""")

system(f"chown cantina:cantina {custom_path}/*/*/*")
system("systemctl enable cantina-olympe")
system("systemctl start cantina-olympe")
