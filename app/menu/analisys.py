import torch
import pandas as pd
import torch.nn.functional as F
from core.encoder import Encoder
from core.classifier import Classifier
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
                self.model = BertModel.from_pretrained(MODEL_NAME)
                self.tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
            case _:
                print('Model not recognized, exiting.')
                exit(1)

        self.review('ele queria dinheiro pra comprar lanche sim kkkkk',160)

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

    def _encode(self,text,max_length):
        return Encoder(self.tokenizer,text,max_length).encode()


    def review(self,text,max_length):
        encoded = self._encode(text,max_length)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        input_ids = encoded['input_ids'].to(device)
        attention_mask = encoded['attention_mask'].to(device)
        class_names = ["negative", "neutral","positive"]

        classify = Classifier(len(class_names),self.model).to(device)

        output = classify(input_ids,attention_mask)
        _,prediction = torch.max(output, dim=1)
        probs = F.softmax(output, dim=1)

        print(f'Review text: {text}')
        print(pd.DataFrame(probs.tolist()[0], class_names)[0])
        print("========================\n")