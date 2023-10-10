## takes blog content from a .json and creates a "bobs books" .mcf file

import json
import re
import os
from bs4 import BeautifulSoup
from bs4 import CData
XML_TEMPLATE = """
<area areatype="textarea">
    <position height="565" left="155" rotation="0" top="165" width="2300" zposition="7000"/>
    <decoration/>
    <text applySpotColor="0" areaTextType="content">
        <textFormat Alignment="ALIGNLEADING" IndentMargin="5" VerticalIndentMargin="50" backgroundColor="#00000000" font="Calibri,16,-1,5,50,0,0,0,0,0" foregroundColor="#ff000000" hasOutline="0"/>
    </text>
</area>"""

HTML_TEMPLATE = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
<head>
    <meta name="qrichtext" content="1" />
    <style type="text/css">p { margin-bottom:50px; }</style>
</head>
<body style="font-family:'Calibri'; font-size:16pt; font-weight:400; font-style:normal;">
    <table style="-qt-table-type: root; margin-top:5px; margin-bottom:5px; margin-left:5px; margin-right:5px;">
        <tr>
            <td style="border: none;"></td>
        </tr>
    </table>
</body>
</html>
"""

P_TEMPLATE = """
<p><span></span>

</p>"""

file_path = "template.mcf"
with open(file_path, "r", encoding="utf-8") as file:
    data = BeautifulSoup(file.read(), "xml")

with open("blog.json", "r") as file:
    book_json = json.load(file)

pages = data.find_all("page")
for index, page_json in enumerate(book_json):
    page = data.find("page", { "pagenr" : str(index+2) })
    if page is None:
        continue

    text_element = BeautifulSoup(XML_TEMPLATE, "xml")

    html_soup = BeautifulSoup(HTML_TEMPLATE, "html.parser")
    td_soup = html_soup.find("td")
    lines = page_json["contents"].split("\n")
    lines = filter(lambda line: line != "", lines)
    for line in lines:
        p_soup = BeautifulSoup(P_TEMPLATE, "html.parser")
        p_soup.find("span").append(line.strip())
        td_soup.append(p_soup)

    text_element.find("text").insert(0, CData(str(html_soup)))
    page.append(text_element)

with open("book.mcf", "w") as file:
    file.write(data.prettify())
    