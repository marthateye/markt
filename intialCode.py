# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 15:36:29 2022

@author: marth
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


pgMax=28 #Total Number of pages to search through
#baseurl = "https://www.wollplatz.de/"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
productlinks = []
data=[]
checkbool=0;
searchList = {'Drops': ['Safran', 'Baby Merino Mix'], 'DMC': 'Natura XL', 'Hahn': 'Alpacca Speciale', 'Stylecraft': 'Special double knit'}

for x in range(1,pgMax):
    k = requests.get('https://www.wollplatz.de/wolle?page={}'.format(x)).text
    soup=BeautifulSoup(k,'html.parser')
    productlist = soup.find_all("div",{"class":"productlistholder"})

    for product in productlist:
        link = product.find("a",{"class":"productlist-imgholder"}).get('href')
        productlinks.append(link)

        f = requests.get(link,headers=headers).text
        hun=BeautifulSoup(f,'html.parser')
        
        try: 
            name=hun.find("span",{"class":"variants-title-txt"}).text.replace('\n',"")
            #print(name)
            nameSplit= name.split(" ", 1)
            brand= nameSplit[0]
            #print(brand)
            productName=nameSplit[1]
            
            for key, value in searchList.items():
                
                if (brand == key and productName in value):
                    checkbool = 1
                 
        except:
            name=None
        
        if checkbool == 1:
            try:
                price = hun.find("span",{"class":"product-price-amount"}).text.replace('\n',"")
            except:
                price = None
                
            try:   
                gdp_table = hun.find("div", {"id": "pdetailTableSpecs"})
                table = gdp_table.find('table')
                gdp_table_data = table.find_all("tr")  # contains 2 rows
                
                composition = gdp_table_data[3].find_all("td")[1].text.replace('\n',"")
                size = gdp_table_data[2].find_all("td")[1].text.replace('\n',"")
            except:
                composition = None
                size = None
            
            #print(composition)
             
            wool = {"name":name,"price":price, "composition":composition, "needle size":size}
            
            data.append(wool)
            
            checkbool=0

df = pd.DataFrame(data)
df.to_csv('wool_comparison.csv')
print(df)

from flask import Flask, render_template

import pandas as pd


app = Flask(__name__)


@app.route('/', methods=("POST", "GET"))
def html_table():

    #return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    return render_template('simple.html',  tables=[df.to_html(classes='data', header="true")])


if __name__ == '__main__':
    app.run(host='0.0.0.0')