from Social.SendEmail import SendEmail
from WebScraping.Weather_Scraper.weather_scraper_v2 import Weather
import os




if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(current_directory, 'config.yaml')
    send_to = input("Enter the email address you are sending mail to: ")
    wi = Weather(location = 'Bangalore',sleep = 1, verbose=False)
    body = wi.check_weather()
    mail_instance = SendEmail(config_file_path='config.yaml',is_html=True)
    mail_instance.send_email(rec_email=send_to,subject= f'Weather Report {wi.location.replace("_"," ").title()}', body = body)
    
    