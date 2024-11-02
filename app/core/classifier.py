from torch import nn

class Classifier(nn.Module):

  def __init__(self, n_classes, bert):
    super(Classifier, self).__init__()
    self.bert = bert
    self.drop = nn.Dropout(p=0.3)
    #The last_hidden_state is a sequence of hidden states of the last layer of the model
    self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
  
  def forward(self, input_ids, attention_mask):
    outputs = self.bert(
      input_ids=input_ids,
      attention_mask=attention_mask
    )
    
    # last_hidden_state = outputs.last_hidden_state
    pooler_output = outputs.pooler_output

    output = self.drop(pooler_output)
    return self.out(output)