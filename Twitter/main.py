import tweepy
import yaml

class TwitterCreateTweet:
    def __init__(self,config_file_path):
        self.config_file_path = config_file_path
        self.config = self.load_config()
    
    def load_config(self):
        try:
            with open(self.config_file_path,'r') as f:
                config = yaml.safe_load(f)
                return config
        except Exception as e:
            d = {}
            return d
    def post_tweet(self,text,media_paths = None):
        client = tweepy.Client(
            consumer_key=self.config["TWITTER_CONSUMER_KEY"],
            consumer_secret=self.config["TWITTER_CONSUMER_SECRET"],
            access_token=self.config["TWITTER_ACCESS_TOKEN"],
            access_token_secret=self.config["TWITTER_ACCESS_TOKEN_SECRET"])
        auth = tweepy.OAuth1UserHandler(self.config["TWITTER_CONSUMER_KEY"], self.config["TWITTER_CONSUMER_SECRET"])
        auth.set_access_token(self.config["TWITTER_ACCESS_TOKEN"], self.config["TWITTER_ACCESS_TOKEN_SECRET"])
        c = tweepy.API(auth)
        media_ids = [c.media_upload(media_path).media_id for media_path in media_paths] if media_paths else None
        response = client.create_tweet(text = text, media_ids = media_ids)
        if len(response.errors) == 0:
            print("Tweet Posted Successfully")
            return response
        else:
            print("Not Posted, Errors: ", response.errors)
            return None
    

if __name__ == "__main__":
    twitter_instance = TwitterCreateTweet(config_file_path="tools_config.yaml")
    twitter_instance.post_tweet("Hello Twitter")
        