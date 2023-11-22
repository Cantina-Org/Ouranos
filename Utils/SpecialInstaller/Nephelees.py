from json import dumps


def create_nephelees_database(database):
    database.create_table("""CREATE DATABASE IF NOT EXISTS cantina_nephelees""")
    database.create_table("CREATE TABLE IF NOT EXISTS cantina_nephelees.file_sharing("
                          "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, file_name TEXT, file_owner text, "
                          "file_short_name TEXT, login_to_show BOOL DEFAULT 1, password TEXT, "
                          "date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")


def create_nephelees_app(database: object, web_addr: str, db_data: str, custom_path: dict):
    database.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""",
                    ("nephelees", web_addr))

    json_data = {
        "database": [{
            "database_username": db_data["username"],
            "database_password": db_data["password"],
            "database_address": db_data["address"],
            "database_port": db_data["port"]
        }],
        "port": 3002
    }

    with open(str(custom_path) + f'/Nephelees/config.json', "w") as outfile:
        outfile.write(dumps(json_data, indent=4))
