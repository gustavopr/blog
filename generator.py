# -*- coding: utf-8 -*-

# The python script that generates my blog from text files written in Markdown.
# It is still very, *very* rudimentary, but it works.

from __future__ import division

# Imports
import os
import sys
import time
import glob
import markdown2
from math import ceil

# Config Var(s)
postsPerPage = 10

# loads up header and footer
with open('header.txt', 'r') as f:
	html_header = f.read()

with open('footer.txt', 'r') as f:
	html_footer = f.read()


def markdown(string):
	# markdown2 writer
	markdowner = markdown2.Markdown()
	result = markdowner.convert(string)
	# put the class title inside the h1 tag
	result = result.replace("<h1>", "<h1 class=\"title\">") 
	return result

def createPost(url, body):
	# fix url for images and removes link in title
	body = body.replace("src=\"images/", "src=\"http://mnmal.me/images/")
	body = body.replace("<h1 class=\"title\"><a href=" + url + " class=\"titlelink\">", "<h1 class=\"title\">")

	# write the html file
	with open(url, 'w') as f:
		f.write(html_header + body.encode('utf-8') + html_footer)

def createHTML(root_dir):
	# sort files by mtime
	files = [(os.stat(i).st_mtime, i) for i in glob.glob(root_dir + "/*")]
	files.sort()
	files.reverse()

	totalPosts = len(files)
	postsMissing = totalPosts
	postsInThisPage = postsPerPage

	# iteration per page
	for page in range(1, int(ceil(totalPosts / postsPerPage)) + 1):
		HTML = ""
		
		# sets the posts counter for each page
		if postsMissing < postsPerPage:
			postsInThisPage = postsMissing
		else:
			postsMissing = postsMissing - postsPerPage
		
		# iteration per post
		for i in range(postsInThisPage):
			post = files[i + (page - 1) * postsPerPage]
			postDate = time.strftime(" - %d %b, %Y", time.localtime(os.stat(post[1]).st_mtime))

			with open(post[1], 'r') as f:
				body = str(markdown(f.read()))

			# create post footer
			body = body + "\n<div id=\"post-footer\"><p id=\"date-time\">" 
			body = body + post[1].split("/")[-1].replace(".txt", "")
			body = body  + postDate + "</p></div><br />\n\n"

			# create url for each post and insert it into the html created by the writer
			url = "posts/" + post[1].split("/")[-1].replace(".txt", "").replace(" ", "_") + ".html"

			body = body.replace("<h1 class=\"title\">", "<h1 class=\"title\"><a href=" + url + " class=\"titlelink\">")
			body = body.replace("</h1>", "</a></h1>")

			# and then create the single page for each post
			createPost(url, body)

			# put it all together
			HTML = HTML + body

		# puts navigation through pages in the bottom
		if page == 1 and int(ceil(totalPosts / postsPerPage)) > 1:
			HTML = HTML + "<div id=\"index\"><a href=\"page2.html\">next page</a><br /></div>"
		elif page == 2 and int(ceil(totalPosts / postsPerPage)) == 2:
			HTML = HTML + "<div id=\"index\"><a href=\"index.html\">previous page</a></div>"
		elif page == int(ceil(totalPosts / postsPerPage)) and int(ceil(totalPosts / postsPerPage)) > 1:
			HTML = HTML + "<div id=\"index\"><a href=\"page" + str(page - 1) + ".html\">previous page</a></div>"
		elif page <> 1 and page <> 2 and int(ceil(totalPosts / postsPerPage)) > 1:
			HTML = HTML + "<div id=\"index\"><a href=\"page" + str(page - 1) + ".html\">previous page</a> - "
			HTML = HTML + "<a href=\"page" + str(page + 1) + ".html\">next page</a><br />"
			HTML = HTML + "</div>"
		elif page == 2 and int(ceil(totalPosts / postsPerPage)) > 2:
			HTML = HTML + "<div id=\"index\"><a href=\"index.html\">previous page</a> - "
			HTML = HTML + "<a href=\"page" + str(page + 1) + ".html\">next page</a><br />"
			HTML = HTML + "</div>"

		# write html file per page with the header, the body and the footer
		# if it's the first page, calls it index.html, else calls it page#.html
		if page == 1:
			print "Writing index.html..."
			with open("index.html", "w") as f:
				f.write(html_header + HTML.encode('utf-8') + html_footer)

		else:
			print "Writing page" + str(page) + ".html"
			with open("page" + str(page) + ".html", "w") as f:
				f.write(html_header + HTML.encode('utf-8') + html_footer)

def main(argv=None):
	if argv is None:
		argv = sys.argv

	if len(argv) != 2:
		print "Usage:"
		print "python generator.py root-dir-for-the-text-files/"
		sys.exit(2)

	# define the root dir where the text files are 
	root_dir = argv[1]

	createHTML(root_dir)

if __name__ == '__main__':
	main()

