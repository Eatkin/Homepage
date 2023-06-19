# Homepage

## About

This is the Github repo containing the source for my personal website, including all tools I use to build it.

This website is a place for me to host my projects and things I've worked on in one place.

The website is pure HTMl and CSS with absolutely no reliance on Javascript, but still has features such as [filtering by tags](https://eatkin.neocities.org/code) and [theme switching](https://eatkin.neocities.org/about).

## Viewing the Website

The website is hosted on Neocities:

* [Neocities](https://eatkin.neocities.org)
* [Direct URL alternative](https://www.edwardatkin.co.uk)

## Contents

The website is my place to show all my projects and things I've worked on in one place, and is ever growing in content.

So far it has:
* [A short about me page](https://eatkin.neocities.org/about)
* [All the games I've made](https://eatkin.neocities.org/games)
* [Coding projects I've worked on](https://eatkin.neocities.org/code)
* [Videos I've worked on](https://eatkin.neocities.org/videos)
* [A (mostly) lighthearted blog where I talk about nothing inparticular](https://eatkin.neocities.org/blog)

## Tools

Neocities only hosts static website, so I use Python scripts to dynamically generate HTML and CSS for pages.

The no-javascript filtering is very tedious to write by hand, featuring absolutely absurd CSS such as:  

```
#tag-algorithms-check:not(:checked)~#tag-backtracking-check:not(:checked)~#tag-beautiful-soup-check:not(:checked)~#tag-brainfuck-check:not(:checked)~#tag-browser-extension-check:not(:checked)~#tag-c-check:not(:checked)~#tag-c-sharp-check:not(:checked)~#tag-certificate-check:not(:checked)~#tag-codepen-check:not(:checked)~#tag-codewars-check:not(:checked)~#tag-command-line-check:not(:checked)~#tag-css-check:not(:checked)~#tag-data-check:not(:checked)~#tag-data-structures-check:not(:checked)~#tag-esoteric-programming-check:not(:checked)~#tag-frontend-check:not(:checked)~#tag-fun-check:not(:checked)~#tag-game-dev-check:not(:checked)~#tag-gist-check:not(:checked)~#tag-git-check:not(:checked)~#tag-hello-world-check:not(:checked)~#tag-html-check:not(:checked)~#tag-javascript-check:not(:checked)~#tag-mathematics-check:not(:checked)~#tag-oop-check:not(:checked)~#tag-powershell-check:not(:checked)~#tag-prolog-check:not(:checked)~#tag-python-check:not(:checked)~#tag-recursion-check:not(:checked)~#tag-regex-check:not(:checked)~#tag-selenium-check:not(:checked)~#tag-shell-check:not(:checked)~#tag-sql-check:not(:checked)~#tag-udemy-check:not(:checked)~#tag-unit-testing-check:not(:checked)~#tag-web-check:not(:checked)~#tag-web-scraping-check:not(:checked)~main section .grid-container div.hideable	{
	display: flex;
}
```

So having scripts to generate this for me is extremely useful.

An example of the no-Javascript filtering is available on [Codepen](https://codepen.io/eatkin/pen/yLxbxgL).

Since I also maintain a structured [blog directory](https://github.com/Eatkin/Homepage/tree/master/txt/blog/), I use a script called [makeblogs.py](https://github.com/Eatkin/Homepage/blob/master/tools/makeBlogs.py) which I wrote to crawl the directory and gather all necessary information to make html pages from markdown source files, along with a blog index.