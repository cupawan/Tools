import os
import yaml
import requests
import csv
from datetime import datetime
import pytz

class OpenWeatherMap:
    def __init__(self, config_path):
        self.config_path = config_path
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.config = self.load_config()

    def load_config(self):
        config_path = os.path.join(self.current_dir, self.config_path)
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config
        except Exception as e:
            print("Error loading API_KEY")
            return {"API_KEY":"NO_KEY"}

    def save_csv(self, data):
        filepath = os.path.join(self.current_dir, 'Geocoding.csv')
        if not os.path.exists(filepath):
            with open(filepath, 'a+') as data_file:
                csvwriter = csv.writer(data_file)
                csvwriter.writerows([["Address", "Latitude", "Longitude"], data])
        else:
            with open(filepath, 'a+') as data_file:
                csvwriter = csv.writer(data_file)
                csvwriter.writerow(data)
   
    def epcoch_to_dtobj(self,ep):
        datetime_object_utc = datetime.utcfromtimestamp(ep)
        target_timezone = pytz.timezone('Asia/Kolkata')
        datetime_object_target_timezone = datetime_object_utc.replace(tzinfo=pytz.utc).astimezone(target_timezone)
        formatted_datetime = datetime_object_target_timezone.strftime("%d %b %I:%M %p")
        return formatted_datetime

    def geocode(self, address, limit=1):
        params = {'q': address, 'limit' : limit, 'appid' : self.config['API_KEY']}
        response = requests.get(url=self.config["GEOCODE"],params = params).json()[0]
        data = [address, response['lat'], response['lon']]
        self.save_csv(data=data)
        return response['lat'], response['lon']
    
    def request_weather_data(self,lat,lon, name = "User", location = None):
        location = f"({lat},{lon})" if not location else location
        params = {'lat': lat, 'lon' : lon, 'appid' : self.config['API_KEY'],'units' : 'metric'}
        response = requests.get(url = self.config["CURRENT_WEATHER"],params=params).json()
        data = response['current']
        cols = ["Data & Time", "Sunrise", "Sunset", "Tempreture", "Feels Like", "Pressure", "Humidity", "Dew Point", "UV Index", "Clouds", "Visibility", "Wind Speed", "Wind Degree"]
        vals = [str(self.epcoch_to_dtobj(data['dt'])),str(self.epcoch_to_dtobj(data['sunrise'])),str(self.epcoch_to_dtobj(data['sunset'])),f"{data['temp']}°C",f"{data['feels_like']}°C",f"{data['pressure']}mb",f"{data['humidity']}%",f"{data['dew_point']}°C",str(data["uvi"]),f"{data['clouds']}%",f"{data['visibility']} Metres",f"{data['wind_speed']}m/s",str(data['wind_deg'])]
        template = f"""Weather Report\n\nHello, {name}\nThe current weather report for {vals[0]} at {location} is as follows:\nSunrise: {vals[1]} | Sunset: {vals[2]}\nTemperature: {vals[3]}, Feels like: {vals[4]}\nAtmospheric Pressure: {vals[5]}, Humidity: {vals[6]}, Dew Point: {vals[7]}\nUV Index: {vals[8]}, Clouds Cover: {vals[9]}, Visibility: {vals[10]}\nWind Speed: {vals[11]}, Direction: {vals[12]}\nHave a nice day!"""
        return template                            
 
      

if __name__ == "__main__":
    config_path = input("Enter config path: ")    
    owm = OpenWeatherMap(config_path=config_path)
    latitude =float(input("Enter Latitude: "))
    longitude  = float(input("Enter longitude: "))
    weather_report = owm.request_weather_data(latitude,longitude)
    print(weather_report)


