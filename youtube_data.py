import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")
api_key = os.getenv("youtube_api_key")
channel_handle = "MrBeast"
max_results = 60
channel_url = "https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={0}&key={1}"
playlist_items_url = "https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={0}&playlistId={1}&key={2}"


def get_playlist_id(channel_handle, api_key):
    try:
        channel_content = requests.get(channel_url.format(channel_handle, api_key))
        channel_content.raise_for_status()
        channel_content_json = channel_content.json()
        channel_items = channel_content_json["items"][0]
        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        raise e
    

def get_video_ids(playlist_id, max_results, api_key):
    try:
        page_token = None
        videos = []        
        url = playlist_items_url.format(max_results, playlist_id, api_key)
        while True:
            if page_token:
                url += "&pageToken={0}".format(page_token)
            playlist_content = requests.get(url)
            playlist_content.raise_for_status()
            playlist_content_json = playlist_content.json()
            playlist_items = playlist_content_json["items"]
            for item in playlist_items:
                video_id = item["contentDetails"]["videoId"]
                videos.append(video_id)
            page_token = playlist_content_json.get("nextPageToken")
            if not page_token:
                break
        return videos
    except requests.exceptions.RequestException as e:
        raise e


def main():
    channel_playlist_id = get_playlist_id(channel_handle, api_key)
    videos = get_video_ids(channel_playlist_id, max_results, api_key)
    # print(len(videos))
    print(videos)


if __name__ == "__main__":
    main()
