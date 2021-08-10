import csv
import jieba
import math

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
    for key,value in data:
        sentence = jieba.lcut(value, cut_all=False)
        word[key] = sentence
   
    return word

def cal_all_word_num(word_list):         #
    count_list = []
        
    for i in range(0,len(word_list)):
        count_list.append(len(word_list[i]))

    return count_list
 
def tf_algorithm(word_freq_list, count_list): #
    freq_list = []
    length = len(word_freq_list)
    
    for i in range(0, length):
        temp = dict()
        for key, value in word_freq_list[i].items():
            temp[key] = (value / count_list[i])
        freq_list.append(temp)
        
    return freq_list


def idf_algorithm(word_freq_list):  #

    length = len(word_freq_list) #
    all_word = []
    ifd_dict = dict()
    temp = dict()
    
    for i in range(0, length):
        all_word.extend(word_freq_list[i])
    
    for word in all_word:
        if temp.__contains__(word) != True:
            temp[word] = 1
        else:
            temp[word] += 1 
    
    for key, value in temp.items():
        ifd_dict[key] = math.log(length/value,10)
    
    return ifd_dict

def tfidf_algorithm(tf_num,idf_num): #
    tfidf_num = []

    for i in range(0,len(tf_num)):
        temp = dict()
        for key,value in tf_num[i].items():
            temp[key] = value * idf_num[key]
        tfidf_num.append(temp)
    
    return tfidf_num

def main():
    name = "dct.csv"
    get_movie_data(name)  
  
if __name__== "__main__":
    main() 
