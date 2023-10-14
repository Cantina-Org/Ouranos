from Utils.database import DataBase

db_data = {}


print('''  ______     ___      .__   __. .___________. __  .__   __.      ___      
 /      |   /   \     |  \ |  | |           ||  | |  \ |  |     /   \     
|  ,----'  /  ^  \    |   \|  | `---|  |----`|  | |   \|  |    /  ^  \    
|  |      /  /_\  \   |  . `  |     |  |     |  | |  . `  |   /  /_\  \   
|  `----./  _____  \  |  |\   |     |  |     |  | |  |\   |  /  _____  \  
 \______/__/     \__\ |__| \__|     |__|     |__| |__| \__| /__/     \__\ ''')

print("Bienvenue dans l'installateur de Cantina Néphélees!")

db_data["username"] = input("Quelle est le nom d'utilisateur de la base de donnée : ")
db_data["password"] = input("Quelle est le mots de passe de la base de donnée : ")
db_data["address"] = input("Quelle est l'addresse de la base de donnée : ")
db_data["port"] = int(input("Quelle est le port d'accès de la base de donnée: "))

print(db_data)
database = DataBase(host=db_data["address"], port=db_data["port"], user=db_data["username"],
                    password=db_data['password'])
try:
    database.connection()
except ConnectionRefusedError:
    exit('Une erreur est survenue lors de la connexion à MariaDB/MySQL!')
