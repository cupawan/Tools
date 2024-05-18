import requests
from datetime import datetime, timedelta
import warnings
import pytz
import yaml

class StravaStats:
    def __init__(self,config_file_path):
        self.config_file_path = config_file_path
        self.config = self.load_config()
        self.access_token = self.get_access_token()

    def load_config(self):
        try:
            with open(self.config_file_path) as f:
                config = yaml.safe_load(f)
                return config
        except Exception as e:
            print(e)
            return {}

    def get_access_token(self):        
        payload = {
        'client_id': self.config['STRAVA_CLIENT_ID'],
        'client_secret': self.config["STRAVA_CLIENT_SECRET"],
        'refresh_token': self.config["STRAVA_REFRESH_TOKEN"],
        'grant_type': "refresh_token",
        'f': 'json'
        }
        res = requests.post(self.config['STRAVA_AUTH_URL'], data=payload, verify=False)
        access_token = res.json()['access_token']
        return access_token

    def access_activity_data(self, before:tuple, after:tuple, latest= False):
        if not latest:
            params:dict={
                'before':int(datetime(before[0],before[1],before[2]).timestamp()),
                'after':int(datetime(after[0],after[1],after[2]).timestamp())
                }
        elif latest:
            params:dict={
                'before':int(datetime.now().timestamp()),
                'after':int(datetime.now( - timedelta(days=1).timestamp()))
                }
        headers:dict = {'Authorization': f'Authorization: Bearer {self.access_token}'}
        if not params:
            response:dict = requests.get(self.config['STRAVA_ACTIVITIES_URL'], headers=headers)
        response:dict = requests.get(self.config['STRAVA_ACTIVITIES_URL'], headers=headers, params=params)
        response.raise_for_status()
        activity_data = response.json()
        return activity_data
    
    def msg_formatter(self,activity_data):
        msg = ''''''
        for i in activity_data[::-1]:
            dt = datetime.fromisoformat(i['start_date'].replace('Z', '+00:00'))
            ist = pytz.timezone('Asia/Kolkata')
            ist_dt = dt.astimezone(ist)
            formatted_datetime = ist_dt.strftime('%d %b %Y, %I:%M %p')
            msg += f"Date and Time: {formatted_datetime}\n"
            msg += f"Name: {i['name']}\n"
            msg += f"Type: {i['type']}\n"
            msg += f"Time: {i['moving_time']//60} Minutes {i['moving_time']%60} Seconds\n"
            msg += f"Average Speed: {(i['average_speed'])}\n"
            msg += f"Distance: {round(i['distance']/1000,2)} Kms\n"
            msg += f"Location:{i['location_city']}\n"
            msg += f"Start Latitude and Longitude: {i['start_latlng']}\n"
            msg += f"End Latitude and Longitude: {i['end_latlng']}\n"
            msg += f"Average Heart Rate: {i['average_heartrate']}\n"
            msg += f"Max Heart Rate: {i['max_heartrate']}\n"
            msg += 2*"\n"
        return msg


if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    config_path = "Tools/Configuration/tools_config.yaml"
    strava_instance = StravaStats(config_file_path=config_path)
    before = (2021,11,15)
    after = (2021,11,10)
    activity_data = strava_instance.access_activity_data(before=before, after = after, latest = False)
    message = strava_instance.msg_formatter(activity_data=activity_data)
    print(message)

    
    