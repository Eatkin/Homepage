import json
import requests
import pyperclip

# Get api key and channel id via command line input
api_key = input("Enter your YouTube API key: ")
channel_id = input("Enter the YouTube channel ID: ")
depth = 3   # Number of videos to retrieve


# Set up the URL and parameters for the API request
url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults={depth}&type=video"

html_string = ""

# Make the API request and store the response in a variable
response = requests.get(url)

# Check the status code to ensure the request was successful
if response.status_code == 200:
    # Extract the channel data from the response
    channel_data = response.json()['items']
else:
    # Handle the error case
    print('Error making API request: ', response.status_code)
    # End program
    exit()

# Loop through the channel data and format as HTML
for video in channel_data:
    video_id = video['id']['videoId']
    video_title = video['snippet']['title']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    video_thumbnail = video['snippet']['thumbnails']['high']['url']
    video_description = video['snippet']['description']
    '''Format:
    <div class="video-container">
            <a href="https://www.youtube.com/watch?v=p01V4u8AXK0" target="_blank">
                <img src="images/video-thumbnails/kimkubus.png" alt="Video Thumbnail">
            </a>
            <div class="video-info">
                <h2><a href="https://www.youtube.com/watch?v=p01V4u8AXK0" target="_blank">In the Mind of Kimberly Kubus:
                        The Game Developer Who Saw God</a></h2>
                <p>In this video, I delve into the fascinating
                    world of
                    game developer Kimberly Kubus and explore his work.</p>
            </div>
        </div>'''
    html_string += "<div class=\"video-container\">\n"
    html_string += f"\t<a href=\"{video_url}\" target=\"_blank\">\n"
    html_string += f"\t\t<img src=\"{video_thumbnail}\" alt=\"{video_title} thumbnail\">\n"
    html_string += "\t</a>\n"
    html_string += "\t<div class=\"video-info\">\n"
    html_string += f"\t\t<h2><a href=\"{video_url}\" target=\"_blank\">{video_title}</a></h2>\n"
    html_string += f"\t\t<p>{video_description}</p>\n"
    html_string += "\t</div>\n"
    html_string += "</div>\n"

# Copy the HTML to the clipboard
pyperclip.copy(html_string)
print("HTML copied to clipboard")
