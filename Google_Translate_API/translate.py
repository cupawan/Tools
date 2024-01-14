import requests
import yaml
import pandas as pd
import os

class Translator():
    def __init__(self,config_path):
        self.config_path = config_path
        self.config = self.load_api_key()
        self.base_url = "https://translation.googleapis.com/language/translate/v2"
        current_directory = os.path.dirname(os.path.realpath(__file__))
        self.csv_path = os.path.join(current_directory, 'languages.csv')
    def load_api_key(self):
        try:
            with open(self.config_path, 'r') as config_file:
                config = yaml.safe_load(config_file)
                return config['API_KEY']
        except FileNotFoundError:
            print(f"Config file not found at {self.config_path}")
            return None
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {self.config_path}: {e}")
            return None
    def detect_language(self, query):
        url = f"{self.base_url}/detect"
        payload = {
            'q' : query,
            'key' : self.config
        }
        response = requests.post(url = url, data = payload)
        if response.status_code == 200:
            result = response.json()['data']
            languages = [detection[0]['language'] for detection in result['detections'] if detection]
            return ",".join(languages)
        else:
            print("No response from the API, check if service is enabled on https://console.developers.google.com/apis/api/translate.googleapis.com/overview?project=<project_id>")

    def code_to_language(self,lang_code):
        df = pd.read_csv(self.csv_path)
        try:
            result = df.loc[df['Code'] == lang_code]['Language'].iloc[0]
            return result
        except IndexError:
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    def language_to_code(self,language):
        df = pd.read_csv(self.csv_path)
        try:
            result = df.loc[df['Language'] == language]['Code'].iloc[0]
            return result
        except IndexError:
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def translate(self,string,target):
        url = self.base_url
        payload = {
            'q' : string,
            'key' : self.config,
            'target' : target
        }
        response = requests.post(url = url, data = payload)
        if response.status_code == 200:
            data = response.json()['data']
            translations_info = [(translation['translatedText'], translation['detectedSourceLanguage']) for translation in data.get('translations', [])]
            if translations_info:
                translated_texts, source_languages = zip(*translations_info)
                full_source = []
                for i in source_languages:
                    full_source.append(self.code_to_language(i)) 
                translated_texts_str = ', '.join(translated_texts)
                source_languages_str = ', '.join(full_source)
            return translated_texts_str, source_languages_str
        else:
            print("No response from the API, check if service is enabled on https://console.developers.google.com/apis/api/translate.googleapis.com/overview?project=<project_id>") 


if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(current_directory, 'config.yaml')
    ins = Translator(config_path = config_path )
    target_language = input("Enter the language you want to translate to: ")
    target = ins.language_to_code(target_language)    
    query = input("Enter Sentence to translate: ")
    detected_language = ins.detect_language(query)
    if detected_language:
        print(f"Source: {detected_language}") 
        translation,source = ins.translate(query,target)
        print(f"{translation} (from {source})")

