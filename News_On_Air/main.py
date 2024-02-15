import requests
from bs4 import BeautifulSoup
import os
import yaml
from datetime import datetime

class NewsOnAIR:
    def __init__(self, language):
        self.language = language
        self.base_url = "https://newsonair.gov.in/"
        if self.language.lower() not in ['hindi', 'english']:
            raise ValueError
    
    def save_news(self, audio_link, title):
        response = requests.get(audio_link)
        os.makedirs("Audio", exist_ok=True)
        if response.status_code == 200:
            with open(f"Audio/{title}", 'wb') as audioFile:
                audioFile.write(response.content)
                return f"Audio/{title}"
        else:
            return None

    def get_news(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.content, features='lxml')
        try:
            newsboxes = soup.select('.accordion-body')
            nb = newsboxes[0] if self.language.lower() == 'english' else newsboxes[1]
            if self.language.lower() == "hindi":
                nb = newsboxes[1]
            elif self.language.lower() == "english":
                nb = newsboxes[0]
            all_audio_elements = nb.find_all('audio')
            for i, audio_element in enumerate(all_audio_elements):
                audio_link = audio_element.get('src')
                filename = audio_link.split('/')[-1]
                if not filename.endswith('.mp3'):
                    filename = filename + ".mp3"
                self.save_news(title=filename, audio_link=audio_link)
        except Exception as e:
            print(f"An Error Occurred: {str(e)}")
            return None


if __name__ == "__main__":
    ni = NewsOnAIR(language='English')
    ni.get_news()