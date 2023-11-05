from Utils import base_installer


base_installer.default_welcome_message()
database, db_data = base_installer.database_connection("Cerbere")
base_installer.create_app(database, db_data, "Cerbere")
