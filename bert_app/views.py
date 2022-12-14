from django.http import HttpResponse
import json
import torch
from transformers import BertTokenizer
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

class BertClassifier:

    def __init__(self, tokenizer_path, model_save_path='content/bert.pt'):
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        self.model_save_path=model_save_path
        self.max_len = 512
    
    def predict(self, text):
        self.model = torch.load(self.model_save_path, map_location=torch.device('cpu'))
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            truncation=True,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
        )
        
        out = {
              'text': text,
              'input_ids': encoding['input_ids'].flatten(),
              'attention_mask': encoding['attention_mask'].flatten()
          }
        
        input_ids = out["input_ids"]
        attention_mask = out["attention_mask"]
        
        outputs = self.model(
            input_ids=input_ids.unsqueeze(0),
            attention_mask=attention_mask.unsqueeze(0)
        )
        
        prediction = torch.argmax(outputs.logits, dim=1).cpu().numpy()[0]

        return prediction

@csrf_exempt
def classificate(request):
    if request.method == 'POST':
        text = request.POST['text']
        cls = BertClassifier(tokenizer_path='cointegrated/rubert-tiny', model_save_path='./content/bert_full_30.pt')
        predict = cls.predict(text)
        with open('./content/theme_number.csv') as f:
            file = f.readlines()
            theme = {}
            for line in file:
                line = line.strip()
                if line.split(',')[0]:
                    theme[int(line.split(',')[0])-1] = line.split(',')[1]
        return HttpResponse(json.dumps({'text':str(theme[predict])}))

def get_data(request):
    if request.method == 'GET':
        theme = pd.read_csv('./content/theme_number.csv').to_dict()
        df = pd.read_csv('./content/data_clear.csv')
        grouped = df.groupby(['????????????????'])['???????????? ????????????????'].apply(list).to_dict()
        for key, item in theme["0"].items():
            grouped[item] = grouped.pop(key)[:3]
        return HttpResponse(json.dumps(grouped))