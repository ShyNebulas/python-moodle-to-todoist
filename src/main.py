import os
import dotenv
from bs4 import BeautifulSoup
import re
from todoist_api_python.api import TodoistAPI


from pathlib import Path

from rich import print

import typer

import blacklist
import stripped

app = typer.Typer()

app.add_typer(blacklist.app, name="blacklist", help="Manage blacklist", invoke_without_command=True)
app.add_typer(stripped.app, name="stripped", help="Manage stripped list", invoke_without_command=True)

if __name__ == "__main__":
    app()




















# # TODO: Add multi-word support
# blacklisted_terms = ['attendance', 'booking', 'discussion', 'folder', 'forum', 'handbook', 'reading', 'selection', 'session', 'slides', 'solution', 'submission', 'support', 'weekly', 'zoom']
# def check_for_blacklist(string):
#     for blacklisted_term in blacklisted_terms:
#         if re.search(r"\b({0})\b".format(blacklisted_term), string, flags=re.IGNORECASE):
#             return True
#     return False








# APP_NAME = "python-moodle-to-todoist"
# def main():
#     env_path = Path("../.env")
#     if not env_path.is_file():
#         console.print("[warning][Warning][/warning] Required '.env' file does not exist")
#         env_path.touch(mode=0o600, exist_ok=False)
#         console.print("Created '.env' file")
#     if "TODOIST_API_KEY" not in dotenv.dotenv_values(env_path):
#         console.print("[warning][Warning][/warning] Required '.env' field 'TODOIST_API_KEY' does not exist")
#         value = typer.prompt("Enter your Todoist API key", hide_input=True)
#         dotenv.set_key(dotenv_path=env_path, key_to_set="TODOIST_API_KEY", value_to_set=value)
#     dotenv.load_dotenv(env_path)    
#     todoist_api = TodoistAPI(os.getenv("TODOIST_API_KEY"))
#     result = None
#     while result is None:
#         try:
#             result = todoist_api.get_projects()
#         except Exception as error:
#             # TODO: Add proper error support
#             console.print("[failure][Failure][/failure] Incorrect API key")
#             value = typer.prompt("Enter your Todoist API key", hide_input=True)
#             dotenv.set_key(dotenv_path=env_path, key_to_set="TODOIST_API_KEY", value_to_set=value)
#             dotenv.load_dotenv(env_path, override=True)  
#             todoist_api = TodoistAPI(os.getenv("TODOIST_API_KEY"))
            


    
  
            


   





# with os.scandir("html") as directory:
#     for entry in directory:
#         if not entry.name.startswith('.') and entry.is_file():
#             with open(entry.path, "r") as file:
#                 soup = BeautifulSoup(file, "html.parser")
#                 sections = soup.select(".content")
#                 for section in sections: 
#                     section_html = section.select(".sectionname")
#                     # if section_html: print(section_html[0].text)
#                     items = section.select(".instancename")
#                     for item in items:
#                         if not check_for_blacklist(item.text):
#                             # print(item.text)
#                             pass
#                         else:
#                             # print(f'[REMOVED] {item.text}')
#                             pass
        



                        
                       



         
          



# todoist_api_key = os.getenv("TODOIST_API_KEY")
# api = TodoistAPI(todoist_api_key)

# try:
#     projects = api.get_projects()
#     print(projects)
# except Exception as error:
#     print(error)