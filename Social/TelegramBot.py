import yaml
import requests


class TelegramMessage:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = self.load_config()
        self.token = self.config['TELEGRAM_BOT_TOKEN']
        self.audio_url = f"https://api.telegram.org/bot{self.token}/sendAudio"
        self.document_url = f"https://api.telegram.org/bot{self.token}/sendDocument"
        self.image_url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
        self.plain_url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        self.get_updates_url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        self.get_me = f"https://api.telegram.org/bot{self.token}/getMe"
        self.download_url = f"https://api.telegram.org/file/bot{self.token}/{self.config['TELEGRAMBOTDOWNLOADPATH']}"

    def load_config(self):
        try:
            with open(self.config_file_path, 'r') as f:
                config = yaml.safe_load(f)
                return config
        except Exception as e:
            d = {}
            return d
        
    def send_message(self, message_type, data, chat_id, caption = None):
        if message_type.lower() == 'plain':
            url = self.plain_url
            data_payload = {'chat_id': chat_id, 'text': data, 'parse_mode' : 'HTML'}
            files_payload = None
        elif message_type.lower() == 'audio':
            url = self.audio_url
            data_payload = {'chat_id': chat_id, 'caption': caption}
            files_payload = {'audio': open(data, 'rb')}
        elif message_type.lower() == 'document':
            url = self.document_url
            data_payload = {'chat_id': chat_id, 'caption': caption}
            files_payload = {'document': open(data, 'rb')}
        elif message_type.lower() == 'image':
            url = self.image_url
            data_payload = {'chat_id': chat_id, 'caption': caption}
            files_payload = {'photo': open(data, 'rb')}
        else:
            print("Unsupported message type.")
            return
        try:
            response = requests.post(url, data=data_payload, files=files_payload)
            response.raise_for_status()
            print(f"Message sent successfully. Response: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")

    def get_updates(self, timeout = None, limit = None, offset = None, allowed_updates = None, download_file = False):
        file_ids = []
        params = {'timeout': timeout, 'limit': limit, 'offset' : offset, 'allowed_updates': allowed_updates}
        response = requests.get(url = self.get_updates_url, params=params)
        response.raise_for_status()
        try:
            response = response.json()
            if response['ok'] and len(response['result']) > 0:
                output = ''''''
                only_message = ''''''
                for i in response['result']:
                    if 'text' in i['message'].keys():
                        message = i['message']['text']
                    else:
                        message = "INFO> File type is different"
                        file_ids.extend(list(set([j['file_id'] for j in i['message']['photo']])))
                    sent_by = i['message']['from']['first_name'] if i['message']['from']['first_name'] else i['message']['from']['id']          
                    out = f"{sent_by}: {message}\n"
                    output += out
                    only_message += message
            if file_ids:
                return output, only_message, file_ids            
            return output, only_message
        except requests.exceptions.RequestException as e:
            print(f"Error fetching updates: {e}")

    def get_last_message(self):
        response_ = requests.get(self.get_updates_url).json()
        if len(response_['result']) > 0:
            last_update_id = response_['result'][-1]['update_id'] 
        else:
            return "No New Messages"    
        response = requests.get(self.get_updates_url, data = {'offset': last_update_id}).json()
        if response['ok'] and len(response['result']) > 0:
            output = ''''''
            only_message = ''''''
            for i in response['result']:
                message = i['message']['text']
                sent_by = i['message']['from']['first_name'] if i['message']['from']['first_name'] else i['message']['from']['id']          
                out = f"{sent_by}: {message}\n"
                output += out
                only_message += message
            return output, only_message
                
        else:
            return "No New Messages"

    def download_file(self, file_ids):
        for i in file_ids:
            response = requests.get(url = self.download_url, data = {'file_id': i})
            print(response.text)
            if response.status_code == 200:
                print(f"File has been downloaded successfully")
            else:
                print("Error downloading file")