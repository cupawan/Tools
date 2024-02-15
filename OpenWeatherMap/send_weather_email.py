from Social.SendEmail import SendEmail
import os
from OpenWeatherMap.main import OpenWeatherMap





if __name__ == "__main__":
    config_file_path = os.environ.get("CONFIG_PATH")
    if not config_file_path:
        print("CONFIG FILE PATH NOT SET")
    contacts = {'username@gmail.com' :[('latitude_value', 'longitude_value'),'location','name'], 'username2@gmail.com' :[('latitude_value2', 'longitude_value2'),'location2', 'name2']}
    try:
        owm = OpenWeatherMap(config_path= config_file_path)
        gc = SendEmail(config_file_path =config_file_path, is_html = True)
        for key,value in contacts.items():
            rec_mail = key
            name = value[-1]
            location,latitude,longitude  = value[1],value[0][0],value[0][1] 
            body = owm.request_weather_data(lat = latitude, lon=longitude, name = name, location=location)
            gc.send_email(rec_email=rec_mail,subject="Today's Weather Report",body = body)
            print("Email Sent to {}".format(name))
    except Exception as e:
        print("There was an error: {}".format(e))