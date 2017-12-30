#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from bs4 import BeautifulSoup
import codecs, io, requests, urllib, json, time

def getPage(letra, s):
    payload = {
        'perfil': 'Home',
        'contexto': '',
        'contexto1': '',
        'BuscaTodos': 'sim',
        'cans': '',
        'razs': letra,
        'cnpj': ''
    }

    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '68',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Host': 'www.ans.gov.br',
        'Origin': 'http://www.ans.gov.br',
        'Referer': 'http://www.ans.gov.br/portal/site/perfil_operadoras/consulta_operadoras/default.asp',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }

    page = s.post('http://www.ans.gov.br/portal/site/perfil_operadoras/consulta_operadoras/default.asp', data = payload, headers = header)
    return BeautifulSoup(page.content, 'html5lib')

def getPlan(codigo, s):
    header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'DNT':'1',
        'Host':'www.ans.gov.br',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }

    page = s.get("http://www.ans.gov.br/portal/site/perfil_operadoras/consulta_planos/busca_planos.asp?contexto=''&cans="+codigo, headers=header)
    
    page = BeautifulSoup(page.content.decode('latin_1'), 'html5lib')
    
    col1 = page.find_all('table')[6].find_all('tr')

    item = {'Total de Beneficiários': 0}

    for x in col1:
        if x.find_all('td')[0].text.strip() == "Total de Beneficiários":
            item[x.find_all('td')[0].text.strip()] = int(col1[11].find_all('td')[1].text.strip().split('-')[0].strip().replace('.', ''))
        else:
            item[x.find_all('td')[0].text.strip()] = x.find_all('td')[1].text.strip()

    item['Código Operadora'] = int(item['Código Operadora'])
    if item['Complemento'] == "_":
        item['Complemento'] = ""
    
    return item

ini = time.time()

s = requests.session()
s.get('http://www.ans.gov.br/portal/site/perfil_operadoras/consulta_operadoras/default.asp')

todos = {}

for x in range(26):
    letra = str(chr((ord('a')+x)))
    pagina = getPage(letra, s)

    pagina = pagina.find_all('tr', {'class':'bg-cinza-4'})

    for y in pagina:
        item = y.find_all('td')
        todos[item[0].text.strip()] = {
            'id': int(item[0].text.strip()),
            'Nome Fantasia': item[3].text.strip()
        }

lista = []

for key in todos:
    item = getPlan(key, s)
    for x in item:
        todos[key][x] = item[x]
    lista.append(todos[key])

with io.open('planos_de_saude.json', 'w', encoding='utf-8') as f:
    json.dump(lista, f, ensure_ascii=False)

print("Tempo de execução:", time.time()-ini)