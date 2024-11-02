import torch
from core.encoder import Encoder
from globals import *
from torch.utils.data import Dataset,DataLoader

class TTDataset(Dataset):
    """This pipeline prepares batches of tokenized text and their associated labels."""

    def __init__(self,reviews,targets,tokenizer,max_length):
        self.reviews = reviews
        self.targets = targets
        self.tokenizer = tokenizer
        self.max_length = max_length

        # If targets are strings, map them to integers;
        label_map = {"negative": 0, "neutral": 1, "positive": 2} 
        self.targets = [label_map[label[0]] for label in targets]
    
    def __getitem__(self,index):
        review = str(self.reviews[index])
        target = self.targets[index]
        encoding = Encoder(self.tokenizer, review, self.max_length).encode()
        return {
            'review_text': review,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'targets': torch.tensor(target, dtype=torch.long)
        }

    def __len__(self):
        return len(self.reviews)
