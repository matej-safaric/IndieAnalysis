import orodja
import re
import requests as req
import datetime
import json



#=============================================================================================================================#
url_sample = re.compile(
    r'<a href="(https:\/\/store\.steampowered\.com\/app\/.*?\/)\?snr=1_7_7',
    flags=re.DOTALL
    )

game_sample = re.compile(
    r'<div id="appHubAppName" class="apphub_AppName">(?P<title>.+?)<\/div>.*?' # Title
    r'<div class="game_description_snippet">(?P<description>.*?)<\/div>.*?' # Description
    r'<div class="subtitle column all">All Reviews:<\/div>.*?<div class="summary column">.*?\((?P<reviews_num>[0-9,]+)\).*?<\/span>.*?(?P<reviews_perc>\d+)%.*?' # Reviews
    r'<div class="date">(?P<release>[a-zA-Z0-9 ,]+?)<\/div>.*?' # Release date
    r'<div data-panel="{&quot;flow-children&quot;:&quot;row&quot;}" class="glance_tags popular_tags" data-appid="\d+">(?P<tags_messy>.*?)onclick="ShowAppTagModal\( \d+? \)">.*?' # Tags
    r'(?:<div class="game_purchase_price price".*?>(?P<price1>.*?)<\/div>|<div class="discount_original_price">(?P<price2>.*?)</div>)',
    flags=re.DOTALL
)

tag_sample = re.compile(
    r'<a href="https:\/\/store\.steampowered\.com\/tags\/.*?class="app_tag" style=".*?">\s*?([\w-]+?)\s*?<\/a>',
    flags=re.DOTALL
)
#=============================================================================================================================#


#=============================================================================================================================#
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
            try:
                game['price'] = game['price1'].strip()
            except:
                game['price'] = game['price2'].strip()
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

def json_to_csv(json_file: str, csv_file: str, tag_list: list):
    with open(json_file, encoding='UTF-8') as d:
        data = json.load(d)
    orodja.zapisi_csv(data, tag_list, csv_file)

# Seznam vseh atributov po prvotnem parsanju: 
# ['title', 'description', 'reviews_num', 'reviews_perc', 'release', 'tags_messy', 'price', 'price1', 'price2']
#=============================================================================================================================#

parse_html_to_json(data=data)

#=============================================================================================================================#
# Naknadni popravki

def open_json(json_file: str):
    with open(json_file, encoding='UTF-8') as d:
        return json.load(d)

def price_to_float(price: str) -> float:
    try:
        lst = price.split(',')
        if '--' in lst[1]:
            # Na tej spletni strani so cene ponekod zapisane kot npr. 3,-- namesto 3,00
            lst[1] = '0'
            print(lst)
        else:
            lst[1] = lst[1][:-1]
        out = float('.'.join(lst))
        return out
    except:
        return 0.0


def json_price_edit(json_file: str, koncna_datoteka: str):
    '''Ob zajemu podatkov je cena ostala tipa string, zato se ta funkcija sprehodi po json file-u in to popravi'''
    dataTemp = open_json(json_file)
    for elt in dataTemp:
        elt['price'] = price_to_float(elt['price'])
        # Eden od price1 in price2 bo None zato je to treba upostevati 
        elt['price1'] = elt['price1'].strip() if elt['price1'] is not None else elt['price1']
        elt['price2'] = elt['price2'].strip() if elt['price2'] is not None else elt['price2']
    orodja.zapisi_json(dataTemp, koncna_datoteka)
#=============================================================================================================================#

json_price_edit('podatki24074.json', 'podatki_price_edit.json')

#=============================================================================================================================#
# Radi bi razdelili en csv file na vec file-ov, namrec znacke posamezne igre ne morejo ostati v seznamu
# Najprej dolocimo ID vsaki igri, ki bo kar zaporedno stevilo v seznamu 

def add_id(json_file: str, out_ime: str):
    '''Funkcija vzame json datoteko in doda ID vrednost vsakemu elementu v datoteki vsebovanega seznama'''
    with open(json_file, encoding='UTF-8') as d:
        dataTemp = json.load(d)
    for (i, elt) in enumerate(dataTemp):
        elt['id'] = i
    orodja.zapisi_json(dataTemp, out_ime)

def date_to_year(json_file: str, out_ime: str):
    '''Funkcija zamenja atribut "release" za atribut "year" tako, da vzame datum oblike DD.MM.YYYY in izlušči leto'''
    dataTemp = open_json(json_file)
    for elt in dataTemp:
        date = elt['release']
        year = date.split('.')[2]
        elt['year'] = year
        _ = elt.pop('release')
    orodja.zapisi_json(dataTemp, out_ime)

#=============================================================================================================================#

add_id('podatki_price_edit.json', 'podatki_added_id.json')

#=============================================================================================================================#

def split(json_file: str, out1_ime: str, out2_ime: str):
    '''Funkcija se sprehodi po seznamu v json file-u in ustvari dve novi json datoteki:
        - Prva vsebuje enako kot prej, le znacke so izbrisane ter kljuca price1 in price2
        - Druga vsebuje le ID vrednosti iger ter njihove znacke'''
    dataTemp = open_json(json_file)
    out1 = []
    out2 = []
    for elt in dataTemp:
        for t in elt['tags_messy']:
            dictTemp = {
                'id' : elt['id'],
                'tag' : t
            }
            out2.append(dictTemp)
        _ = elt.pop('tags_messy')
        _ = elt.pop('price1')
        _ = elt.pop('price2')
        out1.append(elt)
    orodja.zapisi_json(out1, out1_ime)
    orodja.zapisi_json(out2, out2_ime)

 #=============================================================================================================================#

split('podatki_added_id.json', 'igre.json', 'znacke.json')   
json_to_csv('igre.json', 'igre.csv', ['id', 'title', 'description', 'reviews_num', 'reviews_perc', 'release', 'price'])
json_to_csv('znacke.json', 'znacke.csv', ['id', 'tag'])
        
