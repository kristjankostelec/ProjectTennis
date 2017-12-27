import re

with open('nadal1') as f:
    vsebina = f.read()

stevilo = 0

izraz = re.compile(
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
    
    
    
    ,
    flags = re.DOTALL
    )

for ujemanje in izraz.finditer(vsebina):
    print(ujemanje.groupdict())
    #stevilo += 1
#print(stevilo)

#print(vsebina)

    

#print(len(vsebina))
