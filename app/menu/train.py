from globals import *
import torch
import pandas as pd
import torch.nn.functional as F
from transformers import BertModel, BertForPreTraining, BertTokenizer, AutoModel
from rich import print as rich_print
from rich_menu import Menu
from core.trainer import Trainer

class Train:
    def __init__(self,console):
        choice = self._get_model_choice()
        match choice:
            case 'BERTimbau Base (pre-trained)':
                MODEL_NAME = 'neuralmind/bert-base-portuguese-cased'
                model = BertModel.from_pretrained(MODEL_NAME)
                tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
            case _:
                print('Model not recognized, exiting.')
                exit(1)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        rich_print(f'Training of model [bold cyan]{MODEL_NAME}[/bold cyan] started...')
        try:
            Trainer(model,tokenizer,device)
        except Exception as e:
            console.print_exception(show_locals=True)
    
    def _get_model_choice(self):
        choices=['BERTimbau Base (pre-trained)']
        menu = Menu(
            *choices,
            color='yellow',
            panel_title='Select classifier model',
            title='',
            align='left',
            rule=False,
            panel=True,
            selection_char='-> ',
            highlight_color='cyan'
        )
        return menu.ask(screen=False)