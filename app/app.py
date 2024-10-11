from globals import *
import os
import sys
from scraper import Scraper
from rich.prompt import Prompt, Confirm
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rich_print
from rich_menu import Menu
from pyfiglet import Figlet

def display_intro():
    """Displays the application introduction."""
    print(':' * 89)
    print('')
    print(Figlet(font=APP_FONT, width=100).renderText(APP_NAME))
    print(':' * 89)
    print(f'version:            {APP_VERSION}')
    print('')
    print(f'Welcome to {APP_NAME}! This app scrapes comments off of a Tiktok video webpage.')
    print('')

def get_driver_choice():
    """Prompts the user to select a webdriver."""
    choices=['Chrome','Firefox']
    menu = Menu(
        *choices,
        color='yellow',
        panel_title='Select a webdriver',
        title='',
        align='left',
        rule=False,
        panel=True,
        selection_char='-> ',
        highlight_color='cyan'
    )
    selected = menu.ask(screen=False)
    rich_print(f'Webdriver: [bold cyan]{selected}[/bold cyan]')
    return selected

def get_input_method():
    """Prompts the user to select an input method."""
    choices=['From File','From Typing']
    menu = Menu(
        *choices,
        color='yellow',
        panel_title='Select an input method',
        title='',
        align='left',
        rule=False,
        panel=True,
        selection_char='-> ',
        highlight_color='cyan'
    )
    selected = menu.ask(screen=False)
    rich_print(f'Input method: [bold cyan]{selected}[/bold cyan]')
    return selected

def read_urls_from_file(filepath='urls.txt'):
    """Reads URLs from a file."""
    if not os.path.exists(filepath):
        print(f'File "{filepath}" not found')
        sys.exit(1)

    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Remove comments and whitespace
    urls = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
    if not urls:
        print(f'No valid URLs found in "{filepath}". Exiting.')
        sys.exit(1)
    return urls



def main():
    """Main function to run the application."""
    display_intro()
    console = Console()

    driver_name = get_driver_choice()
    input_method = get_input_method()

    if input_method == 'From File':
        rich_print('Reading URLs from [bold cyan]"urls.txt"[/bold cyan]...')
        urls = read_urls_from_file()
    else:
        url = Prompt.ask('Type the TikTok URL you wish to scrape')
        urls = [url]

    scraper = Scraper(driver_name)

    try:
        for url in urls:
            rich_print(f'Scraping [bold cyan]{url}[/bold cyan]')
            scraper.get(url)

            # Wait for human verification
            if not Confirm.ask('Please complete any human verification required. Continue?', default=True):
                print('Cannot proceed without human verification. Exiting.')
                sys.exit(1)

            with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), transient=True) as progress:
                progress.add_task(description="Processing...", total=None)
                scraper.load_comments()
                extraction = scraper.extract_comments()
                scraper.export_comments(scraper.parse_comments(extraction))

        print('Scraping and export completed successfully.')
    except Exception as e:
        console.print_exception(show_locals=True)
    finally:
        scraper.quit()

if __name__ == '__main__':
    main()