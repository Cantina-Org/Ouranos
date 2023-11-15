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