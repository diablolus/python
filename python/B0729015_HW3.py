import csv
import jieba
import math
import time


def get_movie_data(name):
    movie_data = dict()
    with open(name, newline='', encoding="utf-8") as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            if row['movie No.'] != " " and row['Desc'] != " ":
                movie_data[row['movie No.']] = row['Desc']
                
    return movie_data

def jieba_cal(data):
    word = dict()
    for key,value in data.items():
        sentence = jieba.lcut(value, cut_all=False)
        word[key] = sentence
   
    return word

def tf_algorithm(word_dict): 
    
    tf_dict = dict()
    
    for number, word_list in word_dict.items():             #word_list為所有電影的字詞list
        temp = dict()
        length = len(word_list)
        
        for i in range(0,length):
            if word_list[i] not in temp:
                temp[word_list[i]] = 1
            elif word_list[i] in temp:
                temp[word_list[i]] += 1
        
        for key,value in temp.items():
            temp[key] = value / length         #計算TF值
          
        tf_dict[number] = temp                 #建立tf的dict
            
    return tf_dict

def idf_algorithm(word_dict, tf_dict):  
    all_word = set()
    idf_dict = dict()
    length = len(word_dict)
    
    for word_list in word_dict.values():
        word_set = set(word_list)
        all_word.update(word_set)

    for word in all_word:
        idf = 1 #idf=0會有問題
        
        for value in tf_dict.values():                  #計算所有存在該word的檔案
            if word in value:  
                idf += 1
        
        idf_dict[word] = math.log(length / idf, 10)  #某word的idf值
        
    return idf_dict

def tfidf_algorithm(tf_dict, idf_dict): #
    tfidf_dict = dict()
    
    for number, word_dict in tf_dict.items():
        
        temp = dict()
        
        for key,value in word_dict.items():     #計算tfidf的值
            temp[key] = value * idf_dict[key]
        
        tfidf_dict[number] = temp

    return tfidf_dict

def calc_distance(point1, point2):      #計算文章與文章的距離
    distance = 0
    
    for key, value in point1.items():
        if point2.get(key):
            distance += pow((value - point2[key]), 2)
        else:
            distance += pow(value, 2)
                  
    return math.sqrt(distance)

def calc_distance_main(tfidf_data):
    length = len(tfidf_data)
    distance = []
    
    for i in range(1, length):
        temp = dict()
        
        for j in range(1, length):
            point1 = tfidf_data[str(i)]
            point2 = tfidf_data[str(j)]
            
            temp[str(j)] = calc_distance(point1, point2)
            
        distance.append(temp)
        
    print(len(distance))
    return distance

def get_neighbors(distance, k):
    for i in range(1,len(distance)):
        distance[i].sort()
        

def main():
    name = "dct1.csv"
    movie_data = get_movie_data(name)  
    word_dict = jieba_cal(movie_data)
    
    tf = tf_algorithm(word_dict)
    idf = idf_algorithm(word_dict,tf)
    tfidf = tfidf_algorithm(tf, idf)
    distance = calc_distance_main(tfidf)
  
if __name__== "__main__":
    main() 
