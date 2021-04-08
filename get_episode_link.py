import requests
from lxml import html
import json
url = "https://kissanimes.su/anime/naruto-shippuuden-dub-/13912/"

page = requests.get(url)
page_content = html.fromstring(page.content)

def get_episode_link():
    episodes_dict = {}
    names = page_content.xpath("//ul[@id='episode_related']//li//div[@class='name']//text()[not(contains(.,'EP'))]")
    links = page_content.xpath("//ul[@id='episode_related']//li//a//@href")

    for i,j in enumerate(names):
        episodes_dict[j] = links[i]

    return episodes_dict

# with open("episode_list.json",'w') as file:
#     file.write(json.dumps(episodes_list,indent=2))

