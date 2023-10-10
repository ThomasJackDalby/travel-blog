import json
import re
import os
from bs4 import BeautifulSoup

file_path = "greenteaandnoodles.wordpress.2015-03-18.xml"
with open(file_path, "r", encoding="utf-8") as file:
    data = BeautifulSoup(file.read(), "xml")

post_count = 0

book = []
for post_element in data.find_all("item"):
    post_type = post_element.find("wp:post_type") 
    if post_type is None or post_type.contents[0] != "post": continue
    post_count += 1

    page = {
        "title" : post_element.find('title').contents[0],
    }

    # print(f"{post_count}) {title}")

    contents = post_element.find("content:encoded").contents[0]
    # extract captions

    match = re.finditer("\[caption.*\]", contents)

    def extract_image(source_text):
        link = re.search("href=\"([^\"]*)\"", source_text) 
        if link is None: return None

        image = { "file_name" : os.path.basename(link.group(1)) }
        caption = re.search("a\>([^\[]*)\[", source_text) 
        if caption is not None:
            caption = caption.group(1).strip()
            image["caption"] = caption
        return image
    
    images = []
    spans = []
    for caption_match in match:
        start, end = caption_match.span()
        images.append(extract_image(contents[start:end]))
        spans.append((start, end))
        # remove captions from inline
    
    for start, end in reversed(spans):
        contents = contents[:start].strip() + " " + contents[end:].strip()
    
    contents = contents.replace("\u00a0", " ")

    page["contents"] = contents
    page["images"] = images
    book.append(page)

with open("blog.json", "w") as file:
    json.dump(book, file, indent=4)