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
    print(request.POST)
    if request.method == 'POST':
        print(request.POST)
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
        # print(theme)
        df = pd.read_csv('./content/data_clear.csv')
        # df['Название тематики'] = theme["0"]
        print(df)
        # df.replace(theme, inplace=True)
        # print(df['Тематика'].values)
        # d = dict.fromkeys(df['Тематика'].values, [])
        grouped = df.groupby(['Тематика'])['Вопрос абонента'].apply(list).to_dict()
        for key, item in theme["0"].items():
            print('hhh', theme["0"])
            grouped[item] = grouped.pop(key)[:20]
        # for i, row in df.iterrows():
        #     d[row['Тематика']].append(row['Вопрос абонента'])
        # with open('data.csv', 'w')as f:
            
        # print('hhjhj')

        # print(d['akciya_privedi_druga'])
        # with open('./content/data_clear.csv') as f:
        #     file = f.readlines()c16436829c3620aa7466932c4780e115b09510ce
        #     theme = {}
        #     for line in file:
        #         line = line.strip()
        #         theme[line.split(',')[0]] = line.split(',')[1]
        return HttpResponse(json.dumps(grouped))