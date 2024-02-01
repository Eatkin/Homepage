import os
import re
import markdown
import json
from datetime import datetime
from bs4 import BeautifulSoup
from html import unescape


def get_blogs():
    """
    This function will crawl the blog directory and return a list of dictionaries containing the following information:
    - year
    - month
    - day
    - title
    - image
    - url
    - filepath
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(script_dir, os.pardir, "txt", "blog")

    blogs_list = []

    img_pattern = re.compile(r"!\[.*\]\((.*)\)")

    # Begin crawl
    for root, dirs, files in os.walk(dir):
        if files != []:
            for file in files:
                if file.endswith(".md"):
                    # Let's get the relative url, beginning with txt/
                    relative_url = (
                        os.path.join(root, file)
                        .replace(os.path.join(script_dir, os.pardir), "")
                        .replace("\\", "/")
                    )

                    # Open up the file and read the first two lines
                    # These correspond to a date in format dd/mm/yyyy and a title
                    with open(os.path.join(root, file), "r") as f:
                        date = f.readline()
                        title = f.readline()
                        img = ""
                        for line in f:
                            match = re.match(img_pattern, line)
                            if match is not None:
                                img = match.group(1)

                    # They're formatted in markdown so remove the # and strip
                    date = date.replace("#", "").strip()
                    title = title.replace("#", "").strip()
                    blog_dict = {
                        "year": date.split("/")[2],
                        "month": date.split("/")[1],
                        "day": date.split("/")[0],
                        "title": title,
                        "image": img,
                        "url": relative_url,
                        "filepath": os.path.join(root, file),
                    }
                    blogs_list.append(blog_dict)

    # Blogs aren't sorted so let's sort them
    blogs_list = sorted(
        blogs_list,
        key=lambda k: datetime.strptime(k["year"] + k["month"] + k["day"], "%Y%m%d"),
    )

    return blogs_list


def construct_blog(blog):
    """
    This function will take a dictionary containing blog information and construct the html for the blog page
    It will then save the html file in the same directory as the blog's source markdown file
    This function will also generate the open graph tags for the blog
    """
    # Load boilerplate html
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "blogBoilerplate.html")
    ) as f:
        boilerplate = f.read()

    # Replace the title
    boilerplate = boilerplate.replace("[REPLACE-WITH-BLOG-TITLE]", blog["title"])

    # Parse the markdown
    with open(blog["filepath"]) as f:
        markdown_text = f.read()

    html = markdown.markdown(markdown_text)

    # Append a back button
    html += """<p><a href="/blog.html">&#60;- Back to blog index</a></p>"""

    # Now replace the markdown text
    boilerplate = boilerplate.replace("[REPLACE-WITH-BLOG]", html)

    # Generate the open graph tags for title, description and image
    og = {}
    og["title"] = blog["title"]
    og["image"] = blog["image"]

    # Let's read the description directly from the markdown file
    # Loop over the lines until we find the first line that doesn't start with a #
    # This should be the first paragraph
    og["description"] = ""
    max_description_length = 160  # 155-160 characters recommended
    for line in markdown_text.split("\n"):
        if not line.startswith("#") and line != "":
            og["description"] += line + " "
            if len(line) > max_description_length:
                og["description"] = og["description"][:max_description_length] + "..."
                break

    # Type is article
    og["type"] = "article"

    # Save the description into the blog dictionary
    blog["description"] = og["description"]

    # Now we can construct the open graph tags
    # Format: <meta property="og:KEY" content="VALUE" />
    og_tags = []
    for key, value in og.items():
        og_tags.append(f'<meta property="og:{key}" content="{value}" />')

    og_tags = "\n".join(og_tags)

    # Now replace the og tags in the boilerplate
    boilerplate = boilerplate.replace("[REPLACE-WITH-OG-TAGS]", og_tags)

    # Because the site updater detects changes we should compare the new html with the old html
    if not os.path.exists(blog["filepath"].replace(".md", ".html")):
        # Create the file
        f = open(blog["filepath"].replace(".md", ".html"), "w")
        # Close the file
        f.close()

    with open(blog["filepath"].replace(".md", ".html"), "r") as f:
        old_html = f.read()

    if old_html != boilerplate:
        # Save the boilerplate as .html
        with open(blog["filepath"].replace(".md", ".html"), "w") as f:
            f.write(boilerplate)

        print(f"Generated blog: {blog['title']}")
    else:
        print(f"Blog {blog['title']} already up to date")


def construct_blog_index(blogs_list):
    """
    This function will take a list of dictionaries containing blog information and construct the html for the blog index page
    It will then save the html file in the same directory as the blog's source markdown file
    It organises blogs in reverse chronological order and groups them by year
    """
    # Sort the blogs_list by year, month, then day
    blogs_list = sorted(
        blogs_list, key=lambda k: (k["year"], k["month"], k["day"]), reverse=True
    )

    html = ""
    currentYear = 0

    for blog in blogs_list:
        print(f"Adding blog {blog['title']} to blog index")
        print(f"Year: {blog['year']}, Month: {blog['month']}, Day: {blog['day']}")
        # If the year changes, add a new year heading and open an undered list
        if blog["year"] != currentYear:
            # Close the unordered list
            if currentYear != 0:
                html += "</ul>"

            currentYear = blog["year"]
            html += f"""<div class="year-box">
                            <h2>{currentYear}</h2>
                    </div>"""

            # Open the unordered list
            html += '<ul class="post-list">'

        # Add the blog to the list
        html += f"""<li><a href=".{blog["url"].replace('.md', '.html')}" class="txt-link">{blog["day"]}/{blog["month"]}/{blog["year"]} - {blog["title"]}</a>
            </li>"""

    # Close the unordered list
    html += "</ul>"

    # Append a back home link
    html += """<p><a href="/index.html">&#60;- Back to home</a></p>"""

    # Now we need to insert the html into the blog-container div
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "blogIndexBoilerplate.html"
        )
    ) as f:
        boilerplate = f.read()

    boilerplate = boilerplate.replace("[REPLACE-WITH-BLOG-INDEX]", html)

    # Now go up one working directory and save the file as blog.html
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(script_dir, os.pardir)

    with open(os.path.join(dir, "blog.html"), "w") as f:
        f.write(boilerplate)

    print("Generated blog index")


def make_rss_feed(blogs_list):
    max_items = 10

    base_url = "https://eatkin.neocities.org"

    # Load the rss feed components as json
    with open("tools/rss_feed_components.json", "r") as f:
        rss_components = json.load(f)

    # Get the current feed and parse it into its component items
    with open("rss/blog_feed.xml", "r") as f:
        feed = f.read()

    soup = BeautifulSoup(feed, "xml")

    # Get all items
    items = soup.find_all("item")

    # Loop through the blogs and create new items for any that are missing from the feed
    # Get all titles already in the feed
    titles = [item.find("title").text for item in items]

    xml = []
    xml.append(rss_components["header"])
    xml.append("<channel>")
    xml.append(rss_components["blog_header"])

    i = len(blogs_list)
    # Blogs are sorted in reverse chronological order so we need to flip the list
    blogs_list = blogs_list[::-1]
    count = 0
    for blog in blogs_list[:max_items]:
        # If the blog is already in the feed, we've reached the end of the new blogs, so break
        if blog["title"] in titles:
            continue

        date = blog["year"] + "-" + blog["month"] + "-" + blog["day"]
        date_formatted = datetime.strptime(date, "%Y-%m-%d").strftime("%a, %d %b %Y")
        # Add the current time
        date_formatted += datetime.now().strftime(" %H:%M:%S GMT")

        # If count is 0, this is the first item, so we'll update lastBuildDate here
        if count == 0:
            xml[0] = xml[0].replace("[LAST_BUILD_DATE]", date_formatted)

        xml_item = (
            rss_components["blog_item"]
            .replace("[BLOG_TITLE]", blog["title"])
            .replace("[BLOG_LINK]", base_url + blog["url"].replace(".md", ".html"))
            .replace("[BLOG_DATE]", date_formatted)
        )

        # I am going to make this XML feed compatible with feed readers
        # Thus I need to replace [BLOG] with the relevant cdata
        # Like this: <![CDATA[Insert blog here]]>
        # Use BeautifulSoup to parse the blog html to get the html between the 'markdown' div
        blog_html = ""
        with open(blog["filepath"].replace(".md", ".html"), "r") as f:
            blog_html = f.read()

        soup = BeautifulSoup(blog_html, "html.parser")
        blog_html = soup.find("div", {"id": "markdown"}).decode_contents()

        # Drop the final <p> tag because it's just a back button
        final_p = soup.find_all("p")[-1]

        blog_html = blog_html.replace(str(final_p), "")

        # Now put it into the cdata format
        blog_html = "<![CDATA[" + blog_html + "]]>"

        # And add it into the xml item
        xml_item = xml_item.replace("[BLOG]", blog_html)

        xml.append(xml_item)
        i -= 1
        count += 1

    if count == 0:
        print("No new blogs to add to RSS feed")
    else:
        print(f"Added {count} new blogs to the RSS feed")

        # Now we need to add the existing items to reach max_items
        for i in range(max_items - count):
            # Use a try except block to catch the case where there are fewer than max_items comics
            try:
                # We need to clean up because the xml parser escapes the html and fucks everything up
                item = items[i]
                pre = "<![CDATA["
                post = "]]>"

                # Get the description text
                description = item.find("description").text

                description = pre + description + post

                # Now put the description back into the item
                item.find("description").string = description
                # Convert to string
                item = str(item)
                item = unescape(item)
                xml.append(item)
            except:
                break

        # Finish the xml
        xml.append("</channel>")
        xml.append("</rss>")
        xml = "\n".join(xml)

        # Replace last build date with current date and time
        date_formatted = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        xml = xml.replace("[LAST_BUILD_DATE]", date_formatted)

        # Write to file
        with open("rss/blog_feed.xml", "w") as f:
            f.write(xml)

        print("RSS feed created")


blog_information = get_blogs()
print(f"Found {len(blog_information)} blogs")

for blog in blog_information:
    construct_blog(blog)

construct_blog_index(blog_information)

make_rss_feed(blog_information)

print("Finished generating blogs")
