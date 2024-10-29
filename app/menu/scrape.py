from globals import *
import os
import sys
from core.scraper import Scraper
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rich_print
from rich_menu import Menu

class Scrape:
    def __init__(self,console):
        """Main function to run the scrape application."""
        self.console = console
        driver_name = self.get_driver_choice()
        input_method = self.get_input_method()

        if input_method == 'From File':
            rich_print('Reading URLs from [bold cyan]"urls.txt"[/bold cyan]...')
            urls = self.read_urls_from_file()
        else:
            url = Prompt.ask('Type the TikTok URL you wish to scrape')
            urls = [url]

        scraper = Scraper(driver_name)

        try:
            rich_print(f'See what\'s happening at [bold cyan]{SELENIUM_URL}[bold cyan]')
            human_check = 0
            for url in urls:
                rich_print(f'Scraping [bold cyan]{url}[/bold cyan]')
                scraper.get(url)
                
                if human_check < 1: # Only needed in the first of the batch
                    human_check += 1
                    # Wait for human verification
                    if not Confirm.ask('Please complete any human verification required. Continue?', default=True):
                        print('Cannot proceed without human verification. Exiting.')
                        sys.exit(1)

                with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), transient=True) as progress:
                    progress.add_task(description="Processing...", total=None)
                    scraper.load_comments()
                    extraction = scraper.extract_comments()
                    scraper.export_comments(scraper.parse_comments(extraction))
                    scraper.export_labels(scraper.parse_labels(extraction))
            
            os.system('chown -R $HOST_USER_ID:$HOST_USER_GROUP_ID /app/outputs')

            print('Scraping and export completed successfully.')
        except Exception as e:
            self.console.print_exception(show_locals=True)
        finally:
            scraper.quit()

    def get_driver_choice(self):
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

    def get_input_method(self):
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

    def read_urls_from_file(self,filepath='urls.txt'):
        """Reads URLs from a file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'File "{filepath}" not found')

        with open(filepath, 'r') as file:
            lines = file.readlines()

        # Remove comments and whitespace
        urls = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
        if not urls:
            raise Exception(f'No valid URLs found in "{filepath}".')

        return urls