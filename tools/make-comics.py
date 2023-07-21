import os
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

# What are we gonna do?
"""
2. See how many there are
3. Loop over the comics
4. Make pages for each comic
5. The first comic should not have a "first" or "previous" button
6. The last comic should not have a "next" or "last" button
"""

base_dir = "/comics/img/"

# A dict containing all html elements for the comic pages to help construct the page
html_dict = {
    "first": """<a href="[REPLACE WITH LINK]">
                    <img src="/comics/navigation/first.png" alt="First Comic" />
                </a>""",
    "previous": f"""<a href="[REPLACE WITH LINK]">
                    <img src="/comics/navigation/previous.png" alt="Previous Comic" />
                </a>""",
    "next": f"""<a href="[REPLACE WITH LINK]">
                    <img src="/comics/navigation/next.png" alt="Next Comic" />
                </a>""",
    "last": """<a href="[REPLACE WITH LINK]">
                    <img src="/comics/navigation/last.png" alt="Last Comic" />
                </a>""",
}

# A dict with the first and last comics
links_dict = {
    "first": "",
    "last": "",
}


def get_comic_data():
    """Find comic_data.json and return it as a list of dictionaries"""
    # We start in the root of the repository so we need to go to the comics directory
    comic_data_file = os.path.join("comics", "comic_data.json")
    # Open and read the file as a list of dictionary objects
    with open(comic_data_file, "r") as f:
        comic_data = json.load(f)

    return comic_data


def set_comic_links(data):
    """Update dictionaries with links to the first and last comics"""
    # The first element in the list is the first comic
    # The last element in the list is the last comic
    # (obviously)
    links_dict["first"] = "/comics/pages/comic_1.html"
    links_dict["last"] = f"/comics/pages/comic_{len(data)}.html"

    # We can update the html_dict
    html_dict["first"] = html_dict["first"].replace(
        "[REPLACE WITH LINK]", links_dict["first"]
    )
    html_dict["last"] = html_dict["last"].replace(
        "[REPLACE WITH LINK]", links_dict["last"]
    )


def parse_comics(data):
    # This will loop through the comics and create the html for each one
    first = True
    last = False
    num_comics = len(data)
    comic_num = 1

    previous_link = ""
    next_link = "/comics/pages/comic_2.html"

    for comic in data:
        # Construct the navigation buttons
        nav = ""
        if not first:
            nav += html_dict["first"]
            nav += html_dict["previous"].replace("[REPLACE WITH LINK]", previous_link)
        if not last:
            nav += html_dict["next"].replace("[REPLACE WITH LINK]", next_link)
            nav += html_dict["last"]

        # Construct the html
        # Load the boilerplate
        html = ""
        with open("tools/comicBoilerplate.html", "r") as f:
            html = f.read()

        # Replace the title
        html = html.replace("[REPLACE WITH TITLE]", comic["name"])

        # Replace date
        html = html.replace("[REPLACE WITH DATE]", comic["date"])

        # Replace image
        html = html.replace("[REPLACE WITH IMAGE]", base_dir + comic["src"])

        # Replace description
        html = html.replace("[REPLACE WITH DESCRIPTION]", comic["description"])

        # Replace navigation
        html = html.replace("[REPLACE WITH NAV]", nav)

        # Replace tooltip
        html = html.replace("[REPLACE WITH TOOLTIP]", comic["tooltip"])

        # Get the open graph info
        og = make_OG_tags(comic, comic_num)
        html = html.replace("[REPLACE WITH OG]", og)

        # Write the html to a file in the comics directory
        with open(f"comics/pages/comic_{comic_num}.html", "w") as f:
            f.write(html)

        # Update links
        previous_link = f"/comics/pages/comic_{comic_num}.html"
        next_link = f"/comics/pages/comic_{comic_num + 2}.html"

        first = False
        comic_num += 1
        if comic_num == num_comics:
            last = True

        print(
            f"Created page for comic {comic['name']}. {comic_num - 1} of {num_comics}"
        )

    # Update index.html - find the button with the content "Comics" and replace the href
    with open("index.html", "r") as f:
        index_html = f.read()

    # Match regex for the button link - it is of the form "/comics/.*", we want to capture the bit between the quotes and replace it
    regex = r'(?<=<a href=")/comics/.*(?=" class="button">)'
    replacement = links_dict["last"]

    index_html = re.sub(regex, replacement, index_html)

    # Update
    with open("index.html", "w") as f:
        f.write(index_html)
    print("Index.html updated")


def make_OG_tags(comic, comic_num):
    # Make a dictionary
    og = {
        "title": comic["name"],
        "image": f"/comics/og/comic_{comic_num}.png",
        "description": comic["description"],
        "url": f"/comics/pages/comic_{comic_num}.html",
        "type": "article",
    }

    # Make the tags
    # Copied from makeBlogs.py
    # Format: <meta property="og:KEY" content="VALUE" />
    og_tags = []
    for key, value in og.items():
        og_tags.append(f'<meta property="og:{key}" content="{value}" />')

    og_tags = "\n".join(og_tags)

    return og_tags


def make_rss_feed(data):
    max_items = 10

    base_url = "https://eatkin.neocities.org"

    # Load the rss feed components as json
    with open("tools/rss_feed_components.json", "r") as f:
        rss_components = json.load(f)

    xml = []
    xml.append(rss_components["header"])
    xml.append("<channel>")
    xml.append(
        rss_components["comic_header"].replace(
            "[LATEST_COMIC_LINK]", base_url + links_dict["last"]
        )
    )

    # Get the current feed and parse it into its component items
    with open("rss/comic_feed.xml", "r") as f:
        feed = f.read()

    soup = BeautifulSoup(feed, "xml")

    # Get all items
    items = soup.find_all("item")

    # Loop through the comics and create new items for any that are missing from the feed
    titles = [item.find("title").text for item in items]

    # Start creating the item components
    # Iterate over the comics in reverse order to start with most recent
    i = len(data)
    count = 0
    for comic in data[-max_items:][::-1]:
        # If the comic's title is the same as the latest title, we've reached the end of the feed
        if comic["name"] in titles:
            continue

        # Otherwise we can add the comic to the feed
        date_formatted = datetime.strptime(comic["date"], "%Y-%m-%d").strftime(
            "%a, %d %b %Y"
        )
        # Add the current time
        date_formatted += datetime.now().strftime(" %H:%M:%S GMT")

        xml_item = (
            rss_components["comic_item"]
            .replace("[COMIC_LINK]", base_url + f"/comics/pages/comic_{i}.html")
            .replace("[COMIC_TITLE]", comic["name"])
            .replace("[COMIC_DESCRIPTION]", comic["description"])
            .replace("[COMIC_DATE]", date_formatted)
            .replace("[COMIC_IMAGE_LINK]", base_url + base_dir + comic["src"])
        )
        xml.append(xml_item)
        i -= 1
        count += 1

    if count == 0:
        print("No new items to add to the RSS feed")
    else:
        print(f"Added {count} new items to the RSS feed")

        # Now we need to add the existing items to reach max_items
        for i in range(max_items - count):
            # Use a try except block to catch the case where there are fewer than max_items comics
            try:
                xml.append(str(items[i]))
            except:
                break

        xml.append("</channel>")
        xml.append("</rss>")
        xml = "\n".join(xml)

        # Replace last build date with current date and time
        date_formatted = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        xml = xml.replace("[LAST_BUILD_DATE]", date_formatted)

        # Write to file
        with open("rss/comic_feed.xml", "w") as f:
            f.write(xml)

        print("RSS feed created")


data = get_comic_data()
set_comic_links(data)
parse_comics(data)
make_rss_feed(data)
