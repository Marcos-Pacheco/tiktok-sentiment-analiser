from globals import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import StaleElementReferenceException
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
            if 'Firefox' in driverName:
                options = webdriver.FirefoxOptions()
            if 'Chrome' in driverName:
                options = webdriver.ChromeOptions()
            
            self.__driver=webdriver.Remote(command_executor="http://selenium:4444",options=options)
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

        # parar de rodar o vídeo
        self.__driver.execute_script('document.getElementsByTagName("video")[0].pause()')

        container = self.__driver.find_element(By.CSS_SELECTOR,'[class*="DivCommentListContainer"]')

        previous_html = self.__get_inner_html(container)
        unchanged_count = 0 # count how many times the checked for changes and there were none

        try:
            # carrega todos os comentários level-1
            print('expanding level-1 comments...')
            self.__scroll_end(container)
            while unchanged_count < MAX_UNCHANGED_CHECKS:
                time.sleep(TIME_BETWEEN_AUTOMATED_ACTIONS)
                current_html = self.__get_inner_html(container)
                if current_html != previous_html:
                    self.__scroll_end(container)
                    unchanged_count = 0
                    previous_html = current_html
                else:
                    unchanged_count += 1
            
            # carrega todos os comentários level-2
            print('expanding level-2 comments...')
            # replies_containers = self.__driver.find_elements(By.CSS_SELECTOR,'[class*="DivViewRepliesContainer"]')
            # replies_containers = self.__driver.find_elements(By.XPATH, "//div[contains(@class, 'DivViewRepliesContainer') and span[(text()='Ocultar')]]")
            
            search = ['Ver','Visualizar','View','See']
            query = " or ".join([f"contains(span/text(), '{word}')" for word in search])
            replies_containers = self.__driver.find_elements(By.XPATH, f"//div[contains(@class, 'DivViewRepliesContainer') and ({query})]")

            while len(replies_containers):
                was = len(replies_containers)
                for reply_container in replies_containers:
                    try:
                        btn = reply_container.find_element(By.TAG_NAME,'span')
                        # print(self.__get_inner_html(btn))
                        self.__driver.execute_script('arguments[0].scrollIntoView(true);', reply_container)
                        self.__driver.execute_script('arguments[0].click();', btn)
                        time.sleep(TIME_BETWEEN_AUTOMATED_ACTIONS)
                    except StaleElementReferenceException:
                        # print('stale, skiping...')
                        continue
                replies_containers = self.__driver.find_elements(By.XPATH, f"//div[contains(@class, 'DivViewRepliesContainer') and ({query})]")
                # print(f'reloaded replie divs: now - {len(replies_containers)} was - {was}')
                time.sleep(TIME_BETWEEN_AUTOMATED_ACTIONS+2)

        except Exception as e:
            raise e
        
        print('done')
            

    def extract(self):
        # comments = self.__driver.find_elements("[class*='DivCommentItemContainer']")
        # comments = self.__driver.find_elements("[class*='DivCommentHeaderWrapper']")
        comments = self.__driver.find_elements(By.XPATH,"//span[@attribute='data-e2e']")
        for comment in comments:
            print(comment)

    def driver_name(self) -> str:
        return self.__driverName

    def __scroll_end(self,el) -> None:
        self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def __get_inner_html(self,el) -> str:
        return el.get_attribute('innerHTML')
