# Homepage

## About

This is the Github repo containing the source for my personal website, including all tools I use to build it.

This website is a place for me to host my projects and things I've worked on in one place.

The website is pure HTML and CSS with no reliance on Javascript, but still has features such as [filtering by tags](https://eatkin.neocities.org/code) and [theme switching](https://eatkin.neocities.org/about).

## Viewing the Website

The website is hosted on Neocities:

* [Neocities](https://eatkin.neocities.org)

## Contents

The website is my place to show all my projects and things I've worked on in one place, and is ever growing in content.

So far it has:
* [A short about me page](https://eatkin.neocities.org/about)
* [All the games I've made](https://eatkin.neocities.org/games)
* [Coding projects I've worked on](https://eatkin.neocities.org/code)
* [Videos I've worked on](https://eatkin.neocities.org/videos)
* [A (mostly) lighthearted blog where I talk about nothing inparticular](https://eatkin.neocities.org/blog)
* [An extremely ironic web comic](https://eatkin.neocities.org/comics_index)

## Tools

Neocities only hosts static website and has a very minimal interface, so I have built my own basic content management system. Here's a list of tools I use:
- [constructTableFromJson.py](https://github.com/Eatkin/Homepage/blob/master/tools/constructTableFromJson.py) - creates the Games page and associated stylesheet by parsing json
- [makeVideosPage.py](https://github.com/Eatkin/Homepage/blob/master/tools/makeVideosPage.py) - constructs the video pages by querying the Youtube API
- [make-comics.py](https://github.com/Eatkin/Homepage/blob/master/tools/make-comics.py) - constructs the comic index, generates pages and updates button links for the comics. Updates associated RSS feed
- [makeBlogs.py](https://github.com/Eatkin/Homepage/blob/master/tools/makeBlogs.py) - creates blog pages by parsing markdown and updates blog index. Updates associated RSS feed
- [makeCodePage.py](https://github.com/Eatkin/Homepage/blob/master/tools/makeCodePage.py) - creates the code page and associated stylesheet by parsing json
- [updateSite.py](https://github.com/Eatkin/Homepage/blob/master/tools/SiteUpdater/updateSite.py) - file tracking system to automate uploading of files to Neocities via the API as required
