import yaml
import googlemaps
import pandas as pd
from tabulate import tabulate
import os

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
    
    def parse_response(self,response):
        print(f"Fetched {len(response)} results")
        result_df = pd.DataFrame()
        d = {'Formatted_Address': [], "Latitude": [], "Longitude" : [], 'Long Name': [], "Short Name" : [], "Location Type": []}
        for result in response:
            d['Formatted_Address'].append(result['formatted_address'])
            d['Latitude'].append(result['geometry']['location']['lat'])
            d['Longitude'].append(result['geometry']['location']['lng'])
            d['Long Name'].append(result['address_components'][0]['long_name'])
            d['Short Name'].append(result['address_components'][0]['short_name'])
            d['Location Type'].append(result['geometry']['location_type'])
            temp = pd.DataFrame(d)
            result_df = pd.concat([result_df,temp])
        return result_df.drop_duplicates().transpose().rename(columns={0:''})
    def geocode(self, user_input):
        api_key = self.api_key
        gmaps = googlemaps.Client(api_key)
        geocoder_response = gmaps.geocode(user_input)
        return geocoder_response
            
if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(current_directory, 'config.yaml')
    geocoding_instance = GoogleGeocoding(config_path=config_path)
    user_input = input("Enter Address: ")
    user_input = geocoding_instance.validateInput(user_input=user_input)
    result = geocoding_instance.geocode(user_input=user_input)
    df = geocoding_instance.parse_response(result)
    print(tabulate(df, headers='keys', tablefmt='fancy_grid'))


    
