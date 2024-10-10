from globals import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from rich.logging import RichHandler
import time
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scraper:
    """A class to scrape TikTok comments using Selenium WebDriver."""

    def __init__(self, driver_name: str):
        """Initializes the Scraper with the specified WebDriver."""
        self.driver_name = driver_name
        self.driver = self._initialize_driver(driver_name)

    def _initialize_driver(self, driver_name: str):
        """Initializes the WebDriver based on the driver name."""
        options = None
        if driver_name == 'Firefox':
            options = webdriver.FirefoxOptions()
        elif driver_name == 'Chrome':
            options = webdriver.ChromeOptions()
        else:
            raise ValueError(f"Driver '{driver_name}' not supported.")
        
        # Initialize the remote WebDriver
        try:
            driver = webdriver.Remote(
                command_executor=SELENIUM_REMOTE_URL,
                options=options
            )
            return driver
        except Exception as e:
            logger.exception("Failed to initialize WebDriver.")
            raise e

    def get(self, url: str):
        """Navigates to the specified URL."""
        self.driver.get(url)

    def load_comments(self):
        """Loads all comments by scrolling and clicking 'View more replies' buttons."""
        logger.info('Loading comments...')

        # Pause the video to prevent another page loading
        self.driver.execute_script('document.getElementsByTagName("video")[0].pause()')

        # Locate the comment container
        container = self.driver.find_element(By.CSS_SELECTOR, '[class*="DivCommentListContainer"]')
        previous_html = container.get_attribute('innerHTML')
        unchanged_count = 0

        try:
            # Load level-1 comments
            logger.info('Expanding level-1 comments...')
            self._scroll_to_end()

            while unchanged_count < MAX_UNCHANGED_CHECKS:
                time.sleep(TIME_BETWEEN_ACTIONS)
                current_html = container.get_attribute('innerHTML')
                if current_html != previous_html:
                    self._scroll_to_end()
                    unchanged_count = 0
                    previous_html = current_html
                else:
                    unchanged_count += 1

            # Load level-2 comments (replies)
            logger.info('Expanding level-2 comments...')
            self._expand_replies()

            logger.info('All comments loaded.')
        except Exception as e:
            logger.exception("An error occurred while loading comments.")
            raise e

    def _expand_replies(self):
        """Clicks on 'View replies' buttons to load all replies."""
        search_texts = ['Ver', 'Visualizar', 'View', 'See']
        query = " or ".join([f"contains(span/text(), '{text}')" for text in search_texts])
        xpath = f"//div[contains(@class, 'DivViewRepliesContainer') and ({query})]"

        while True:
            reply_buttons = self.driver.find_elements(By.XPATH, xpath)
            if not reply_buttons:
                break

            for button_container in reply_buttons:
                try:
                    button = button_container.find_element(By.TAG_NAME, 'span')
                    self.driver.execute_script('arguments[0].scrollIntoView(true);', button_container)
                    self.driver.execute_script('arguments[0].click();', button)
                    time.sleep(TIME_BETWEEN_ACTIONS)
                except StaleElementReferenceException:
                    continue

    def _scroll_to_end(self):
        """Scrolls to the bottom of the page to load more comments."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def extract_comments(self):
        """Extracts comments from the loaded page."""
        logger.info('Extracting comments...')
        comments_elements = self.driver.find_elements(
            By.XPATH, "//span[starts-with(@data-e2e, 'comment-level-')]//span[1]"
        )
        comments = [elem.get_attribute('innerHTML') for elem in comments_elements]
        logger.info(f'Extracted {len(comments)} comments.')
        return comments
    
    def parse_comments(self, comments):
        """Parses the extracted comments into a structured format."""
        logger.info('Parsing comments...')
        parsed_comments = []
        for comment in comments:
            comment_data = {
                'user': '',  # Placeholder, needs proper extraction
                'date': '',  # Placeholder, needs proper extraction
                'comment': comment,
                'classification': '', # To be added manually
                'likes': '',  # Placeholder, needs proper extraction
            }
            parsed_comments.append(comment_data)

        result = {
            'executed_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'app_version': APP_VERSION,
            'from': self.driver.current_url,
            'total': len(parsed_comments),
            'comments': parsed_comments
        }
        return result
    
    def export_comments(self, data, filename=None):
        """Exports the parsed comments to a JSON file."""
        if not filename:
          filename = time.strftime('outputs/comments-%Y%m%d%H%M%S.json')

        logger.info(f'Exporting comments to {filename}...')
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info('Export completed successfully.')
        except Exception as e:
            logger.exception("Failed to export comments.")
            raise e
        
    def quit(self):
        """Quits the WebDriver session."""
        logger.info('Closing WebDriver session.')
        self.driver.quit()