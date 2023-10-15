import os

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
    custom_path = os.getcwd()
    print(custom_path)
