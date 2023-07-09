import requests

# Get api key and channel id via command line input
api_key = input("Enter your YouTube API key: ")
channel_id = "UCSdC_KL-it-m3Z-CK9VUUrg"
depth = 3  # Number of videos to retrieve


# Set up the URL and parameters for the API request
url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults={depth}&type=video"

html_string = ""

# Make the API request and store the response in a variable
response = requests.get(url)

# Check the status code to ensure the request was successful
if response.status_code == 200:
    # Extract the channel data from the response
    channel_data = response.json()["items"]
    print("Got channel data")
else:
    # Handle the error case
    print("Error making API request for videos:", response.status_code)
    # End program
    exit()

# API request to get playlists
url = f"https://youtube.googleapis.com/youtube/v3/playlists?part=snippet,id&channelId={channel_id}&maxResults=50&key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    # Get playlist data
    playlist_data = response.json()["items"]
    print("Got playlist data")
else:
    # Failed
    print("Error making API request for playlists:", response.status_code)
    # End program
    exit()


# Loop through the channel data and format as HTML
for video in channel_data:
    video_id = video["id"]["videoId"]
    video_title = video["snippet"]["title"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    video_thumbnail = video["snippet"]["thumbnails"]["high"]["url"]
    video_description = video["snippet"]["description"]
    """Format:
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
        </div>"""
    html_string += '<div class="video-container">\n'
    html_string += f'\t<a href="{video_url}" target="_blank">\n'
    html_string += f'\t\t<img class="video-thumbnail" src="{video_thumbnail}" alt="{video_title} thumbnail">\n'
    html_string += "\t</a>\n"
    html_string += '\t<div class="video-info">\n'
    html_string += (
        f'\t\t<h2><a href="{video_url}" target="_blank">{video_title}</a></h2>\n'
    )
    html_string += f"\t\t<p>{video_description}</p>\n"
    html_string += "\t</div>\n"
    html_string += "</div>\n"
    print("Parsed video:", video_title)

# Add a h2 tag for the playlists
html_string += "<h2>Playlists</h2>\n"

# We can copy the format above for the playlists
for playlist in playlist_data:
    playlist_id = playlist["id"]
    playlist_title = playlist["snippet"]["title"]
    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
    # Maxres is sometimes available, fall back to high if not
    try:
        playlist_thumbnail = playlist["snippet"]["thumbnails"]["maxres"]["url"]
    except:
        playlist_thumbnail = playlist["snippet"]["thumbnails"]["high"]["url"]
    playlist_description = playlist["snippet"]["description"]
    """Format:
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
        </div>"""
    html_string += '<div class="video-container">\n'
    html_string += f'\t<a href="{playlist_url}" target="_blank">\n'
    html_string += f'\t\t<img class="playlist-thumbnail" src="{playlist_thumbnail}" alt="{playlist_title} thumbnail">\n'
    html_string += "\t</a>\n"
    html_string += '\t<div class="video-info">\n'
    html_string += (
        f'\t\t<h2><a href="{playlist_url}" target="_blank">{playlist_title}</a></h2>\n'
    )
    html_string += f"\t\t<p>{playlist_description}</p>\n"
    html_string += "\t</div>\n"
    html_string += "</div>\n"
    print("Parsed playlist:", playlist_title)

# Load the boilerplate
with open("tools/videosBoilerplate.html", "r") as f:
    boilerplate = f.read()

# Replace the placeholder with the HTML string
boilerplate = boilerplate.replace("[REPLACE WITH HTML CONTENT]", html_string)

# Now save it to a file
with open("videos.html", "w") as f:
    f.write(boilerplate)

print("Done!")
