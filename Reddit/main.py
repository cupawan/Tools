import requests
import yaml
import json
import praw
from email_script import EmailWithPython

class RedditData:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()
        self.USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config
        except Exception as e:
            return None

    def auth(self):
        reddit = praw.Reddit(client_id=self.config['REDDIT_CLIENT_ID'],
                             client_secret=self.config['REDDIT_CLIENT_SECRET'],
                             username=self.config['REDDIT_USERNAME'],
                             password=self.config['REDDIT_PASSWORD'],
                             user_agent=self.USER_AGENT)
        return reddit

    def make_request(self, sub,filter):
        response = requests.get(url=f"https://www.reddit.com/r/{sub}/{filter}.json", headers={'User-Agent': self.USER_AGENT},
                                params={'limit': 20})
        data = json.loads(response.content)
        data = data['data']['children']
        body = ''
        for i in data:
            post = ''
            post += f'<div><strong>{i["data"]["author"]}</strong></p>\n'
            post += f'<p><h3>{i["data"]["title"]}</h3></p>\n'
            if i['data']['selftext']:
                 post +=  f'<p>{i["data"]["selftext"]}</p>\n'
            if 'preview' in i['data']:
                all_images = [x['source'] for x in i['data']['preview']['images']]                                
                for image in all_images:
                    post += f'<img src="{image["url"]}"  alt="Post Image">\n'
            post += f'<p>Upvotes: {i["data"]["ups"]} Comments: {i["data"]["num_comments"]}</p>'
            if i['data']['is_video']:
                post += f"<br><a class='watch-video-btn' href='https://reddit.com{i['data']['permalink']}'> Watch Video</a>"
            else:
                post += f"<br><a class='watch-video-btn' href='https://reddit.com{i['data']['permalink']}'> See on Reddit</a>"
            post += '</div>\n'
            post += "<hr>"
            body += post
        body += "<p>That concludes today's content. Join me again tomorrow for more engaging posts! Wishing you a wonderful day!</p>"

        return body    
    def generate_html(self, body):
        return f'''<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Reddit Posts</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #2c3e50;
                        color: #ecf0f1;
                        margin: 20px;
                    }}

                    div {{
                        background-color: #e9ecf0;
                        border: 1px solid #2c3e50;
                        padding: 15px;
                        margin-bottom: 20px;
                        border-radius: 10px;
                        box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
                    }}

                    img {{
                        max-width: 100%;
                        height: auto;
                        border-radius: 10px;
                        margin-top: 15px;
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                    }}

                    strong {{
                        color: #3498db;
                    }}

                    p {{
                        margin: 0;
                    }}

                    .posted-by {{
                        font-size: 14px;
                        color: #95a5a6;
                        margin-bottom: 5px;
                    }}
                     hr {{
                    width: 80%;
                    margin: 20px auto; 
                    border: 1px solid #000;
                    }}
                    .watch-video-btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: #fff;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background-color 0.3s ease;
                    }}

                    .watch-video-btn:hover {{
                        background-color: #2980b9;
                    }}
                </style>
            </head>
            <body>

            {body}
            </body>
            </html>'''


if __name__ == "__main__":
    sub = input("Subreddit: ")
    filter = input("Filter by ['Hot'/'New'/'Top']: ")
    reddit = RedditData(config_path = 'config.yaml')
    body = reddit.make_request(sub=sub,filter = filter.lower())
    html_content = reddit.generate_html(body)    
    em = EmailWithPython(config_path="config.yaml",is_html=True)
    em.send_email(rec_email='username@gmail.com',subject=f"r/{sub.title()}'s {filter.title()} Posts Today",body=html_content)
    
