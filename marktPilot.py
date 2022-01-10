# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 15:36:29 2022

@author: marth
"""

from flask import Flask, render_template, jsonify, request
from Factory.SitesAdapterFactory import SitesAdapterFactory
from DB.ProductDBModelAdapter import ProductDBModelAdapter
import pandas as pd

from Services.ProductService import ProductService

app = Flask(__name__)
products_db_adapter = ProductDBModelAdapter()
product_service = ProductService()

@app.route('/', methods=("POST","GET"))
def index():
    product_summary = product_service.summary()
    return render_template('products.html', page_data=product_summary)

@app.route('/search', methods=("POST","GET"))
def search():
    args = request.args.to_dict()
    filtered_products = products_db_adapter.get_products(WHERE=args)
    product_summary = product_service.get_summary(filtered_products)
    return render_template('products.html', page_data=product_summary)


@app.route('/start-scrapper', methods=("POST","GET"))
def scrapper():
    adapter_factory = SitesAdapterFactory()
    site_products = adapter_factory.initialize_scrapping()
    for site in site_products:
        df = pd.DataFrame(site_products[site])
        df.to_csv('{}_comparison.csv'.format(site))
        
    return jsonify(site_products)

@app.route('/results', methods=("POST","GET"))
def get_products():
    args = request.args.to_dict()
    print(args)
    all_products = products_db_adapter.get_products(WHERE=args)
    return jsonify(all_products)

if __name__ == '__main__':
    app.run(host='0.0.0.0')