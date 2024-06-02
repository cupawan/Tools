import yaml
import requests


class GoogleGeocoding:
    def __init__(self, config_path):
        self.config_path = config_path
        self.api_key = self.load_api_key()
        self.base_url = "https://api.opencagedata.com/geocode/v1/json"
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
    def validateInput(self,user_input):
        print("Validating Address...")
        try:
            user_input = user_input.strip()
        except Exception as e:
            print("Sorry, not a valid input")
        return user_input
    def geocode(self, user_input):
        params = {
            'q': user_input,
            'key': self.api_key,
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                first_result = data['results'][0]
                latitude = first_result['geometry']['lat']
                longitude = first_result['geometry']['lng']
                formatted_address = first_result['formatted']
                return {'latitude': latitude, 'longitude': longitude, 'formatted_address': formatted_address}
            else:
                return {'error': 'No results found for the provided location.'}
        else:
            return {'error': f'Request failed with status code {response.status_code}'}
            
if __name__ == "__main__":
    geocoding_instance = GoogleGeocoding(config_path='config.yaml')
    user_input = input("Enter Address: ")
    user_input = geocoding_instance.validateInput(user_input=user_input)
    result = geocoding_instance.geocode(user_input=user_input)
    print(result)


    
