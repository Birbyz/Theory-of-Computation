import requests
import re

expr = re.compile(r'\<p\sclass=\"css\-xl6fe0\-Text\seu5v0x0\">([0-9].+)\slei\<\/p\>')

def get_salary(url):
    r = requests.get(url)
    match = expr.search(r.text)
    if not match:
        return get_salary(url)

    return match.group(1)

salary = get_salary('https://www.olx.ro/oferta/loc-de-munca/presto-pizza-angajeaza-livrator-IDbqkxs.html')
print(salary)


