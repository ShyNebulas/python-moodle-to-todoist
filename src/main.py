import os
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI

load_dotenv()

with os.scandir("html") as directory:
    for entry in directory:
        if not entry.name.startswith('.') and entry.is_file():
            with open(entry.path, "r") as file:
                print(entry.path)


# todoist_api_key = os.getenv("TODOIST_API_KEY")
# api = TodoistAPI(todoist_api_key)

# try:
#     projects = api.get_projects()
#     print(projects)
# except Exception as error:
#     print(error)