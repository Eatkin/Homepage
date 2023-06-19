import os
import re
import markdown


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
    html += """<p><a href="/blog.html"><- Back to blog index</a></p>"""

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

    # Now we can construct the open graph tags
    # Format: <meta property="og:KEY" content="VALUE" />
    og_tags = []
    for key, value in og.items():
        og_tags.append(f'<meta property="og:{key}" content="{value}" />')

    og_tags = "\n".join(og_tags)

    # Now replace the og tags in the boilerplate
    boilerplate = boilerplate.replace("[REPLACE-WITH-OG-TAGS]", og_tags)

    # Save the boilerplate as .html
    with open(blog["filepath"].replace(".md", ".html"), "w") as f:
        f.write(boilerplate)

    print(f"Generated blog: {blog['title']}")


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
        html += f"""<li><a href=".{blog["url"].replace('.md', '.html')}" class="txt-link">{blog["day"]}/{blog["month"]}/{blog["year"]} - {blog["title"]}</a>
            </li>"""

    # Close the unordered list
    html += "</ul>"

    # Append a back home link
    html += """<p><a href="/index.html"><- Back to home</a></p>"""

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


blog_information = get_blogs()
print(f"Found {len(blog_information)} blogs")

for blog in blog_information:
    construct_blog(blog)

construct_blog_index(blog_information)

print("Finished generating blogs")
