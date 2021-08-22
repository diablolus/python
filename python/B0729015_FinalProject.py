from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re

def useless_word(word):
    rule = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<u3000=uffbf>?@ωㄧ，。?★、…【】《》；\n\t「」：（）？“”‘’！[\\]^_`{|}~]+'    #資料處理規則  
    word = re.sub(rule,'',word)
    if word == None:
        return None
    else:
        return word

def get_article_word(data, start, end):  #建立所有文章各自的word dict
    all_word = []
    
    for i in range(start, end):#len(data)
        segment = data["segment_context"][i].split('/')
        segment = str(list(filter(useless_word, segment)))
        all_word.append(segment)
        
    return all_word
    
def get_tfidf_value(train, test):
    tfidf = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
    train_weight = tfidf.fit_transform(train).toarray() #tfidf權重
    test_weight = tfidf.transform(test).toarray()
    #word = tfidf.get_feature_names()
  
    return (train_weight, test_weight)

def knn_algo(train_data, test_data, train_label, start, end):
    label_push = train_label["push"][start:end]
    label_down = train_label["down"][start:end]

    knn = KNeighborsClassifier()
    knn.fit(train_data, label_push)
    push = knn.predict(test_data)
    
    knn.fit(train_data, label_down)
    down = knn.predict(test_data)
    
    return (push, down)
    
def write_result(csv_name, push, down, start, end):
    index = list(range(start, end))
    if start == 0:
        dataframe = pd.DataFrame({'index':index, 'push':push, 'down':down})
        dataframe.to_csv(csv_name, mode="w", index=False, sep=',')
    else:
        dataframe.to_csv(csv_name, mode="a", index=False, sep=',')
    
    return 

def main():
    train_data = pd.read_csv('train_data.csv')
    train_label = pd.read_csv('train_label.csv')
    test_data = pd.read_csv('test_data.csv')
    result_data = "sample_submission.csv"
    
    start = [0,10000,20000,30000]
    end = [10000,20000,30000, len(test_data)]

    for i in range(0,4):
        print(i)
        #建立training的前置data
        all_train_word = get_article_word(train_data, start[i], end[i])
        #建立testing的前置data
        all_test_word = get_article_word(test_data, start[i], end[i])
        
        train_weight, test_weight = get_tfidf_value(all_train_word, all_test_word)
        push, down = knn_algo(train_weight, test_weight, train_label, start[i], end[i])
 
        write_result(result_data, push, down, start[i], end[i])
    
if __name__== "__main__":
    main()   
    