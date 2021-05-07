import requests
from bs4 import BeautifulSoup

response = requests.get("https://rapperviper.bandcamp.com/music")
soup = BeautifulSoup(response.content, "html.parser")
f = open("data/bandcamp_albums.txt", "w")
for element in soup.select("p[class='title']"):
    f.write(element.text.strip() + "\n")
f.close()