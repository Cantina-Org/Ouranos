from json import dumps


def create_cerbere_database(database):
    pass


def create_cerbere_app(database: object, web_addr: str, db_data: str, custom_path: dict):
    database.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""",
                    ("nephelees", web_addr))

    json_data = {
        "database": [{
            "database_username": db_data["username"],
            "database_password": db_data["password"],
            "database_address": db_data["address"],
            "database_port": db_data["port"]
        }],
        "port": 3001
    }

    with open(str(custom_path) + f'/Cerbere/config.json', "w") as outfile:
        outfile.write(dumps(json_data, indent=4))
