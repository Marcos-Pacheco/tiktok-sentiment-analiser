from Gui import *
from Helpers import *
from Scrapper import Scrapper
from selenium.webdriver.common.by import By
import time

class App:

  def __init__(self):
    self.scrapper = Scrapper('Chrome')
  
app = App()
app.scrapper.get('https://vm.tiktok.com/ZMjf2PEHg/')

"""
  ESTRUTURA DE UM COMENTÁRIO - 04/09/2024
  - DivCommentObjectWrapper
	- DivCommentContentWrapper
		- data-e2e="comment-level-1"
			- span
				- <comentario>
"""

# verificação humana

if(confirm('Waiting for human verification','Click "OK" when done')):
  # comments = app.scrapper.find_elements(By.XPATH,"//*[contains(@class, 'DivCommentItemContainer')]")
  comments = app.scrapper.find_elements(By.CSS_SELECTOR,"[class*='DivCommentItemContainer']")

  for comment in comments:
    print(comment.text)

  app.scrapper.quit()