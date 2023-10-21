import rich
from InquirerPy import inquirer, get_style
from InquirerPy.utils import InquirerPyStyle
from Utils import base_installer


base_installer.default_welcome_message()

to_install = inquirer.select("Quel application Cantina voulez vous installer ?", choices=["Ouranos", "Nephelees", "Cerbere"]).execute()
print(to_install)
