import torch
import time
import pandas as pd
import numpy as np
import torch
import json
import os
import math
from collections import defaultdict
from globals import *
from core.loader import Loader
from rich import print as rich_print
from rich_menu import Menu
from sklearn.model_selection import train_test_split
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from core.classifier import Classifier
from transformers import (
    AdamW,
    get_linear_schedule_with_warmup,
)

class Trainer:
    def __init__(self,bert,tokenizer,device):
        MAX_LEN = 160
        BATCH_SIZE = 16
        RANDOM_SEED = 50
        np.random.seed(RANDOM_SEED)
        torch.manual_seed(RANDOM_SEED)

        # pergunta ao usuário qual arquivo será utilizado para treinamento
        df = pd.DataFrame(self._import())

        # spinner
        with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), transient=True) as progress:
            progress.add_task(description="Training...", total=None)

        # quebrando o dataframe em treinamento, teste e valores
        df_train, df_test = train_test_split(df, test_size=0.1, random_state=RANDOM_SEED)
        df_val, df_test = train_test_split(df_test, test_size=0.5, random_state=RANDOM_SEED)

        # esse pedaço do código garante que haja somente um label por entrada a ser feita review
        df['label'] = df['label'].apply(lambda x: x[0] if isinstance(x, list) and x else None)

        # renomeia os campos para ficar no padrão que o modelo consegue entender
        df.rename(columns={'text':'content', 'label':'sentiment'}, inplace=True)

        train_data_loader = Loader(df_train, tokenizer, MAX_LEN, BATCH_SIZE).create()
        val_data_loader = Loader(df_val, tokenizer, MAX_LEN, BATCH_SIZE).create()
        test_data_loader = Loader(df_test, tokenizer, MAX_LEN, BATCH_SIZE).create()
        
        self.EPOCHS = 10
        # Learning rate (Adam): 5e-5, 3e-5, 2e-5
        self.LEARNING_RATE = 5e-5
        self.STEPS = len(train_data_loader) * self.EPOCHS
        loss_fn = torch.nn.CrossEntropyLoss().to(device)

        self.optimizer = AdamW(bert.parameters(), lr=self.LEARNING_RATE, correct_bias=False)
        self.scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps = 0,
            num_training_steps = self.STEPS
        )

        self._execute(
            model=bert,
            data_loader=train_data_loader,
            loss_fn=loss_fn,
            device=device,
            scheduler=self.scheduler,
            optimizer=self.optimizer,
            df_train=df_train,
            df_test=df_test,
            df_val=df_val,
            val_data_loader=val_data_loader,
            test_data_loader=test_data_loader
        )
    
    def _train(self,model,data_loader,loss_fn,optimizer,device,scheduler,n_examples):
        model = model.train()
        losses = []
        correct_predictions = 0

        for data in data_loader:
            input_ids = data['input_ids'].to(device)
            attention_mask = data['attention_mask'].to(device)
            targets = data['targets'].to(device)

            classify = Classifier(3,model).to(device)
            outputs = classify(input_ids,attention_mask)

            _, preds = torch.max(outputs,dim=1)
            loss = loss_fn(outputs, targets)

            correct_predictions += torch.sum(preds == targets)
            losses.append(loss.item())

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

        return correct_predictions.double() / n_examples, np.mean(losses)
    
    def _eval(self,model,data_loader,loss_fn,device,n_example):
        model = model.eval()
        losses = []
        correct_predictions = 0

        with torch.no_grad():
            for data in data_loader:
                input_ids = data['input_ids'].to(device)
                attention_mask = data['attention_mask'].to(device)
                targets = data['targets'].to(device)

                classify = Classifier(3,model).to(device)
                outputs = classify(input_ids,attention_mask)

                _, preds = torch.max(outputs, dim=1)

                loss = loss_fn(outputs, targets)

                correct_predictions += torch.sum(preds == targets)
                losses.append(loss.item())

        return correct_predictions.double() / n_example, np.mean(losses)
    
    def _execute(self, model, data_loader, loss_fn, device, scheduler, optimizer, df_train, df_test, df_val, val_data_loader, test_data_loader):
        start_time = time.time()

        # history = defaultdict(list)
        best = 0

        for epoch in range(self.EPOCHS):
            print(f'Epoch {epoch + 1}/{self.EPOCHS}')
            print('-' * 20)

            train_acc, train_loss = self._train(
                model,
                data_loader,
                loss_fn,
                optimizer,
                device,
                scheduler,
                len(df_train)
            )

            print(f'Train loss {train_loss} accuracy {train_acc}\n')

            val_acc, val_loss = self._eval(
                model,
                val_data_loader,
                loss_fn, 
                device, 
                len(df_val)
            )

            print(f'Val   loss {val_loss} accuracy {val_acc}\n')

            # history['train_acc'].append(train_acc)
            # history['train_loss'].append(train_loss)
            # history['val_acc'].append(val_acc)
            # history['val_loss'].append(val_loss)

            if val_acc > best:
                torch.save(model.state_dict(), 'best_model_state.bin')
                best = val_acc

        end_time = time.time()
        exec_time = end_time - start_time

        h = math.ceil(exec_time // 3600)
        m = math.ceil((exec_time % 3600) // 60)
        s = math.ceil(exec_time % 60)

        print(f'Trainig done: {h} hours, {m} minutes, {s} seconds elapsed')

    
    def _import(self):
        filepath = self.__get_file_choice()

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data

    def __get_file_choice(self):
        choices=[os.path.join(LABELED_DATA_FOLDER, file) for file in os.listdir(LABELED_DATA_FOLDER) if os.path.isfile(os.path.join(LABELED_DATA_FOLDER, file))]
        menu = Menu(
            *choices,
            color='yellow',
            panel_title='Select a labeled file to import',
            title='',
            align='left',
            rule=False,
            panel=True,
            selection_char='-> ',
            highlight_color='cyan'
        )
        return menu.ask(screen=False)