from typing import Any
from selenium import webdriver
from re import search


class Scrapper:
    url = None
    driver = None       

    # inicia o objeto Scrapper com uma instância de webdriver
    def __init__(self, driverName):
        driver = getattr(webdriver, driverName, None)
        if driver:
          self.driver = driver()
        else:
          raise ValueError(f"Driver {driverName} não suportado.")
    
    # passa todas as chamadas de método que não existem nessa classe para o objeto webdriver
    def __getattr__(self, method):
        return lambda *args, **kwargs: getattr(self.driver, method)(*args, **kwargs)

    def getComments(self):
        pass

