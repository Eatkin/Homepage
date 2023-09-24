import json
import pyperclip
import os

# get the absolute path to the current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# construct the path to games.json relative to the current directory
games_path = os.path.join(dir_path, "games.json")

with open(games_path, "r") as f:
    data = json.load(f)

# Firstly we'll generate the table content and save all the tags

html_output = ""
tags = set()

for game in data:
    tag_classes = " ".join([f"tag-{tag}" for tag in game["tags"]])
    html_output += f'<div class="' + tag_classes + ' hideable">\n'
    html_output += '    <div class="grid-item image-container">\n'
    html_output += f"        <img src=\"images/games/{game['img']}\" alt=\"{game['gameTitle']} Title Card\">\n"
    html_output += "    </div>\n"
    html_output += '    <div class="grid-item text-container">\n'
    html_output += f"        <h2>{game['gameTitle']}</h2>\n"
    html_output += f"        <h3>{game['shortDesc']}</h3>\n"
    html_output += f"        {game['longDesc']}\n"
    html_output += f"        <a href=\"{game['link']}\" class=\"game-button\" target=\"_blank\">Play {game['gameTitle']}</a>\n"
    html_output += "        <p><b>Tags:</b> "
    html_output += ", ".join(game["tags"])
    html_output += "</p>\n"
    html_output += "    </div>\n"
    html_output += "</div>\n"
    for tag in game["tags"]:
        tags.add(f"tag-{tag}")

# Sort tags to alphabetical
tags = sorted(tags)

# Now we can iterate through the set of tags to generate style
# Here we also generate the unordered list which we can style
style = ""
nav = ""
styleAppend = ""
for tag in tags:
    # Style first
    style += f"div.{tag} {{\n"
    style += "display: none;\n"
    style += "}\n\n"
    style += f"#{tag}-check:checked~main section .grid-container div.{tag} {{\n"
    style += "display: flex;\n"
    style += "}\n\n"
    style += f"input#{tag}-check {{\n"
    style += "display: none;\n"
    style += "}\n\n"
    # Now the list
    nav += (
        f'<input type="checkbox" id="{tag}-check"><label for="{tag}-check" class="filter-label">'
        + f"{tag[4:]}"
        + f"</label>\n"
    )
    styleAppend += f"#{tag}-check:not(:checked)~"

# Finally we need one selector that makes sure anything tagged with "hideable" is not hidden if nothing is checked
# So let's get that updated

styleAppend = styleAppend[:-1]
styleAppend += "~main section .grid-container div.hideable {\ndisplay:flex;\n}"

# Additional styling of labels


style += styleAppend

# Start putting together the html page
htmlPage = '<!DOCTYPE html>\n<html lang="en">\n\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n'
htmlPage += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<link rel="stylesheet" href="style.css?v=3.0">\n'
htmlPage += '<link rel="stylesheet" type="text/css" href="gamesFilter.css?v=3.0">\n<link rel="preconnect" href="https://fonts.googleapis.com">\n'
htmlPage += '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=IM+Fell+DW+Pica&display=swap" rel="stylesheet">\n'
htmlPage += "<title>The Edspace</title>\n</head>\n\n"

# Header
htmlPage += "<body>\n<header>\n<h1>Games</h1>\n<p>Here you can find all the games I've made in recent years.</p>\n"
htmlPage += "<p>I have a long history of making games with Gamemaker, starting in around 2003. After a very long break I took up the hobby again in 2018. Since then, I've made many games in a variety of genres, styles and qualities.</p>\n"
htmlPage += "<p>Filter by <i>best-of</i> for the good stuff.</p>\n</header>"
htmlPage += '<div id="games-container">\n'

# Add all the checkboxes here
htmlPage += nav
# Now set up the table
htmlPage += '<main>\n<section id="games">\n<div class="grid-container">\n'
# We can insert all the rows that we've generated now
htmlPage += html_output
# Now close off the table
htmlPage += "\n</div>\n</section>\n"

# Info for nerds
htmlPage += "<section>\n<p>Page info for nerds: This page is generated from .json using a Python script.</p>\n"
htmlPage += '<p>The filtering is done with absolutely no javascript. CSS only. If you want an idea of what absolute sins against programming I had to do to accomplish this, check out <a href="gamesFilter.css">gamesFilter.css</a>.</p>\n'
htmlPage += "<p>You might see why I got a script to generate the page and stylesheet for me.</p>\n</section>\n"

htmlPage += "</main>\n</div>\n\n"
# Add the footer
htmlPage += "<footer>\n"
htmlPage += '<p>Copyright &copy; <span id="year">2023</span> Edward Atkin</p>\n\n'
# Script for updating the year automatically
htmlPage += '<script>\ndocument.getElementById("year").innerHTML = new Date().getFullYear();\n</script>'
# Close off the footer and the document
htmlPage += "</footer>\n\n</body>\n\n</html>"

print("HTML page copied to clipboard")
pyperclip.copy(htmlPage)

input("Press enter and we'll copy the style sheet to your clipboard too")
print("Style copied")
pyperclip.copy(style)
