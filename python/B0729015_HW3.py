import csv
import jieba

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

name = "dct.csv"
get_movie_data(name)    