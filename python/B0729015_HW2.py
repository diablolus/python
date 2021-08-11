import requests
from bs4 import BeautifulSoup
import math
import random
from fake_useragent import UserAgent
import csv

def get_soup(address):
    user_agent = UserAgent()
    proxy_list = [
        'http://34.138.225.120:8888',
        'http://35.232.28.68:8080',
        'http://69.78.101.142:443',
        'http://198.199.86.11:3128',
        'http://34.121.55.127:8080',
        'http://170.106.175.94:80',
        'http://52.149.152.236:80',
    ]
    
    proxy_ip = random.choice(proxy_list) # 隨機取得代理ip

    headers = {
        'http': proxy_ip,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "zh-TW,zh;q=0.9", 
        "Host": "movies.yahoo.com.tw",  #目標網站 
        "Sec-Fetch-Dest": "document", 
        "Sec-Fetch-Mode": "navigate", 
        "Sec-Fetch-Site": "none", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": user_agent.random
    }
    
    r = requests.get(url = address, headers = headers)
    soup = BeautifulSoup(r.text,"html.parser")
    
    return soup

def get_movie_address_main():
    url = "https://movies.yahoo.com.tw/moviegenre_result.html?"
    movie_address = []
    
    for web_id in range(1, 5):
        address_main = url+"genre_id="+str(web_id)
        soup = get_soup(address_main)
        movie_address.extend(get_movie_address(soup))

        length_str = soup.find('div', class_ = "release_time _c").find("p").text
        local1 = length_str.find("共")
        local2 = length_str.find("筆")
        length = math.ceil(int(length_str[local1+1:local2])/10)
        
        for page in range(2, length):
            address_mov = address_main + "&page=" + str(page)
            soup = get_soup(address_mov)
            movie_address.extend(get_movie_address(soup))
        
    return movie_address
    
def get_movie_address(soup):
    soup = soup.select("div.en")
    href = []
    for a in soup:
        href.append(a.select_one("a").get("href"))
        
    return href
   

def get_movie_info(address):
    soup = get_soup(address)

    main_info = soup.select("div.movie_intro_info_r")
    desc_info = soup.select("span#story")
    type_info = soup.select('div.level_name_box')
    
    if main_info is None or desc_info is None or type_info is None:
        return False
    
    data = dict()
    
    for info1 in main_info:
        movie_name = info1.find('h1').text.strip()
        movie_date = info1.findAll('span')[0].text[5:].strip()
        movie_length = info1.findAll('span')[1].text[5:].strip()
        movie_company = info1.findAll('span')[2].text[5:].strip()
        movie_imdb = info1.findAll('span')[3].text[7:].strip()
        movie_director = info1.find('div', class_ = 'movie_intro_list').text.strip().replace('\n', '').replace('\r', '').replace(" ", "")
        movie_actor = info1.findAll('div', class_ = 'movie_intro_list')[1].text.strip().replace(" ", "").replace('\n', '').replace('\r', '')
        
    for info2 in desc_info:
        movie_desc = info2.text.strip().replace('\n', '')
    
    for info3 in type_info:
        movie_tag = info3.findAll('a', class_ ="gabtn")[0]
        
    data[movie_name] = [movie_tag, movie_date, movie_length, movie_company, movie_imdb, movie_director, movie_actor, movie_desc]
    
    return data
    
def main():
    movie_info = dict()
    address_set = set(get_movie_address_main())
    address_list = list(address_set)
          
    with open('dct.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["movie No.", "Name", "Tag", "Date", "Length", "Company", "Imdb", "Director", "Actor", "Desc"])
        j = 1
        for i in range(0, len(address_list)):
            movie_info = get_movie_info(address_list[i])
            
            if movie_info == False:
                print("false")
                continue
            
            print(j)
            for mov_title, mov_data in movie_info.items():
                writer.writerow([j, mov_title, mov_data[0], mov_data[1], mov_data[2], mov_data[3], mov_data[4], mov_data[5], mov_data[6], mov_data[7]])
                j += 1
        
if __name__== "__main__":
    main() 
