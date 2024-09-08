# from typing import Any
from Gui import alert
from Helpers import dd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time

class Scrapper:
    driver = None

    # inicia o objeto Scrapper com uma instância de webdriver
    def __init__(self, driverName: str):
        driver = getattr(webdriver, driverName, None)
        if driver:
            if ('Firefox' in driverName):
                service = Service("/snap/bin/firefox.geckodriver")
                self.driver = webdriver.Firefox(service=service)
            else:
                self.driver = driver()
        else:
            raise ValueError(f"Driver {driverName} not supported.")

    # passa todas as chamadas de método que não existem nessa classe para o objeto webdriver
    def __getattr__(self, method):
        return lambda *args, **kwargs: getattr(self.driver, method)(*args, **kwargs)

    # carrega os comentários
    def load(self) -> None:
        container = self.__find_elements('[class*="DivCommentListContainer"]')[0]

        previous_html = self.__get_inner_html(container)
        unchanged_count = 0 # count how many times the checked for changes and there were none
        max_unchanged_checks = 5 # maximum ammount of change checks. If reached, means that no more comments will be loaded
        secs = 5

        try:
            print('=== starting load process ===')
            self.__scroll_end(container)
            while unchanged_count < max_unchanged_checks:
                time.sleep(secs)
                current_html = self.__get_inner_html(container)
                if current_html != previous_html:
                    print('=== loaded more comments ===')
                    self.__scroll_end(container)
                    unchanged_count = 0
                    previous_html = current_html
                else:
                    unchanged_count += 1
                    tries_left = max_unchanged_checks - unchanged_count
                    if tries_left:
                        print(f'=== nothing found on this try. {tries_left} tries left. waiting {secs} secs ===')
        except Exception as e:
            alert('Error',f'The following error occured while loading: {e}')
        
        print('=== load process ended ===')
            

    def extract(self):
        comments = self.__find_elements("[class*='DivCommentItemContainer']")
        for comment in comments:
            print(comment.text)

    def __scroll_end(self,el) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def __get_inner_html(self,el) -> str:
        return el.get_attribute('innerHTML')
    
    def __find_elements(self,identifier: str) -> None:
        return self.driver.find_elements(By.CSS_SELECTOR,identifier)