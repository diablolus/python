import requests
from bs4 import BeautifulSoup
import math
import random
from fake_useragent import UserAgent
import csv

def get_soup(address):
    user_agent = UserAgent()
    proxy_list = [
        'http://138.68.60.8:8080',
        'http://209.97.150.167:8080',
        'http://191.96.42.80:8080',
        'http://198.199.86.11:3128',
        'http://35.232.28.68:8080',
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
            
        print(web_id)
        
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
    
    data = dict()
  
    for info1 in main_info:
        title = info1.find('h1').text
        date = info1.findAll('span')[0].text[5:]
        length = info1.findAll('span')[1].text[5:]
        company = info1.findAll('span')[2].text[5:]
        imdb = info1.findAll('span')[3].text[7:]
        director = info1.find('div', class_ = 'movie_intro_list').text.strip().replace('\n', '').replace('\r', '').replace(" ", "")
        actor = info1.findAll('div', class_ = 'movie_intro_list')[1].text.strip().replace(" ", "").replace('\n', '').replace('\r', '')
        
    for info2 in desc_info:
        desc = info2.text.strip().replace('\n', '')
    
    for info3 in type_info:
        temp = info3.findAll('a', class_ ="gabtn")
        for x in temp:
            tag = x.text.strip()
            break
        
    data[title] = [tag, date, length, company, imdb, director, actor, desc]
    return data
    
def main():
    movie_info = dict()
    address_set = set(get_movie_address_main())
    address_list = list(address_set)
          
    with open('dct.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        j = 1
        for i in range(0, len(address_list)):
            movie_info = get_movie_info(address_list[i])
            print(movie_info)
            writer.writerow(["movie No.", "Name", "Tag", "Date", "Length", "Company", "Imdb", "Director", "Actor", "Desc"])
            for title,data in movie_info.items():
                writer.writerow([j, title, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]])
                j += 1
        
if __name__== "__main__":
    main() 
