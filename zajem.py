import orodja
import re
import requests as req
import datetime
import json

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


def str_to_date(str: str):
    '''Sprejme niz oblike "DD MMM, YYYY" (npr. "11 Sep, 2001") in vrne zapis oblike "DD.MM.YYYY"'''
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

def parse_html_to_json(data: str):
    out = []
    count = 0 # Ta spremenljivka je tu le zaradi lazjega sledenja programu med obratovanjem
    for url in url_sample.finditer(data): # Sprehodi se po vseh igrah na strani in gre za vsako igro na njeno dedicated spletno stran, kjer pobere podatke
        try:
            r = req.get(url.group(1))
            t = r.text
            game = game_sample.search(t).groupdict()
            game['tags_messy'] = [tag.group(1) for tag in tag_sample.finditer(game['tags_messy'])]
            game['description'] = game['description'].strip()
            game['reviews_num'] = int(game['reviews_num'].replace(',',''))
            game['reviews_perc'] = int(game['reviews_perc'])
            game['release'] = str_to_date(game['release'])
            out.append(game)
        except:
            print(f'{count}: Error! url:{url.group(1)}')
            continue
        if count % 200 == 0:
            orodja.zapisi_json(out, f'podatki{count}.json') # Na vsakih 200 iger shrani rezultat v nov json (za vsak slucaj)
        print(count)
        count += 1
    orodja.zapisi_json(out, f'podatki{count}.json')
    print(datetime.datetime.now())       # Da vem ob kateri uri je program koncal in koliko casa je potreboval

def json_to_csv(json_file: str, csv_file: str):
    with open(json_file, encoding='UTF-8') as d:
        data = json.load(d)
    orodja.zapisi_csv(data, ['title', 'description', 'reviews_num', 'reviews_perc', 'release', 'tags_messy'], csv_file)
 
parse_html_to_json(data=data)
json_to_csv('podatki25455.json', 'vsc_csv.csv')