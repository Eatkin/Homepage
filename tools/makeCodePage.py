import os
import json


def get_code_info():
    """
    This will load code.json and return a list of dictionaries containing the following information:
    -Title
    -Description
    -Link
    -Tags
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    _json = json.load(open(os.path.join(script_dir, "code.json"), "r"))
    info = []
    for item in _json:
        code_dict = {}
        code_dict["title"] = item["title"]
        code_dict["description"] = item["description"]
        code_dict["link"] = item["link"]
        code_dict["tags"] = item["tags"]
        info.append(code_dict)

    return info


def construct_code_page(info):
    """
    This function will take a list of dictionaries containing code information and construct the html for the code page
    Format:
    <div class="tag-tag1 tag-tag2 hideable">
        <div class="text-container">
            <h2>Title</h2>
            <p>Description.</p>
            <div>
                <a href="Link" class="code-button"
                    target="_blank">View</a>
            </div>
            <p><b>Tags:</b> tag1, tag2, tag3</p>
        </div>
    </div>

    The function will also generate a stylesheet for use with the page
    """
    html = ""
    nav = ""
    style = ""
    style_append = ""
    all_tags = set()

    # This generate the html for the main page
    for item in info:
        tag_classes = " ".join(["tag-" + tag for tag in item["tags"]]) + " hideable"
        title = item["title"]
        description = item["description"]
        url = item["link"]
        tags = ", ".join(item["tags"])
        html += f"""<div class="{tag_classes}">
            <div class="grid-item text-container">
                <h2><a href="{url}" class="code-link">{title}</a></h2>
                <p>{description}</p>
                <p><b>Tags:</b> {tags}</p>
            </div>
        </div>
        """
        # Append the tags to the set
        for tag in item["tags"]:
            all_tags.add("tag-" + tag)

        print("Added " + title)

    # Sort tags
    all_tags = sorted(all_tags)

    # Generate style sheet
    for tag in all_tags:
        # Style first
        style += f"""div.{tag} {{
            display: none;
        }}
        #{tag}-check:checked~main section .grid-container div.{tag} {{
            display: flex;
        }}
        input#{tag}-check {{
            display: none;
        }}
        """

        # The navigation bar
        nav += f"""<input type="checkbox" id="{tag}-check"><label for="{tag}-check" class="filter-label">{tag[4:]}</label>
        """

        # Additional style for the end
        style_append += f"#{tag}-check:not(:checked)~"

    # Add the last bit to style_append to make it work
    style_append += "main section .grid-container div.hideable {display: flex;}"

    print("Generated style sheet")

    # Now load the boilerplate
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "codeBoilerplate.html"), "r") as f:
        boilerplate = f.read()

    boilerplate = boilerplate.replace("(INSERT TAGS FILTER HERE)", nav).replace(
        "(INSERT GRID HERE)", html
    )

    # Now write the html
    destination = os.path.join(script_dir, os.pardir, "code.html")
    with open(destination, "w") as f:
        f.write(boilerplate)

    # Now write the stylesheet
    destination = os.path.join(script_dir, os.pardir, "code.css")
    with open(destination, "w") as f:
        f.write(style + style_append)


info = get_code_info()
construct_code_page(info)
