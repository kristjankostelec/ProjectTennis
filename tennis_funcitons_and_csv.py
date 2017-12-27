import requests
import os
import re
import string
import csv
import json

first_page = 'http://www.atpworldtour.com/en/rankings/singles?rankDate=2017-12-25&rankRange=1-100'
test = 'http://www.atpworldtour.com/en/players/rafael-nadal/n409/overview'

'''
strani_igralcev (velika_stran) =

izraz_za_url = re.compile(
    r'<td class="player-cell">'
    r'<a href=(?P<url>.*?) data-.*?>(?P<ime>.*?)</a>'
    r'.*?'
    flags = re.DOTALL
    )

'''
izraz_podatki2 = re.compile(
    # ime
    '<div class="first-name">'
    '(?P<ime>.*?)</div>'
    '.*?'
    # priimek
    '<div class="last-name">'
    '(?P<priimek>.*?)</div>'
    '.*?'
    # singles ranking
    '<div class="data-number" style="margin-left: 10px">.*?'
    '(?P<rank>\d+)'
    '.*?'
    # drzava
    '<div class="player-flag-code">'
    '(?P<drzava>.*?)</div>'
    '.*?'
    # starost
    'Age</div>\n\s*?<div class="table-big-value">\n\s*?'
    '(?P<starost>\d{2})'
    '.*?'
    # rojstni dan
    '<span class="table-birthday">\n\s*?\('
    '(?P<birthday>.*?)\)'
    '.*?'
    # turned pro
    'Turned Pro</div>\n\s*?<div class="table-big-value">.*?'
    '(?P<turnedpro>\d{4})'
    '.*?'
    # weight
    'class="table-weight-kg-wrapper">\('
    '(?P<teza_kg>\d+)kg\)'
    '.*?'
    # height
    'class="table-height-cm-wrapper">\('
    '(?P<visina_cm>\d+)cm\)'
    '.*?'
    # birthplace
    'Birthplace\n\s*?</div>\n\s*?<div class="table-value">.*?'
    '(?P<rojstnikraj>[A-Z].*?)\n\s*?<'
    '.*?'
    # prebivalisce
    'Residence</div>.*?<div class="table-value">'
    '(?P<prebivalisce>.*?)<'
    '.*?'
    # trener/ka/ji/ke
    'Coach</div>.*?<div class="table-value">.*?'
    '(?P<trener_ji>[A-Z].*?)\n'
    '.*?'
    # 2017 W-L
    'Move.*?</div>.*?</td>.*?<td colspan="1">.*?'
    'class="stat-value">.*?'
    '(?P<razmerje17>\d+-\d+).*?</div>'
    '.*?'
    # 2017 titles
    'W-L.*?</div>.*?</td>.*?<td colspan="1">.*?'
    'class="stat-value">.*?'
    '(?P<naslovi17>\d+).*?</div>'
    '.*?'
    # 2017 prize money
    'class="stat-value">.*?\$'
    '(?P<zasluzki17>(,|\d)*).*?</div>'
    '.*?'
    # career high
    'class="stat-value">.*?'
    '(?P<careerhigh>\d+)'
    '.*?'
    # career W-L
    'class="stat-value">.*?'
    '(?P<careerrazmerje>\d+-\d+)'
    '.*?'
    # carrer titles
    'W-L.*?</div>.*?</td>.*?<td colspan="1">.*?'
    'class="stat-value">.*?'
    '(?P<careertitles>\d+)'
    '.*?'
    # career prize money (S&D combined)
    'class="stat-value">.*?\$'
    '(?P<careerzasluzki>(,|\d)*)',
    flags = re.DOTALL
    )

def page_to_file(url, file):
    try:
        request = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('connection lost - force shut your computer and hide under the desk until internet is back on.')
        return
    with open(file, 'w', encoding = 'utf-8') as f:
        f.write(request.text)
        return

page_to_file(test,'nadal1')


with open ('nadal1') as nad:
    nadal = nad.read()

dict={}
for ujemanje in izraz_podatki2.finditer(nadal):
    dict = ujemanje.groupdict()

seznam_podatkov = []
for podatek in dict:
    seznam_podatkov.append(podatek)
seznam_podatkov = sorted(seznam_podatkov)

with open('prvi_podatki', 'w', encoding = 'utf-8') as prvi:
    prvi.write(dict.get('ime') + ' ' + dict.get('priimek') + ': ')
    for podatek in seznam_podatkov:
        if podatek not in {'ime','priimek'}:
            prvi.write(dict.get(podatek) + '; ')
'''
with open('prvi_podatki','w', encoding = 'utf-8') as prvi:
        dict = (izraz_podatki2.finditer(nadal)).groupdict()
        prvi.write(dict('ime')+':')
        for podatek in dict:
            if podatek != 'ime':
                prvi.write(dict(podatek)+',')
'''
'''
TODO FUNKCIJE:
    . save page to file
    . read file to string
    . write csv
    .
    . vmes: razdeli file na poddele
'''
