from InquirerPy import inquirer
from Utils import base_installer


base_installer.default_welcome_message()

to_install = inquirer.select("Quel application Cantina voulez vous installer ?", choices=["Olympe", "Nephelees",
                                                                                          "Cerbere"]).execute()
database, db_data = base_installer.database_connection(to_install)
base_installer.create_app(database, db_data, to_install)

