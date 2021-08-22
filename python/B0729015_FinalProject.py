import pandas as pd
import re
import math

def get_data_characteristic():
     
    label = pd.read_csv('train_label.csv')  
    
    push_down = push_num = down_num = none_num = 0
    
    for i in range(0,len(label)):
        if label["push"][i] > 0 and label["down"][i] > 0:
            push_down += 1
        if label["push"][i] > 0:
            push_num += 1
        elif label["down"][i] > 0:
            down_num += 1     
        else:
            none_num += 1
            
    all_num = push_down + push_num + down_num + none_num
    
    print("同時推噓:", push_down, "推:", push_num, "噓:", down_num, "無推噓:", none_num)
    print('同時推噓: {:.2%}'.format(push_down/all_num), '推: {:.2%}'.format(push_num/all_num),
           '噓: {:.2%}'.format(down_num/all_num),'無推噓: {:.2%}'.format(none_num/all_num))

def useless_word(word):
    rule = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》；\n\t「」：（）？“”‘’！[\\]^_`{|}~]+'    #資料處理規則  
    word = re.sub(rule,'',word)
    if word == None:
        return None
    else:
        return word

def create_article_word_dict(data):  #建立所有文章各自的word dict
    all_word = []
    
    for i in range(0,10):#len(data)
        segment = data["segment_context"][i].split('/')
        segment = list(filter(useless_word, segment))    
        all_word.append(segment)
        
    return all_word
    
def create_tf_algo(all_word):
    tf_value = []
    
    for article in all_word:
        article_word = dict()
        length = len(article)
        
        for word in article:
            if word not in article_word:
                article_word[word] = 1
            else:
                article_word[word] += 1

        for key,value in article_word.items():
            article_word[key] = (value / length)
    
        tf_value.append(article_word)
      
    #print(tf_value)
    print("tf_algorithm is completed")        
    return tf_value
    
def create_idf_algo(all_word):
    word_set = set()#所有的word
    article_word = []
    article_num = len(all_word)#所有文章總數
    idf_dict = dict()
    
    for article in all_word:
        word_set.update(set(article))
        article_word.append(set(article))
    
    for word in word_set:
        idf = 1
        for article in article_word:
            if word in article:
                idf += 1
        
        idf_dict[word] = math.log(article_num / idf, 10)  #某word的idf值
        
    #print(idf_dict)
    print("idf_algorithm is completed")     
    return idf_dict
    
def create_tfidf_algo(tf_value, idf_value):
    tfidf_value = []
    for article in tf_value:
        tfidf = dict()
        
        for key, value in article.items():
            tfidf[key] = value * idf_value[key]
        
        tfidf_value.append(tfidf)
    
    #print(tfidf_value)
    print("tfidf_algorithm is completed") 
    return tfidf_value

def calc_distance(point1, point2):      
    point_dist = 0
    
    for key, value in point1.items():
        if point2.get(key):
            point_dist += pow((value - point2[key]), 2)
        else:
            point_dist += pow(value, 2)
                  
    return math.sqrt(point_dist)

def calc_distance_main(tfidf_train, tfidf_test): #計算test point離train point距離
    knn_value = []
   
    for article_test in tfidf_test:
        distance = dict()
        serial = 0
        
        for article_train in tfidf_train:
            distance[serial] = calc_distance(article_test, article_train)#計算兩點之間的距離
            serial += 1
               
        knn_value.append(distance)
        
    #print(knn_value)
    print("calc_distance is completed") 
    return knn_value


def main():
    train_data = pd.read_csv('train_data.csv')
    test_data = pd.read_csv('test_data.csv')
    
    get_data_characteristic()       #取得資料特徵
    
    #建立training的前置data
    all_word_train = create_article_word_dict(train_data)
    tf_value = create_tf_algo(all_word_train)
    idf_value = create_idf_algo(all_word_train)
    tfidf_train = create_tfidf_algo(tf_value, idf_value)
  
    #建立testing的前置data
    all_word_test = create_article_word_dict(test_data)
    tf_value = create_tf_algo(all_word_test)
    idf_value = create_idf_algo(all_word_test)
    tfidf_test = create_tfidf_algo(tf_value, idf_value)
    
    #取得test與train的距離
    knn_value = calc_distance_main(tfidf_train, tfidf_test)
    
if __name__== "__main__":
    main()   
    
