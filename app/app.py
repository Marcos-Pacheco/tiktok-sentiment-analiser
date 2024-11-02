from globals import *
from rich.console import Console
from rich import print as rich_print
from rich_menu import Menu
from pyfiglet import Figlet
from menu.scrape import Scrape
from menu.classify import Classify
from menu.analisys import Analisys
from menu.train import Train
import sys

def display_intro():
    """Displays the application introduction."""
    print(':' * 89)
    print('')
    print(Figlet(font=APP_FONT, width=100).renderText(APP_NAME))
    print(':' * 89)
    print(f'version:            {APP_VERSION}')
    print('')
    print(f'Welcome to {APP_NAME}! This app provides advanced sentiment analysis tools specifically designed for TikTok content.')
    print('')

def get_functionality_choice():
    """Prompts the user to choose a specific application feature."""
    choices=['Scrape','Classify','Sentiment Analysis', 'Train Model']
    menu = Menu(
        *choices,
        color='yellow',
        panel_title='Select a feature',
        title='',
        align='left',
        rule=False,
        panel=True,
        selection_char='-> ',
        highlight_color='cyan'
    )
    selected = menu.ask(screen=False)
    rich_print(f'Feature: [bold cyan]{selected}[/bold cyan]')
    return selected

def main():
    """Main function to run the application."""
    display_intro()
    console = Console()

    match get_functionality_choice():
        case 'Scrape':
            Scrape(console)
        case 'Classify':
            Classify()
        case 'Sentiment Analysis':
            Analisys()
        case 'Train Model':
            Train(console)
        case _:
            rich_print('Error: [bold red]feature selected is not found.[/bold red]')
            pass
    print('end')
    sys.exit(1)

if __name__ == '__main__':
    main()