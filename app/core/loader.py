import os
import json
import numpy as np
import pandas as pd
from globals import *
from core.ttdataset import TTDataset
from torch.utils.data import DataLoader
from pprint import pp

class Loader:
    def __init__(self,df,tokenizer,max_length,batch_size):        
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.batch_size = batch_size
        self.df = df
    
    def create(self):
        ds = TTDataset(
            reviews=self.df.text.to_numpy(),
            targets=self.df.label.to_numpy(),
            tokenizer=self.tokenizer,
            max_length=self.max_length
        )

        return DataLoader(
            ds,
            batch_size=self.batch_size,
            num_workers=4
        )   