def create_administration_database(database):
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


def create_nephelees_database(database, web_addr):
    database.create_table("""CREATE DATABASE IF NOT EXISTS cantina_nephelees""")
    database.create_table("CREATE TABLE IF NOT EXISTS cantina_nephelees.file_sharing("
                          "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, file_name TEXT, file_owner text, "
                          "file_short_name TEXT, login_to_show BOOL DEFAULT 1, password TEXT, "
                          "date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")

    database.insert("""INSERT INTO cantina_administration.domain(name, fqdn) VALUES (%s, %s)""",
                    ("nephelees", web_addr))