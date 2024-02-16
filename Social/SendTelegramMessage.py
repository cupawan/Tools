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

    def get_updates(self, timeout = None, limit = None, offset = None, allowed_updates = None):
        params = {'timeout': timeout, 'limit': limit, 'offset' : offset, 'allowed_updates': allowed_updates}
        try:
            response = requests.get(url = self.get_updates_url, params=params)
            response.raise_for_status()
            print(f"Updates fetched successfully. Response: {response.json()['result']}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching updates: {e}")



if __name__ == "__main__":
    ins = TelegramMessage(config_file_path="tools_config.yaml")
    ins.send_message(message_type='plain', data = "", chat_id = "")