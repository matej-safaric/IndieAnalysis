import orodja
import re
# temp
import requests as req

url_sample = re.compile(
    r'<a href="(https:\/\/store\.steampowered\.com\/app\/.*?\/)\?snr=1_7_7',
    flags=re.DOTALL
    )

game_sample = re.compile(
    r'',
    flags=re.DOTALL
)

with open('html.txt', encoding='UTF-8') as d:
    data = d.read()

# Temp sample code
with open('sample_html.txt', encoding='UTF-8') as d:
    sample = d.read()

def gamesite_parse(html_code):
    pass

for url in url_sample.finditer(sample):
    r = req.get(url.group(1))
    t = r.text
    gamesite_parse()


