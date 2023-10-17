import typer

import config
import run

app = typer.Typer()

app.add_typer(config.app, name="config")
app.add_typer(run.app, name="run", invoke_without_command=True)

if __name__ == "__main__":
    app()




















# # TODO: Add multi-word support
# blacklisted_terms = ['attendance', 'booking', 'discussion', 'folder', 'forum', 'handbook', 'reading', 'selection', 'session', 'slides', 'solution', 'submission', 'support', 'weekly', 'zoom']
# def check_for_blacklist(string):
#     for blacklisted_term in blacklisted_terms:
#         if re.search(r"\b({0})\b".format(blacklisted_term), string, flags=re.IGNORECASE):
#             return True
#     return False









            


    
  
            


   

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
        



                        
                       



         
          



