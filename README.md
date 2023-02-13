# IndieAnalysis

V okviru tega projekta nameravam zajeti podatke o najbolj prodajanih video igrah s spletne trgovine Steam (https://store.steampowered.com/search/?filter=topsellers)

### Podatki, ki jih potrebujem za posamezno igro:
- Naslov in opis
- Datum izdaje
- Ocena igre izražena s številom ocen in deležem pozitivnih ocen
- Žanr oz. značke posamezne igre

### Hipoteze:
- S časom se popularnost posameznih žanrov iger spreminja, v vsakem letu lahko določimo najbolj popularne 
- S časom povprečna cena izdelka narašča
- S časom je proporcionalno vedno več brezplačnih iger v primerjavi s številom vseh iger na trgu
- Veliko večino vseh izdelkov na Steam-u predstavljajo video igre, cenejše od 10€
- Kvaliteta izdelka ter število igralcev sta neposredno povezana s ceno izdelka

V datoteki igre.csv se nahajajo podatki: Naslov, Opis, podatki o ocenah, ID posamezne igre\n
V datoteki znacke.csv se nahajajo: ID posamezne igre, znacke

kraja_html.py vsebuje kodo za jemanje .html kode s spletne strani\n
zajem.py vsebuje kodo za parsanje kode iz html.txt
