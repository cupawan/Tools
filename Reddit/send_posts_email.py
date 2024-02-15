from Reddit.main import RedditData
from Social.SendEmail import SendEmail




if __name__ == "__main__":
    sub = input("Subreddit: ")
    filter = input("Filter by ['Hot'/'New'/'Top']: ")
    reddit = RedditData(config_path = 'config.yaml')
    body = reddit.make_request(sub=sub,filter = filter.lower())
    html_content = reddit.generate_html(body)    
    em = SendEmail(config_file_path="config.yaml",is_html=True)
    em.send_email(rec_email='username@gmail.com',subject=f"r/{sub.title()}'s {filter.title()} Posts Today",body=html_content)
    