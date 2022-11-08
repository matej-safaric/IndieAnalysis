import orodja
import re
# temp
import requests as req

url_sample = re.compile(
    r'<a href="(https:\/\/store\.steampowered\.com\/app\/.*?\/)\?snr=1_7_7',
    flags=re.DOTALL
    )

game_sample = re.compile(
    r'<div id="appHubAppName" class="apphub_AppName">(?P<title>.+?)<\/div>.*?' # Title
    r'<div class="game_description_snippet">(?P<description>.*?)<\/div>.*?' # Description
    r'<div class="subtitle column all">All Reviews:<\/div>.*?<div class="summary column">.*?\((?P<reviews_num>[0-9,]+)\).*?<\/span>.*?(?P<reviews_perc>\d+)%.*?' # Reviews
    r'<div class="date">(?P<release>[a-zA-Z0-9 ,]+?)<\/div>.*?' # Release date
    r'<div data-panel="{&quot;flow-children&quot;:&quot;row&quot;}" class="glance_tags popular_tags" data-appid="\d+">(?P<tags_messy>.*?)onclick="ShowAppTagModal\( \d+? \)">', # Tags
    #r'<div class="game_purchase_price price">(?P<price>.*?)<\/div>',
    flags=re.DOTALL
)

tag_sample = re.compile(
    r'<a href="https:\/\/store\.steampowered\.com\/tags\/.*?class="app_tag" style=".*?">\s*?([\w-]+?)\s*?<\/a>',
    flags=re.DOTALL
)

with open('html.txt', encoding='UTF-8') as d:
    data = d.read()

# Temp sample code
with open('sample_html.txt', encoding='UTF-8') as d:
    sample = d.read()

with open('sample_gamesite_html.txt', encoding='UTF-8') as d:
    sample_game = d.read()

def gamesite_parse(html_code):
    pass

def str_to_date(str: str):
    months = {
        'jan': '1',
        'feb': '2',
        'mar': '3',
        'apr': '4',
        'may': '5',
        'jun': '6',
        'jul': '7',
        'aug': '8',
        'sep': '9',
        'oct': '10',
        'nov': '11',
        'dec': '12'
    }
    list = str.lower().split(' ') 
    m = list[1].replace(',', '')
    list[1] = months[m]
    return '.'.join(list)

for url in url_sample.finditer(sample):
    r = req.get(url.group(1))
    t = r.text
    game = game_sample.search(t).groupdict()
    game['tags_messy'] = [tag.group(1) for tag in tag_sample.finditer(game['tags_messy'])]
    game['description'] = game['description'].strip()
    game['reviews_num'] = int(game['reviews_num'].replace(',',''))
    game['reviews_perc'] = int(game['reviews_perc'])
    game['release'] = str_to_date(game['release'])
    print(game)
