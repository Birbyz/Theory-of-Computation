import requests
import re
import os

try:
    import requests
except ImportError:
    os.system('cmd /c "pip install requests"')
    import requests

site = 'https://www.olx.ro'
category = '/locuri-de-munca'

number_of_pages = 1
# CATEGORIES : 
# 1. sofer - sofer, curier, 'tractorist'
# 2. constructie - zidar, tamplar, stivuitorist, 'buldoexcavatorist', 'macaragiu', 'lucrator', 'muncitor(i)"
# 3. meserii tehnice - 'electrician', 'mecanic', 'sudor(i)', 'lacatus', 'tehnician', 'montator'
# 4. delivery - livrator(i), 'postas', 'distribuitor', 'manipulanti marfa', 'descarcator'
# 5. make-up & beauty - 'coafeza', 'manichiurista', 'pedichiurista',
# 6. food & drinks - 'pizzer', "bucatar", 'barman', 'ospatar', 'macelar',
# 7. sanitary - 'menajera', 'ingrijitor', 'infirmiera', 'hostess'
# 8. social - 'operator', 'casier/a', "agent", 'dispecer', 'vanzatoare', 'lucrator comercial','receptioner'
# 9. kids - 'bona', 'educator / educatoare', 
# 10. desk jobs - 'contabil', 'consilier', 'croitor', 'inspector', 'translator', 'operator'

# RegEX:
regex = {
    'driver': r'(soferi?|curieri?|tractoristi?)',
    'constructions': r'(zidari?|tamplari?|stivuitoristi?|buldoexcavatoristi?|macaragi(u|i)|lucratori?|muncitori?)',
    'tech': r'(electici(an|eni)|mecanici?|sudori?|lacatusi?|tehnici(an|eni)|montatori?)',
    'delivery': r'(livratori?|posta(s|rita)?|distribuito(ri?|are)|manipulanti?|descarcato(ri?|oare))',
    'cosmetics': r'(coafez(a|e)?|manichiurist(a|e)?|pedichiurist(a|e)?)',
    'food': r'(pizzeri?|bucatar(i|e(se|asa))|barmani?|ospatar(i|e(se|asa))|macelar(i|e(se|asa)))',
    'sanitary': r'(menajer(a|e|i)?|ingrijito(ri?|are)|infirmier(a|e|i)?|hostess(a|es?))',
    'social': r'(operato(ri?|are)|casier(a|e|i)?|agent(a|e|i)?|dispecer(a|e|i)?|vanzato(ri?|are)|lucrato(ri?|are) comercial(i|a)?|receptioner(i|a|e)?)',
    'kids': r'(bon(a|e)|educato(ri?|are))',
    'desk': r'(contabil(a|e|i)?|consilier(a|e|i)?|croitor(i|e(asa|se))?|inspecto(ri?|are)|translator(a|e|i)?|operato(ri?|are))',
    'higher': None,
    'lower': None,
    'between': None
}

'''
    keys = {
        # driver = []
        # constructions = []
        ...
        *will add links later
} 
'''
keys = {key: [] for key in regex.keys()}
expr = re.compile(r'\<p\sclass=\"css\-xl6fe0\-Text\seu5v0x0\">([0-9].+)\slei\<\/p\>')

# extracting salaries
def get_salary(url: str, depth = 0):
    if depth == 4:
        return None

    r = requests.get(url)
    match = expr.search(r.text)
    if not match:
        return get_salary(url, depth = depth+1)

    salary = match.group(1).split(" - ")
    return salary[0] if len(salary) == 1 else salary[1].replace(" ", '')


# looking for sites having the href type and a 10-letters/digits code at the end
pattern = re.compile(r'href=\"(.*\.html\#[a-z0-9]{1,10})\"')
    # <p class="css-xl6fe0-Text eu5v0x0">4 500 - 7 000 lei</p>
expr = re.compile(r'\<p\sclass=\"css\-xl6fe0\-Text\seu5v0x0\">([0-9].+)\slei\<\/p\>')


print('''
/**
*   OLW - Web Crawler - Course CS112
*   @author: Filimon 'Birbyz' Ioana-Andreea
*   13.05.2022
*/
''' )
print('\n')
while True:
    if number_of_pages == 1:
        url = site + category
    else: 
        url = site + category + f'/?page={number_of_pages}'
    print("Extracting announcemenets...")
    response = requests.get(url, allow_redirects=False)
    patterns = re.findall(pattern, response.text)

    # retry request on same page if this fails
    if not patterns and number_of_pages != 1:
        break

    # adding links in a list
    print("Sorting current page's links...")
    for p in patterns:
        # links sort
        for key in keys.keys():
            reg = regex[key]
            if reg and re.search(regex[key], p):
                keys[key].append(p)
                break
        
        # higher = salaries higher than 10000 RON
        # lower = lower than 5000 RON
        # between = between higher and lower

        # looking for salaries
        salary = get_salary(p)
        if salary is not None:
            match = re.search(r'(?P<higher>[0-9]{5,9})|(?P<between>[1-4][0-9]{3})|(?P<lower>[5-9][0-9]{3})', salary)
            if match:
                for key, value in match.groupdict().items():
                    if value:
                        keys[key].append(p)
                        break

    print(f"current page: {number_of_pages}")
    print('\n')
    number_of_pages = number_of_pages+1

category_number = 1

file = open('output.html', 'w')

file.write('''
    <!DOCTYPE html>
        <head>
            <h1> <b> OLX - Locuri de munca </b> </h1>
        </head>

        <body>
    ''')

for key in keys.keys():
    file.write(f"<br><br><h2><i> {category_number}. {key} </i></h2> <br>")
    for link in keys[key]:
        file.write(f"<a href={link}> {link} </a> <br>")
    category_number += 1

file.write('''
            <footer>
                <br>
                <hr>
                    <sub>
                        This project was made by: <br>
                                - Filimon Ioana-Andreea <br>
                                - Popescu Mihaela-Maria <br>
                                - Mihai Andrei-Alexandru <br>
                        <center> <i> University of Bucharest - Faculty of Mathematics and Informatics </i> -<b> Course CS112 </b> </center>
                    </sub>
            </footer>

        </body>
    </html>
    ''')
file.close()

os.system('cmd /c "output.html"')