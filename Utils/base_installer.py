from json import dumps
from os import system, getcwd, geteuid, path, sep
from uuid import uuid3, uuid1
from rich import print_json
from InquirerPy import inquirer
from InquirerPy.validator import NumberValidator
from argon2 import PasswordHasher
from unidecode import unidecode
from Utils.database import DataBase
from importlib import util

ph = PasswordHasher()


def default_welcome_message():
    print('''  ______     ___      .__   __. .___________. __  .__   __.      ___      
 /      |   /   \     |  \ |  | |           ||  | |  \ |  |     /   \     
|  ,----'  /  ^  \    |   \|  | `---|  |----`|  | |   \|  |    /  ^  \    
|  |      /  /_\  \   |  . `  |     |  |     |  | |  . `  |   /  /_\  \   
|  `----./  _____  \  |  |\   |     |  |     |  | |  |\   |  /  _____  \  
 \______/__/     \__\ |__| \__|     |__|     |__| |__| \__| /__/     \__\ ''')

    if geteuid() != 0:
        exit("Le script doit être lancée avec une permission d'administrateur!")
    else:
        print(geteuid())


def database_connection(module):
    db_data = {"username": inquirer.text(message="Nom d'utilisateur de la base de données :").execute(),
               "password": inquirer.secret(message="Mot de passe de la base de données :").execute(),
               "address": inquirer.text(message="Adresse de la base de données :").execute(),
               "port": inquirer.number(message="Port de la basse de donnée :", validate=NumberValidator()).execute()}

    print_json(dumps(db_data))

    database = DataBase(host=db_data["address"], port=int(db_data["port"]), user=db_data["username"],
                        password=db_data['password'])

    try:
        database.connection()
    except ConnectionRefusedError:
        exit('Une erreur est survenue lors de la connexion à MariaDB/MySQL!')

    data = database.select('SHOW DATABASES')
    already_an_instance = False

    for db in data:
        if db[0] == 'cantina_administration':
            already_an_instance = True

    if not already_an_instance and module == "Olympe":
        print("Création de la base de données...")

        import_and_execute_installer_module('Olympe', 'create_olympe_database', database)

        print("Création du premier utilisateur :")
        new_uuid = str(uuid3(uuid1(), str(uuid1())))
        user_data = {"username": inquirer.text(message="Nom d'utilisateur Cantina :").execute(),
                     "password": inquirer.secret(message="Mot de passe de l'utilisateur Cantina :").execute(),
                     "verif_password": inquirer.secret(message="Mot de passe de l'utilisateur Cantina :").execute()}

        while user_data["password"] != user_data["verif_password"]:
            print("Les deux mots de passe ne correspondent pas!")
            user_data = {"username": inquirer.text(message="Nom d'utilisateur Cantina :").execute(),
                         "password": inquirer.secret(message="Mot de passe de l'utilisateur Cantina :").execute(),
                         "verif_password": inquirer.secret(message="Mot de passe de l'utilisateur Cantina :").execute()}

        database.insert('''INSERT INTO cantina_administration.user(token, user_name, password, admin, work_Dir) 
        VALUES (%s, %s, %s, %s, %s)''', (new_uuid, user_data["username"],  ph.hash(user_data["password"]), 1, None))

    elif not already_an_instance and module != "Olympe":
        exit("Merci de d'abord installer l'outils Olympe !")

    elif already_an_instance and module != "Olympe":
        globals()['create_' + unidecode(str.lower(module)) + '_database'](database, )

    print("Une instance de Cantina a été retrouvée dans la base de données. Poursuite de la procédure...")
    print('''
    ------------------------------------------------------------------------------------------------------------------------
    ''')

    return database, db_data


def create_app(database, db_data, module):
    web_address = inquirer.text(message=f"Adresse de l'application Cantina {module} ? ({module.casefold()}.example"
                                        f".com) ?").execute()
    custom_path = inquirer.filepath(message=f"Où seront stockés les données de Cantina {module} ? (Enter = {getcwd()}/"
                                            f"{module}/)").execute()

    database.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""",
                    (f"{module.casefold()}", web_address))

    if custom_path == '':
        custom_path = getcwd()
        print(custom_path)

    system(f"cd {custom_path} && git clone https://github.com/Cantina-Org/{module}.git")

    json_data = {
            "database": [{
                "database_username": db_data["username"],
                "database_password": db_data["password"],
                "database_address": db_data["address"],
                "database_port": db_data["port"]
            }],
            "port": 3002
        }

    with open(str(custom_path) + f'/{module}/config.json', "w") as outfile:
        outfile.write(dumps(json_data, indent=4))

    system(f"""echo '[Unit]
        Description=Cantina {module}
        [Service]
        User=cantina
        WorkingDirectory={custom_path}/{module}
        ExecStart=python3 app.py
        [Install]
        WantedBy=multi-user.target' >> /etc/systemd/system/cantina-{module.casefold()}.service""")

    system(f"chown cantina:cantina {custom_path}/*/*/*")
    system(f"systemctl enable cantina-{module.casefold()}")
    system(f"systemctl start cantina-{module.casefold()}")


def import_and_execute_installer_module(file_name, module_name, database):
    chemin_du_fichier = 'Utils.SpecialInstaller.' + file_name

    try:
        # Importez le module dynamiquement
        module_spec = util.find_spec(chemin_du_fichier)
        module = util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        # Vérifiez si la fonction spécifiée existe dans le module
        if hasattr(module, module_name) and callable(getattr(module, module_name)):
            # Obtenez la référence de la fonction et appelez-la
            fonction = getattr(module, module_name)
            if module_name.endswith('_database'):
                fonction(database)
            else:
                pass
        else:
            print("La fonction spécifiée n'existe pas dans le module.")
    except ImportError as e:
        print("Impossible d'importer le module ou l'attribut spécifié. " + str(e))
