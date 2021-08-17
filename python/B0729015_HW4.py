import os
import json
import jieba
import pandas as pd
from string import punctuation
from opencc import OpenCC
import re
from gensim.models import word2vec, fasttext

def get_file_name():
    file_address = []
    data_path = './wiki_zh/'
    
    all_file = os.walk(data_path)
    
    for folder in all_file:
        if folder[2] != True:
            for file in folder[2]:
                file_address.append(folder[0] + "/" + file)
            
    return file_address


def trans_text(file_address):
    cc = OpenCC('s2twp')
    trans_data = []

    for name in file_address: 

        with open("./wiki_zh/AM/wiki_73", mode='r', encoding="utf-8") as file:
            line = file.readlines()
            print(line)
            data = json.loads(line)
            text = cc.convert(data["text"]).strip().replace('\n', '').replace('\r', '').replace(" ", "")
            trans_data.append(text) 
        """with open(name, mode='r', encoding="utf-8") as file:
            line = file.readline()
            data = json.loads(line)
            text = cc.convert(data["text"]).strip().replace('\n', '').replace('\r', '').replace(" ", "")
            trans_data.append(text)"""
    
    return trans_data

def jieba_cal(data):
    jieba.set_dictionary('dict.txt')
    file_name = 'wiki_text.txt'
    
    add_punc='，。、【 】 “”：；·（）《》‘’{}？!?~/！⑦()、%^>℃：.”“^-——=&#@￥」「'
    add2_punc = '的之'
    all_punc = punctuation + add_punc + add2_punc
    
    for value in data:
        temp = jieba.lcut(value)
        
        with open(file_name, 'w', encoding='utf-8') as file:
            for i in temp:
                if i in all_punc:
                    temp.remove(i)
                else:
                    re.sub(r'[A-Za-z0-9]|/d+','',i)
                    file.writelines(i+"\n")
                 
    return file_name
    

    
file_address = get_file_name()
trans_data = trans_text(file_address)
"""word_data = jieba_cal(trans_data)

# Settings
seed = 812
sg = 0
window_size = 10
vector_size = 100
min_count = 1
workers = 8
epochs = 5
batch_words = 10000


# Train
train_data = word2vec.LineSentence(word_data)
model = fasttext.FastText(
    train_data,
    min_count=min_count,
    vector_size =vector_size,
    workers=workers,
    epochs=epochs,
    window=window_size,
    sg=sg,
    seed=seed,
    batch_words=batch_words,
)


model.save('t.model')

model = word2vec.Word2Vec.load('t.model')

for item in model.wv.most_similar('李知恩'):
    print(item)

model.save('t.model')"""


