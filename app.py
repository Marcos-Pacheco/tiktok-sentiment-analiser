import os
from globals import *
from scraper import Scraper
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pyfiglet import Figlet

class App:
    __scraper = None

    def __init__(self,driverName: str = None):
        self.__scraper = Scraper(driverName)
    
    def get(self, url: str) -> None:
        if url:
            self.__scraper.get(url)
    
    def scraper(self) -> Scraper:
        return self.__scraper

def intro():
    print(':' * 89)
    print('')
    print(Figlet(font=APP_FONT, width=100).renderText(APP_NAME))
    print(':' * 89)
    print(f'version:            {APP_VERSION}')
    print('')
    print(f'Welcome to {APP_NAME}! This app scrapes comments off of a Tiktok video webpage.')
    print('')

intro()

console = Console()
driverName = Prompt.ask('Select a webdriver: ', choices=['Firefox','Chrome'], default='Chrome')
inputMethod = Prompt.ask('Select an input: ', choices=['From Typing','From File'], default='From File')

urls = []

if inputMethod == 'From File':
    filepath = 'urls.txt'
    print(f'From File reads urls from the file "{filepath}"')
    if not os.path.exists(filepath):
        print(f'File "{filepath}" not found')
    else:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for key,line in enumerate(lines):
                if '#' in line:
                    lines.pop(key)

            if not len(lines):
                print(f'No entries found in "{filepath}", exiting.')
                exit()
    urls = [*urls , *lines]

if inputMethod == 'From Typing':
    urls.append(Prompt.ask('Type the TikTok url you wish to scrape'))

app = App(driverName)

try:
    for url in urls:
        print(f'scraping {url}')
        app.get(url)
        # verificação humana
        if Confirm.ask('Is human verification done?', default='y'):
            with Progress(
                SpinnerColumn(),
                TextColumn('[progress.description]{task.description}'),
                transient=True,
            ) as progress:
                progress.add_task(description="Processing...", total=None)
                app.scraper().load()
        else:
            print('Cannot proceed. Exiting.')
    input('End')
except Exception as e:
    console.print_exception(show_locals=True)
# finally:
    # app.scraper().quit()