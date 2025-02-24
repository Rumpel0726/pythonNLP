import requests
from bs4 import BeautifulSoup

from database import DBObj


class ParseObj:
    def __init__(self):
        self.db = DBObj()

    def parse_main(self, url):
        page_cont = ''
        title = ''
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'lxml')
        divs = soup.find_all('div', class_='news-feed')

        ul = divs[1].find_all('ul')
        for li in ul[0].find_all('li'):
            i = li.find_all('a')
            if (len(li.find_all('h3')) > 0):
                dt = li.find_all('h3')[0].text
            if (len(li.find_all('span')) > 0):
                tm = li.find_all('span')[0].text

            if (len(i) > 0):
                url = i[0].get('href')
                print("https://www.yarnews.net" + url)

                page_cont = self.get_page_cont("https://www.yarnews.net" + url)
                title = i[0].text
                self.db.insert_data(title, "https://www.yarnews.net" + url, page_cont, str(dt)+" "+str(tm))

    def get_page_cont(self, url):
        response2 = requests.get(url)
        html_content = response2.content
        soup = BeautifulSoup(html_content, 'lxml')
        divs = soup.find_all('div', class_='text')
        content = ''
        for i in divs[0].find_all('p'):
            content += i.text
        return content



# url = 'https://www.yarnews.net/news/bymonth/2014/12/0/'
# response = requests.get(url)
# html_content = response.content
# soup = BeautifulSoup(html_content, 'lxml')
# divs = soup.find_all('div', class_='news-feed')
# ul = divs[1].find_all('ul')
# print(ul[0])
# # for i in ul[0].find_all('a'):
# #     print("https://www.yarnews.net" + i.get('href'))
# print("https://www.yarnews.net" + ul[0].find_all('a')[0].get('href'))
# response2 = requests.get("https://www.yarnews.net" + ul[0].find_all('a')[0].get('href'))
# html_content = response2.content
# soup = BeautifulSoup(html_content, 'lxml')
# divs = soup.find_all('div', class_='text')
# content = ''
# for i in divs[0].find_all('p'):
#     content += i.text
# print(content)
# hr = ul[0].find_all('a')[0].get('href')
#
# print("https://www.yarnews.net" + hr)




