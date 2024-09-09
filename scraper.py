from globals import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from rich.console import Console
import time

class Scraper:
    __driverName = None
    __driver = None

    # inicia o objeto Scrapper com uma instância de webdriver
    def __init__(self, driverName: str):
        driver = getattr(webdriver, driverName, None)
        if driver:
            self.__driverName = driverName
            if ('Firefox' in driverName):
                service = Service("/snap/bin/firefox.geckodriver")
                self.__driver = webdriver.Firefox(service=service)
            else:
                self.__driver = driver()
        else:
            raise ValueError(f"Driver {driverName} not supported.")

    # passa todas as chamadas de método que não existem nessa classe para o objeto webdriver
    def __getattr__(self, method):
        if self.__driver:
            return lambda *args, **kwargs: getattr(self.__driver, method)(*args, **kwargs)
        else:
            raise SystemError('No driver selected.')

    # carrega os comentários
    def load(self) -> None:
        container = self.__find_elements('[class*="DivCommentListContainer"]')[0]

        previous_html = self.__get_inner_html(container)
        unchanged_count = 0 # count how many times the checked for changes and there were none

        console = Console()

        try:
            print('starting...')
            self.__scroll_end(container)
            while unchanged_count < MAX_UNCHANGED_CHECKS:
                time.sleep(TIME_BETWEEN_AUTOMATED_ACTIONS)
                current_html = self.__get_inner_html(container)
                if current_html != previous_html:
                    print('loaded more...')
                    self.__scroll_end(container)
                    unchanged_count = 0
                    previous_html = current_html
                else:
                    unchanged_count += 1
                    tries_left = MAX_UNCHANGED_CHECKS - unchanged_count
                    if tries_left:
                        print(f'nothing found. {tries_left} tries left...')
        except Exception as e:
            raise e
        
        print('done')
            

    def extract(self):
        comments = self.__find_elements("[class*='DivCommentItemContainer']")
        for comment in comments:
            print(comment.text)

    def __scroll_end(self,el) -> None:
        self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def __get_inner_html(self,el) -> str:
        return el.get_attribute('innerHTML')
    
    def __find_elements(self,identifier: str) -> None:
        return self.__driver.find_elements(By.CSS_SELECTOR,identifier)

    def driver_name(self) -> str:
        return self.__driverName