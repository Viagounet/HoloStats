import dateutil
import requests

from utility import yt_duration_to_datetime


def return_video_ids(playlist_id):
    ids = []

    response = requests.get(
        f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&key=AIzaSyAACDpViFfwP8tXHnnw6BSNM04VpDMb05Y")
    response_json = response.json()
    ids += [item['snippet']['resourceId']['videoId'] for item in response_json['items']]
    next_page_token = response_json.get("nextPageToken")

    n_pages = response_json.get("pageInfo").get("totalResults") // 50
    for i in range(n_pages):
        response = requests.get(
            f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&key=AIzaSyAACDpViFfwP8tXHnnw6BSNM04VpDMb05Y&pageToken={next_page_token}")
        response_json = response.json()
        ids += [item['snippet']['resourceId']['videoId'] for item in response_json['items']]
        next_page_token = response_json.get("nextPageToken")

    return ids


def get_video_details(video_id):
    URL = "https://www.googleapis.com/youtube/v3/videos?part="
    API_KEY = "YOUR_API_KEY"
    content_details = requests.get(f"{URL}contentDetails&id={video_id}&key={API_KEY}").json()['items'][0][
        'contentDetails']
    statistics = requests.get(f"{URL}statistics&id={video_id}&key={API_KEY}").json()['items'][0]['statistics']
    snippet = requests.get(f"{URL}snippet&id={video_id}&key={API_KEY}").json()['items'][0]['snippet']

    live_streaming_details = requests.get(f"{URL}liveStreamingDetails&id={video_id}&key={API_KEY}").json()['items'][0][
        'liveStreamingDetails']
    infos = {"views": int(statistics['viewCount']),
             "like_count": int(statistics['likeCount']),
             "comment_count": int(statistics['commentCount']),
             "actual_start_time": dateutil.parser.isoparse(live_streaming_details['actualStartTime']),
             "scheduled_start_time": dateutil.parser.isoparse(live_streaming_details['scheduledStartTime']),
             "actual_end_time": dateutil.parser.isoparse(live_streaming_details['actualEndTime']),
             "duration": yt_duration_to_datetime(content_details['duration']),
             "description": snippet['description'],
             "thumbnail": snippet['thumbnails']['high']['url'],
             "title": snippet['title']
             }
    infos["start_delay"] = infos["actual_start_time"] - infos["scheduled_start_time"]
    infos["percent_like"] = round(100 * infos["like_count"] / infos["views"], 2)
    infos["percent_comment"] = round(100 * infos["comment_count"] / infos["views"], 2)

    return infos