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
    rule = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》；「」：（）？“”‘’！[\\]^_`{|}~]+'    #資料處理規則

    for path in file_path:
        with open(path, mode='r', encoding="utf-8") as file:
            unformatted_text = file.readlines()
            
            for line in unformatted_text:  
                json_text = json.loads(line)
                formatted_text = re.sub(rule, '', json_text["text"].strip().replace('\n', '').replace('\r', '').replace(" ", ""))
                all_contents.append(formatted_text)
        
    print("get_file_contents")
    return all_contents

def jieba_cal(data, origin_file):   
    with open(origin_file , mode='w', encoding="utf-8") as file:
        for value in data:
            temp = jieba.lcut(value)
    
            for word in temp:               
                file.writelines(word+"\n")
        
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
    seed = 432
    sg = 0
    window_size = 10
    vector_size = 100
    min_count = 5
    epochs = 10
    batch_words = 100000
    
    # Train
    train_data = word2vec.LineSentence(input_file)
    model = fasttext.FastText(
        train_data,
        min_count=min_count,
        vector_size =vector_size,
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

def test():
    model = fasttext.FastText.load('t.model')

    print("輸入一個詞，則去尋找前20個該詞的相似詞")

    while True:
        try:
            query = input()
            q_list = query.split()

            if len(q_list) == 1:
                print("相似詞前 20 排序")
                res = model.wv.most_similar(q_list[0],topn = 20)
                for item in res:
                    print(item[0]+","+str(item[1]))

        except Exception as e:
            print(repr(e))

def main():
    data_path = './wiki_zh/'        #wiki資料路徑
    origin_file = "untranslated.txt"
    training_file = "training_data.txt"
    
    #取得資料集
    all_file_path = get_file_path(data_path)
    all_contents = get_file_contents(all_file_path)
    jieba_cal(all_contents, origin_file)
    trans_text(origin_file ,training_file)
        
    print("DataSet is completed")
    
    training_model(training_file)
    test()
    
if __name__== "__main__":
    main() 
