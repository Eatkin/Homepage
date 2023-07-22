from bs4 import BeautifulSoup
from datetime import datetime
from html import unescape

# Parsing RSS feeds leads to HTML escape characters in the text
# I'm going to try stop that happening in this environment


# Get the current feed and parse it into its component items
with open("rss/comic_feed.xml", "r") as f:
    feed = f.read()

soup = BeautifulSoup(feed, "xml")

# Get all items
items = soup.find_all("item")

for item in items:
    # We have to clean the text up
    pre = "<![CDATA["
    post = "]]>"
    # Get the description string so it's unescaped
    description = item.find("description").text
    # Add pre and post tags back in
    description = pre + description + post

    # Now we can put the description back into the item
    item.find("description").string = description
    # Convert item to a string
    item = str(item)
    item = unescape(item)
    print(item)

    # Well that was fucking annoying
