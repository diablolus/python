import csv
import jieba
import math

def get_movie_data(name):           #取得desc資料
    movie_data = dict()
    
    with open(name, newline='', encoding="utf-8") as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            if row['movie No.'] != "None" and row['Desc'] != " ":
                movie_data[row['movie No.']] = row['Desc'] + row['Date'] + row['Director'] + row['Actor']
                
    return movie_data

def get_movie_tag(name):            #取得tag資料
    movie_tag = dict()
    
    with open(name, newline='', encoding="utf-8") as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            if row['movie No.'] != None and row['Tag'] != " ":
                movie_tag[row['movie No.']] = row['Tag']
                
    return movie_tag

def jieba_cal(data):
    word = dict()
    #jieba.set_dictionary('dict.txt')

    for key,value in data.items():
        sentence = jieba.lcut(value)
        word[key] = sentence
   
    return word

def tf_algorithm(word_dict): 
    
    tf_dict = dict()
    
    for number, word_list in word_dict.items():             #word_list為所有電影的字詞list
        temp = dict()
        length = len(word_list)
        
        for i in range(0, length):
            if word_list[i] not in temp:
                temp[word_list[i]] = 1
            elif word_list[i] in temp:
                temp[word_list[i]] += 1
        
        for key,value in temp.items():
            temp[key] = value / length         #計算TF值
          
        tf_dict[number] = temp                 #建立tf的dict
    
    print("tf_algorithm is completed")        
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
    
    print("idf_algorithm is completed")     
    return idf_dict

def tfidf_algorithm(tf_dict, idf_dict): #
    tfidf_dict = dict()
    
    for number, word_dict in tf_dict.items():
        
        temp = dict()
        
        for key,value in word_dict.items():     #計算tfidf的值
            temp[key] = value * idf_dict[key]
        
        tfidf_dict[number] = temp
    
    print("tfidf_algorithm is completed") 
    return tfidf_dict

#計算文章與文章的距離
def calc_distance(point1, point2):      
    point_dist = 0
    
    for key, value in point1.items():
        if point2.get(key):
            point_dist += pow((value - point2[key]), 2)
        else:
            point_dist += pow(value, 2)
                  
    return math.sqrt(point_dist)

def calc_distance_main(tfidf_data, start, end):
    length = len(tfidf_data)
    dist = dict()
    
    for i in range(start, end+1):
        temp = dict()
        
        for j in range(1, length+1):
            point1 = tfidf_data[str(i)]
            point2 = tfidf_data[str(j)]
            
            temp[str(j)] = calc_distance(point1, point2)    #計算兩點之間的距離
    
        dist[str(i)] = temp
        
    print("calc_distance is completed") 
    return dist

#取得離該點最近的k個鄰居
def get_neighbors(distance, k):
    neighbor = dict()
    
    for key, value in distance.items():
        temp = dict()

        for i in range(0, k):
            min_item = min(value, key=value.get)            
            if value[min_item] == 0:
                value.pop(min_item)
            else:
                temp[min_item] = value[min_item]              
                value.pop(min_item)
                
        neighbor[key] = temp
    
    print("get_neighbors is completed")     
    return neighbor

#判斷start~end個點最近鄰居最多的類別        
def get_tag(neighbor, movie_tag, start, end):
    guess_tag = dict()
    
    for i in range(start, end+1):
        temp_tag = dict()
        
        for k in neighbor[str(i)]:
            if movie_tag[k] not in temp_tag:
                temp_tag[movie_tag[k]] = 1
            elif movie_tag[k] in temp_tag:
                temp_tag[movie_tag[k]] += 1

        guess_tag[str(i)] = max(temp_tag, key=temp_tag.get)
    
    print("get_tag is completed")  
    return guess_tag

def pred_result(guess_tag, movie_tag, num):
    correct = 0
    for k, v in guess_tag.items():
        if v == movie_tag[k]:
            correct += 1
            
    print("算法精準度:",correct/num) 
    return correct/num
    
def main():
    file_name = "dct.csv"
    start = 5500
    end = 6000
    num = end - start
    
    #取得測試資料
    movie_data = get_movie_data(file_name)  
    movie_tag = get_movie_tag(file_name)
    word_dict = jieba_cal(movie_data)
    
    #TF-IDF計算
    tf = tf_algorithm(word_dict)
    idf = idf_algorithm(word_dict,tf)
    tfidf = tfidf_algorithm(tf, idf)
    
    distance = calc_distance_main(tfidf, start, end)
    neighbor = get_neighbors(distance, 17)
    
    #6000筆資料，取500筆作測試，算出預測成功率
    guess_tag = get_tag(neighbor, movie_tag, start, end)
    pred_result(guess_tag, movie_tag, num)
  
if __name__== "__main__":
    main() 
