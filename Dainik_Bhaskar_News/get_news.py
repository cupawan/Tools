import requests
from bs4 import BeautifulSoup


class News:
    def __init__(self,state = None, city = None):
        self.bhaskar_base_url = "https://www.bhaskar.com/"
        self.db_categories = ['career','ayodhya-ram-mandir','db-original',f'mera-shaher/local/{state}/{city}','sports/cricket','entertainment','lifestyle','israel-hamas-war','women','national','international','business','tech-auto','jeevan-mantra','sports','no-fake-news','opinion','madhurima','magazine','happylife','utility']

    def url_builder(self,category):
        category = category.lower()
        if category in self.db_categories:
            return self.bhaskar_base_url + category
    def fetch_bhaskar_news(self,category):
        url = self.url_builder(category=category)
        all_urls_dict = {}
        all_urls = []
        msgbody = ''''''
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                headlines = soup.find_all(class_='c7ff6507')
                for i in headlines:
                    for j in i.contents:
                        all_urls_dict[j.text] = []
                        slug = j.get('href')
                        if slug:
                            all_urls_dict[j.text].append(url+slug)
                            all_urls.append(url+slug)
                for key,value in all_urls_dict.items():
                    headline = key
                    news = ''''''
                    for i in value:
                        response = requests.get(i)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        news_element = soup.find_all('p')
                        for n in news_element:
                            news += n.text
                    msgbody += "<mark><h3>" + headline + "</h3></mark>"+ '\n'
                    msgbody += "<p>" + news + "</p>" + '\n'

            return msgbody
        except Exception as e:
            return msgbody



