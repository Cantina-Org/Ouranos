from os import system, getcwd
from json import dumps
from Utils.database import DataBase
from Utils.create_database import create_administration_database

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
db_data["username"] = 'cantina'  # input("Quelle est le nom d'utilisateur de la base de donnée : ")
db_data["password"] = 'LeMdPDeTest'  # input("Quelle est le mots de passe de la base de donnée : ")
db_data["address"] = '127.0.0.1'  # input("Quelle est l'addresse de la base de donnée : ")
db_data["port"] = 3306  # int(input("Quelle est le port d'accès de la base de donnée: "))

print(db_data)
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

print("Une instance de Cantina a été retrouvé dans la base de données.")
wipe_db = input("Voulez vous réutiliser cette base de donnée? (Y/N) ")

while wipe_db not in ['Y', 'y', 'yes', 'N', 'n', 'no']:
    wipe_db = input("Voulez vous réutiliser cette base de donnée? (Y/N) ")

if wipe_db in ['N', 'n', 'no']:
    print('Suppression de la base de donnée cantina_administration...')
    database.insert('''DROP DATABASE cantina_administration''', ())
    print('Création de la nouvelle base de donnée cantina_administration...')
    create_administration_database(database)
else:
    print('Les informations de connexion à Cantina seront les mêmes que ceux déjà définie.')

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
