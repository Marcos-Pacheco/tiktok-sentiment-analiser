from globals import *
from scrapper import Scrapper

class App:
    def __init__(self):
        self.scrapper = Scrapper("Chrome")


app = App()
app.scrapper.get("https://vm.tiktok.com/ZMjf2PEHg/")

# verificação humana

try:
    if confirm("Waiting for human verification", 'Click "OK" when done'):
        app.scrapper.load()
except Exception as e:
    alert("Error", f"The following error occured: {e}")
finally:
    app.scrapper.quit()
