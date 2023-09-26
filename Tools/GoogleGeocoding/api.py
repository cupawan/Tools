import googlemaps
import sys
import yaml
import json

def loadConfig(file_path):
    try:
        with open(file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        return config['API_KEY']
    except FileNotFoundError:
        print(f"Config file not found at {file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML in {file_path}: {e}")
        return None


def fileSaver(filename):
    d = {'results':[]}
    with open(filename, 'w') as f:
        f.write("")


def validateInput(user_input):
    print("Validating Address...")
    try:
        user_input = user_input.strip()
    except Exception as e:
        print("Sorry, not a valid input")
        return None
    return user_input

def callAPI(user_input):
    api_key = loadConfig("config.yaml")
    gmaps = googlemaps.Client(api_key)
    print("Calling API")
    geocoder_response = gmaps.geocode(user_input)[0]
    key = geocoder_response["address_components"][0]["short_name"]
    print(key)
    d = {key:[]}
    d[key].append(geocoder_response)
    with open(f'{key}_geocoding.json', 'a+') as result:
        result.write(json.dumps(d, indent=3))
    return "OK"


if __name__ == "__main__":
    user_input = validateInput(','.join(sys.argv[1:]))
    print(callAPI(user_input=user_input))
    print('Done') 


    
