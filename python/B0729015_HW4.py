import os
import json
import jieba
import re
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
    rule = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'    #資料處理規則

    for path in file_path:
        with open(path, mode='r', encoding="utf-8") as file:
            unformatted_text = file.readlines()
            
            for line in unformatted_text:  
                json_text = json.loads(line)
                formatted_text = re.sub(rule, '', json_text["text"].replace('\n', ''))
                all_contents.append(formatted_text)
        
    print("get_file_contents")
    return all_contents

def jieba_cal(data, origin_file):
    word_set = set()
    
    with open(origin_file , mode='w', encoding="utf-8") as file:
        for value in data:
            temp = jieba.lcut(value)
    
            for word in temp:
                if word in word_set:
                    continue
                
                file.writelines(word+"\n")
                word_set.add(word)
        
    print("jieba_cal")
    return

def trans_text(origin_data, trans_data):           #翻譯簡中文字
    cc = OpenCC('s2twp')
    
    with open(origin_data , mode='r', encoding="utf-8") as input_data:
        with open(trans_data , mode='w', encoding="utf-8") as output_data:
            for text in input_data.readlines():
                result = cc.convert(text)
                output_data.writelines(result)
    
    print("trans_text")
    return

def training_model(input_file):
    print("training")

    # Settings
    seed = 666
    sg = 0
    window_size = 20
    vector_size = 50
    min_count = 1
    workers = 8
    epochs = 5
    batch_words = 100000
    
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
    
    for item in model.wv.most_similar('李知恩', topn=20):
        print(item)
        
    model.save('t.model')
    return
 
"""def using_model():
    model = models.Word2Vec.load('word2vec.model')"""
    

def main():
    data_path = './wiki_zh/'        #wiki資料路徑
    origin_file = "untranslated.txt"
    training_file = "training_data.txt"
    
    #取得資料集
    """all_file_path = get_file_path(data_path)
    all_contents = get_file_contents(all_file_path)
    jieba_cal(all_contents, origin_file)
    trans_text(origin_file ,training_file)"""
        
    print("DataSet is completed")
    
    training_model(training_file)
    
if __name__== "__main__":
    main() 
