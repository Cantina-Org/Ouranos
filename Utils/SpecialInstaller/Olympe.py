from json import dumps


def create_olympe_database(database):
    database.create_table("""CREATE DATABASE IF NOT EXISTS cantina_administration""")
    database.create_table("""CREATE TABLE IF NOT EXISTS cantina_administration.user(id INT PRIMARY KEY NOT NULL 
        AUTO_INCREMENT, token TEXT, user_name TEXT, password TEXT, admin BOOL, work_Dir text, 
        last_online TEXT)""")
    database.create_table("""CREATE TABLE IF NOT EXISTS  cantina_administration.log(id INT PRIMARY KEY NOT NULL 
        AUTO_INCREMENT, name TEXT, user_ip TEXT, user_token TEXT, argument TEXT, log_level INT, date TIMESTAMP DEFAULT 
        current_timestamp)""")
    database.create_table("""CREATE TABLE IF NOT EXISTS  cantina_administration.domain(id int PRIMARY KEY NOT NULL 
        AUTO_INCREMENT, name TEXT, fqdn TEXT)""")
    database.create_table("""CREATE TABLE IF NOT EXISTS  cantina_administration.config(id INT PRIMARY KEY NOT NULL 
        AUTO_INCREMENT, name TEXT, content TEXT)""")


def create_olympe_app(database, web_addr, custom_path, db_data):
    database.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""",
                    ("olympe", web_addr))

    json_data = {
        "database": [{
            "database_username": db_data["username"],
            "database_password": db_data["password"],
            "database_address": db_data["address"],
            "database_port": db_data["port"]
        }],
        "port": 3000
    }

    with open(str(custom_path) + f'/Olympe/config.json', "w") as outfile:
        outfile.write(dumps(json_data, indent=4))
