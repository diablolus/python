# -*- coding: utf-8 -*-
import jieba
import math
import matplotlib.pyplot as plt

def jieba_cal():
    f = open('hw1-dataset.txt', 'r', encoding = 'utf8')
    result = []
    while True:
        text = f.readline().replace("\t"," ").replace("\n","")
        if not text:
            break
        sentence = jieba.lcut(text,cut_all=False)
        filter(None, sentence)
        result.append(sentence)
    f.close()
    return result

def cal_single_sentence(word_list):     #�p��C�g�峹���ӧO�Ҧ������W�v
    word_freq_list = []
    word_list_len = len(word_list)
    
    for i in range(0,word_list_len):
        word_freq = dict()
        for j in range(0,len(word_list[i])):
            if(word_list[i][j] != " " and word_list[i][j] not in word_freq):
                count = word_list[i].count(word_list[i][j])
                word_freq[word_list[i][j]] = count
        word_freq_list.append(word_freq)
        
    return word_freq_list

def cal_all_word_num(word_list):         #�p���@�峹�`����
    count_list = []
        
    for i in range(0,len(word_list)):
        count_list.append(len(word_list[i]))

    return count_list
 
def tf_algorithm(word_freq_list, count_list): #�Y�@���y�X�{�����ư��H���ɮת��`���y��
    freq_list = []
    length = len(word_freq_list)
    
    for i in range(0, length):
        temp = dict()
        for key, value in word_freq_list[i].items():
            temp[key] = (value / count_list[i])
        freq_list.append(temp)
        
    return freq_list


def idf_algorithm(word_freq_list):  #�ɮ��`�ơA���H�X�{�Y�@�_�����ɮ׼�

    length = len(word_freq_list) #�ɮ��`��
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

def tfidf_algorithm(tf_num,idf_num):
    tfidf_num = []

    for i in range(0,len(tf_num)):
        temp = dict()
        for key,value in tf_num[i].items():
            temp[key] = value * idf_num[key]
        tfidf_num.append(temp)
    
    return tfidf_num

def select_data(data):
    temp = dict()
    max_dict = dict()
    for i in range(0, len(data)):
        max_price = max(zip(data[i].values(), data[i].keys()))
        temp[max_price[1]] = max_price[0]
    
    for i in range(0, 100):
        max_price = max(zip(temp.values(), temp.keys()))
        max_dict[max_price[1]] = max_price[0]
        del temp[max_price[1]]
         
    return max_dict  


def make_picture(result):
    xpt = []
    ypt = []
    i = 0
    for x,y in result.items():
        print(i, ":", x)
        xpt.append(i)
        ypt.append(y)
        i += 1
        
    plt.plot(xpt,ypt)
    plt.show()

def main():
    article_list = jieba_cal()
    single_word_freq = cal_single_sentence(article_list)
    count_list = cal_all_word_num(single_word_freq)
    
    tf_num = tf_algorithm(single_word_freq, count_list)
    idf_num = idf_algorithm(single_word_freq)
    tfidf_num = tfidf_algorithm(tf_num,idf_num)

    result_list1 = select_data(tfidf_num)
    result_list2 = select_data(tf_num)
    
    make_picture(result_list1)
    make_picture(result_list2)
  
if __name__== "__main__":
    main() 

