from globals import *
from rich import print as rich_print
from rich_menu import Menu
from transformers import BertModel, BertForPreTraining, BertTokenizer, AdamW, get_linear_schedule_with_warmup, pipeline
from transformers import AutoModel

class Analisys:
    def __init__(self):
        choice = self._get_model_choice()
        match choice:
            case 'BERTimbau Base (pre-trained)':
                MODEL_NAME = 'neuralmind/bert-base-portuguese-cased'
                self.model = BertForPreTraining.from_pretrained(MODEL_NAME)
                self.tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
            case _:
                print('Model not recognized, exiting.')
                exit(1)
        
        self.tokenize('Hello World!!')

        # rich_print('For sentiment analisys access the following URL:[bold cyan]"PLACE HOLDER"[/bold cyan]')
    
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

    def tokenize(self,text):
        tokens = self.tokenizer(text)
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)

        print(f' Sentence: {text}')
        print(f'   Tokens: {tokens}')
        print(f'Token IDs: {token_ids}')

        return (tokens,token_ids)
            