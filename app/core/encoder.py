class Encoder:
    def __init__(self,tokenizer,text, max_length):
        self.tokenizer = tokenizer
        self.text = text
        self.max_length = max_length

    def encode(self):
        return self.tokenizer.encode_plus(
            self.text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            add_special_tokens= True,
            return_token_type_ids=False,
            return_attention_mask=True,
            return_tensors='pt',
        )
