import os
import json
import jieba
from string import punctuation
from opencc import OpenCC
from gensim.models import word2vec, fasttext
import logging

jieba.setLogLevel(logging.INFO)

def get_file_path(folder_path):     #取得wiki所有檔案路徑
    file_path = []
    
    all_path = os.walk(folder_path)
    
    for folder in all_path:
        if folder[2] != True:
            for file in folder[2]:
                file_path.append(folder[0] + "/" + file)
     
    return file_path

def get_file_contents(file_path):   #取得wiki所有text
    all_contents = []
    for path in file_path:
        with open(path, mode='r', encoding="utf-8") as file:
            unformatted_text = file.readlines()
            
            for line in unformatted_text:  
                json_text = json.loads(line)
                formatted_text = json_text["text"].strip().replace('\n', '').replace('\r', '').replace(" ", "")
                all_contents.append(formatted_text)
        
    print("get_file_contents")
    return all_contents

def trans_text(contents):           #翻譯簡中文字
    cc = OpenCC('s2twp')
    trans_text = []
    
    for text in contents:
        result = cc.convert(text)
        trans_text.append(result)
    
    print("trans_text")
    return trans_text

def jieba_cal(data):
    jieba.set_dictionary('dict.txt')
    word_set = set()
    
    #資料處理規則
    add_punc='，。、【 】 “”：；·（）《》‘’{}？!?~/！⑦()、%^>℃：.”“^-——=&#@￥」「'
    add2_punc = '的之'
    all_punc = punctuation + add_punc + add2_punc
    
    for value in data:
        temp = jieba.lcut(value, cut_all=False)
        for word in temp:
            if word in all_punc:
                continue
            elif word not in word_set:
                word_set.add(word)
        
    print("jieba_cal")
    return word_set

def training_model(input_file):
    print("training")
    # Settings
    seed = 812
    sg = 0
    window_size = 5
    vector_size = 300
    min_count = 1
    workers = 8
    epochs = 5
    batch_words = 10000
    
    # Train
    train_data = word2vec.LineSentence(input_file)
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
    
    for item in model.wv.most_similar('李知恩'):
        print(item)
        
    model.save('t.model')
    return
 
def main():
    data_path = './wiki_zh/'        #wiki資料路徑
    training_file = "training_data.txt"
    
    all_file_path = get_file_path(data_path)
    all_contents = get_file_contents(all_file_path)
    trans_data = trans_text(all_contents)
    training_set = jieba_cal(trans_data)
        
    print("DataSet is completed")
    
    with open(training_file , mode='w', encoding="utf-8") as file:
        for word in training_set:
            file.writelines(word+"\n")
    
    training_model(training_file)

if __name__== "__main__":
    main() 
