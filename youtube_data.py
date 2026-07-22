import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")
api_key = os.getenv("youtube_api_key")
# channel_id = "UCX6OQ3DkcsbYNE6H8uQQuVA"
channel_handle = "MrBeast"
channel_url = "https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={0}&key={1}"


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


def main():
    channel_playlist_id = get_playlist_id(channel_handle, api_key)
    # print(json.dumps(channel_playlists_id, indent=4))
    print(channel_playlist_id)


if __name__ == "__main__":
    main()
