import requests
import os
import re
import string
import csv

first_page = 'http://www.atpworldtour.com/en/rankings/singles?rankDate=2017-12-25&rankRange=1-3'
test = 'http://www.atpworldtour.com/en/players/rafael-nadal/n409/overview'

izraz_za_url = re.compile(
    '<td class="player-cell">.*?'
    '<a href="(?P<url>.*?)".*?>(?P<ime>.*?)</a>',
    flags = re.DOTALL
    )


izraz_osnovni_podatki = re.compile(
    # ime
    r'hero-name(\"|\')>.*?<div class=(\"|\')first-name(\"|\')>'
    r'(?P<ime>.*?)</div>'
    r'.*?'
    # priimek
    r'<div class=(\"|\')last-name(\"|\')>'
    r'(?P<priimek>.*?)</div>'
    r'.*?'
    # drzava
    r'<div class=(\"|\')player-flag-code(\"|\')>'
    r'(?P<drzava>.*?)</div>'
    r'.*?'
    # starost
    r'Age</div>\n\s*?<div class=(\"|\')table-big-value(\"|\')>\n\s*?'
    r'(?P<starost>\d{2})'
    r'.*?'
    # rojstni dan
    r'<span class=(\"|\')table-birthday(\"|\')>\n\s*?\('
    r'(?P<rojstni>.*?)\)'
    r'.*?'
    # singles ranking
    r'data-singles=(\"|\')'
    r'(?P<rank>\d+)',
    flags=re.DOTALL)

izraz_teza = re.compile(
    # weight
    r'class=(\"|\')table-weight-kg-wrapper(\"|\')>\('
    r'(?P<teza_kg>\d+)kg\)'
    r'.*?',
    flags=re.DOTALL)

izraz_visina = re.compile(
    # height
    r'class=(\"|\')table-height-cm-wrapper(\"|\')>\('
    r'(?P<visina_cm>\d+)cm\)'
    r'.*?',
    flags=re.DOTALL)

izraz_igre = re.compile(
    # 2017 W-L
    r'Move.*?</div>.*?</td>.*?<td colspan=(\"|\')1(\"|\')>.*?'
    r'class=(\"|\')stat-value(\"|\')>.*?'
    r'(?P<razmerje17>\d+-\d+).*?</div>'
    r'.*?'
    # 2017 titles
    r'W-L.*?</div>.*?</td>.*?<td colspan=(\"|\')1(\"|\')>.*?'
    r'class=(\"|\')stat-value(\"|\')>.*?'
    r'(?P<naslovi17>\d+).*?</div>'
    r'.*?'
    # 2017 prize money
    r'class=(\"|\')stat-value(\"|\')>.*?\$'
    r'(?P<zasluzki17>(,|\d)*).*?</div>'
    r'.*?'
    # career high
    r'class=(\"|\')stat-value(\"|\')>.*?'
    r'(?P<vrhunec>\d+)'
    r'.*?'
    # career W-L
    r'class=(\"|\')stat-value(\"|\')>.*?'
    r'(?P<k_razmerje>\d+-\d+)'
    r'.*?'
    # carrer titles
    r'W-L.*?</div>.*?</td>.*?<td colspan=(\"|\')1(\"|\')>.*?'
    r'class=(\"|\')stat-value(\"|\')>.*?'
    r'(?P<k_naslovi>\d+)'
    r'.*?'
    # career prize money (S&D combined)
    r'class=(\"|\')stat-value(\"|\')>.*?\$'
    r'(?P<k_zasluzki>(,|\d)*)',
    flags = re.DOTALL
    )

def page_to_file(url, file):
    try:
        request = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('connection lost - force shut your computer and hide under the desk until internet is back on.')
        return
    with open(file, 'w',encoding = 'utf-8')as f:     
        f.write(request.text)
        return

def zapisi_podatke(prvi):
        prvi.write(pod['ime'] + ' ' + pod['priimek'] + ': ')
        for podatek in seznam_podatkov:
             if podatek not in {'ime','priimek','k_zasluzki'}:
                 if pod.get(podatek) == None:
                     prvi.write('/;')
                 else:
                     prvi.write(pod[podatek] + '; ')
        prvi.write(pod['k_zasluzki'] + '\n')



page_to_file(first_page,'tenisaci')
seznam_podatkov = ['ime','priimek','rank','drzava','starost','rojstni',
                   'teza_kg','visina_cm','razmerje17',
                   'naslovi17','zasluzki17','vrhunec','k_razmerje',
                   'k_naslovi','k_zasluzki']


#--------------------------------
#konstruiramo seznam s stranmi igralcev
seznam_igralcev = []
with open ('tenisaci') as ten:
    tenisac = ten.read()
    
for ujemanje in izraz_za_url.finditer(tenisac):
    seznam_igralcev.append(ujemanje.groupdict())

igralci = []
            
for igralec in seznam_igralcev:
    flag = False
    if '#' in igralec['url']:
            flag = True
    if flag == False:
        igralci.append((igralec['ime'],'http://www.atpworldtour.com' + igralec['url']))

#------------------------------
#vse strani igralcev
for igralec in igralci:
    ime = igralec[0]
    if os.path.exists(ime)== False:
        print('dajem dol',ime)
        page_to_file(igralec[1],ime)
    else:
        print('ze obstajam')

#-------------------------------------

#zapis vseh podatkov   
with open('vsi_podatki.csv', 'w',encoding = 'utf-8') as podatki:
    for igralec in  igralci:
        ime=igralec[0]
        with open(ime, 'r', encoding='utf-8') as dat:
                datt = dat.read()
        for ujemanje in izraz_osnovni_podatki.finditer(datt):
            pod = ujemanje.groupdict()
            
        for ujemanje in izraz_teza.finditer(datt):
            pod['teza_kg'] = (ujemanje.groupdict())['teza_kg']
            
        for ujemanje in izraz_visina.finditer(datt):
            pod['visina_cm'] = (ujemanje.groupdict())['visina_cm']

        for ujemanje in izraz_igre.finditer(datt):
            print(ujemanje)
            for info in seznam_podatkov[-7:]:
                print(info)
                pod[info] = (ujemanje.groupdict())[info]

        zapisi_podatke(podatki)
