import os
import json
import re

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

        if last:
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


data = get_comic_data()
set_comic_links(data)
parse_comics(data)
