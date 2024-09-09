from globals import *
from scraper import Scraper
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.console import Console
from pyfiglet import figlet_format as fig
from pyfiglet import Figlet
from rich.progress import Progress, SpinnerColumn, TextColumn

class App:
    __scraper = None
    __url = None

    def __init__(self):
        self.__intro()
        self.__driver(Prompt.ask('Select a webdriver: ', choices=['Firefox','Chrome'], default='Chrome'))
        self.__url(Prompt.ask('Type the TikTok url you wish to scrape'))
        self.__scraper.get(self.__url)
    
    def __intro(self):
        print(':' * 89)
        print('')
        print(Figlet(font=APP_FONT, width=100).renderText(APP_NAME))
        print(':' * 89)
        print(f'version:            {APP_VERSION}')
        print('')
        print(f'Welcome to {APP_NAME}! This app scrapes comments off of a Tiktok video webpage.')
        print('')
    
    def __driver (self,driverName:str = None) -> None:
        if driverName:
            self.__scraper = Scraper(driverName)
    
    def __url(self, url: str) -> None:
        if url:
            self.__url = url
    
    def scraper(self) -> Scraper:
        return self.__scraper


app = App()
console = Console()

try:
# verificação humana
    if Confirm.ask('Is human verification done?', default='y'):
        with Progress(
            TextColumn('[progress.description]{task.description}'),
            transient=True,
        ) as progress:
            progress.add_task(description="Processing...", total=None)
            app.scraper().load()
except Exception as e:
    console.print_exception(show_locals=True)
finally:
    app.scraper().quit()