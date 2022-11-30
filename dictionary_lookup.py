import requests
import sys
from bs4 import BeautifulSoup as bs

en_word = sys.argv[1]
url = f"https://jisho.org/search/{en_word}"

r = requests.get(url)

soup = bs(r.content, "lxml")

blocks = soup.find("div", {"class": "concept_light clearfix"})
# will match the first 3 best definitions/words of the english word given, or however many the word has if there are less than 3

f = open("output", "w")

j = 0
while blocks is not None and j < 3:
    if blocks.find_parent("div", {"class": "names"}) is not None:
        break

    word = blocks.find("span", {"class": "text"})
    if word is not None:
        print(word.text.strip(" \n\t") + "\n")
    pos = blocks.find("div", {"class": "meaning-tags"})

    if pos is not None:
        print(f"{pos.text}\n")
    # gets the 3 best meanings of the word, or less if there are not 3
    meanings = blocks.find_all("span", {"class": "meaning-meaning"}, limit=3)

    for i, meaning in enumerate(meanings):
        print(f"{i+1}. {meaning.text}\n")

    blocks = blocks.find_next("div", {"class": "concept_light clearfix"})
    j += 1

