# I haven't written this yet but here's the outline:
"""
Now we need to construct the blog page itself
It will be a dictionary of dictionaries
It needs to contain the year, the date, the name and the url of the blog
For each dictionary we need to iterate over them to determine the order that they will be placed on the page
We can take the dates from the dictionary and insert them into a list, sort the list from latest to earliest
We can then make one final dictionary that has years as the keys, and dictionaries containing the link text and URL to the blog
We can then iterate over that dictionary and construct the html for the blog page
This will then be inserted into boilerplate html that we have stored for the blog page
Done!
Should be fun
"""
import os
import re
import markdown


def get_blogs():
    # First start the crawl - go up one directory then open the blog folder
    # We will then crawl through the blog folder and find all the .md files
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

    return blogs_list


def construct_blog(blog):
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

    # Now replace the markdown text
    boilerplate = boilerplate.replace("[REPLACE-WITH-BLOG]", html)

    # Save the boilerplate as .html
    with open(blog["filepath"].replace(".md", ".html"), "w") as f:
        f.write(boilerplate)

    # Don't forget the open graph tags!!!


def construct_blog_index(blogs_list):
    # We can then iterate over the sorted dictionary and construct the html for the blog page as follows:
    # For every change in year we add a year heading followed by and opening unordered list
    # For every blog we add a list item containing the date and title of the blog
    # At change of year we close the unordered list
    # After looping through the dictionary we close the unordered list because otherwise it will be left open
    # We'll have some boilerplate html and can insert it into the blog-container div

    # Sort the blogs_list by year, month, then day
    blogs_list = sorted(
        blogs_list, key=lambda k: (k["year"], k["month"], k["day"]), reverse=True
    )

    html = ""
    currentYear = 0

    for blog in blogs_list:
        # If the year changes, add a new year heading and open an undered list
        if blog["year"] != currentYear:
            # Close the unordered list
            if currentYear != 0:
                html += "</ul>"

            currentYear = blog["year"]
            html += """<div class="year-box">
                            <h2>2023</h2>
                    </div>"""

            # Open the unordered list
            html += '<ul class="post-list">'

        # Add the blog to the list
        html += f"""<li><a href="{blog["url"].replace('.md', '.html')}" class="txt-link">{blog["day"]}/{blog["month"]}/{blog["year"]} - {blog["title"]}</a>
            </li>"""

    # Close the unordered list
    html += "</ul>"

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


blog_information = get_blogs()
for blog in blog_information:
    construct_blog(blog)

construct_blog_index(blog_information)
