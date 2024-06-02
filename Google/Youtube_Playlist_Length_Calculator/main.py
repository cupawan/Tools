import requests
import json
import os
from datetime import timedelta
import isodate
import pandas as pd
from tabulate import tabulate

class YoutubeData:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_playlist_duration(self, playlist_link):
        playlist_id = playlist_link.split("=")[-1]
        api_playlist_url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&fields=items/contentDetails/videoId,nextPageToken&key={}&playlistId={}&pageToken='.format(self.api_key, playlist_id)
        video_url = 'https://www.googleapis.com/youtube/v3/videos?&part=contentDetails&key={}&id={}&fields=items/contentDetails/duration'.format(self.api_key, '{}')
        next_page = ''
        total_videos = 0
        total_duration = timedelta(0)
        df = pd.DataFrame()
        df["Property"] = ['Number of videos','Average length of video','Total length of playlist','At 1.25x','At 1.50x','At 1.75x','At 2.00x']
        while True:
            video_ids = []
            results = json.loads(requests.get(api_playlist_url + next_page).text)
            for item in results.get('items', []):
                video_ids.append(item['contentDetails']['videoId'])
            video_ids_str = ','.join(video_ids)
            total_videos += len(video_ids)
            video_details = json.loads(requests.get(video_url.format(video_ids_str)).text)
            for video in video_details.get('items', []):
                total_duration += isodate.parse_duration(video['contentDetails']['duration'])
            if 'nextPageToken' in results:
                next_page = results['nextPageToken']
            else:
                values = [total_videos,total_duration / total_videos,total_duration,total_duration / 1.25,total_duration / 1.5,total_duration / 1.75,total_duration / 2]
                df['Value'] = values
                print(tabulate(df,tablefmt = 'fancy_grid',showindex=False))
                break

if __name__ == "__main__":
    youtube_playlist_url = input("Enter youtube URL: ")
    api_key = os.environ.get("GOOGLE_API_KEY")
    object = YoutubeData(api_key=api_key)
    object.get_playlist_duration(playlist_link=youtube_playlist_url)