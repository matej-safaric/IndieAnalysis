import orodja
import re

vzorec_bloka = re.compile(
    r'<a href="https:\/\/store\.steampowered\.com\/app\/.*?'
    r'<div style="clear: left;"><\/div>',
    flags=re.DOTALL
    )

orodja.shrani_spletno_stran('https://store.steampowered.com/search/?category1=998&filter=topsellers', 'html.txt')