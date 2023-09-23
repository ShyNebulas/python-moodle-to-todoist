import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
from todoist_api_python.api import TodoistAPI

load_dotenv()

blacklisted_terms = ["weekly", "support", "session", "submission", "slides", "zoom", "folder", "forum", "discussion", "solution"]
with os.scandir("html") as directory:
    for entry in directory:
        if not entry.name.startswith('.') and entry.is_file():
            with open(entry.path, "r") as file:
                soup = BeautifulSoup(file, "html.parser")
                sections = soup.select(".content")
                for section in sections: 
                    section_name = section.select(".sectionname")
                    if section_name: print(section_name[0].text)
                    items = section.select(".instancename")
                    for item in items:
                        print(item.text)
                       



         
          



# todoist_api_key = os.getenv("TODOIST_API_KEY")
# api = TodoistAPI(todoist_api_key)

# try:
#     projects = api.get_projects()
#     print(projects)
# except Exception as error:
#     print(error)