def create_nephelees_database(database, web_addr):
    database.create_table("""CREATE DATABASE IF NOT EXISTS cantina_nephelees""")
    database.create_table("CREATE TABLE IF NOT EXISTS cantina_nephelees.file_sharing("
                          "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, file_name TEXT, file_owner text, "
                          "file_short_name TEXT, login_to_show BOOL DEFAULT 1, password TEXT, "
                          "date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")

    database.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""",
                    ("nephelees", web_addr))
