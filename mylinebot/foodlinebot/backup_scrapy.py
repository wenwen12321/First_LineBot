from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests

# 美食抽象類別
class Food(ABC):
    def __init__(self, area):
        self.area = area #地區

    @abstractmethod
    def scrape(self): 
        pass
        #共同的介面，未來新增的美食網頁爬蟲，就可以依據各自的邏輯來實作這個介面

# 愛食記 爬蟲
class IFoodie(Food):
 
    def scrape(self):
        # response = requests.get(
        #     "https://ifoodie.tw/explore/" + self.area +
        #     "/list?sortby=popular&opening=true")
        response = requests.get(
           "https://ifoodie.tw/explore/" + self.area + "/list?sortby=rating")

            

        soup = BeautifulSoup(response.content, "html.parser")

        # 爬取前五筆餐廳卡片資料
        cards = soup.find_all('div', {'class': 'jsx-558691085 restaurant-info'}, limit=5) 
        # print("\n\n\n\n\n", cards, "\n\n\n\n\n")
        
        content = ""
        for card in cards:
 
            title = card.find(  # 餐廳名稱
                "a", {"class": "jsx-558691085 title-text"}).getText()
            # print("\n\n\n\n\n----------------------------", type(title), "\n\n\n\n")
 
            stars = card.find(  # 餐廳評價
                "div", {"class": "jsx-1207467136 text"}).getText()
 
            address = card.find(  # 餐廳地址
                "div", {"class": "jsx-558691085 address-row"}).getText()
 
            # 將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
            content += f"{title} \n{stars}顆星 \n{address} \n\n"


 
        return content
