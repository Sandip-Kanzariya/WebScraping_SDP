from flask import Flask, render_template, request
import subprocess as sp
from pymongo import MongoClient
from mongopass import mongopass

import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import csv

app = Flask(__name__)

client = MongoClient(mongopass)
db = client.webScaping
netmeds = db.netmeds
zeeLab = db.zeeLab
truemeds = db.truemeds

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/netmeds')
def netmeds_data():
    title_list = []
    price_list = []
    image_url_list = []

    for i in range(1, 4):
        url = f"https://www.netmeds.com/non-prescriptions/ayush/homeopathy/page/{i}"
        webpage = requests.get(url).text
        print(i)
        # webpage
        soup = BeautifulSoup(webpage, 'html.parser')

        companies = soup.find_all('div', class_='product-list')

        for company in companies:
            cat_items = company.find_all(class_='cat-item')
            for item in cat_items:
                # Take Price
                price = item.find_all('span', class_="price-box")
                price = price[0].find('span')

                # Take Imgae URL
                image = item.find_all('span', class_="cat-img")
                image = image[0].find_all('img', class_="product-image-photo")
                image = image[0]
                image_url_list.append(image['src'])

                # Take Title
                item = item.find_all('a', class_="category_name")
                item = item[0]
                title = item.find_all('span', class_="clsgetname")
                title_list.append(title[0].text)
                price_list.append(price.text)
                
                # Store data in MongoDB
                netmeds.insert_one({
                    'Title': title[0].text,
                    'Price': price.text,
                    'ImageUrl': image['src']
                })

    results = {'Title': title_list, 'Price': price_list, 'ImageUrl': image_url_list}

    return render_template('netmeds.html', data=results)


@app.route('/zeelab')
def zeelab_data():

    url = f"https://zeelabpharmacy.com/health/bone-joints"
    webpage=requests.get(url).text

    # webpage
    soup = BeautifulSoup(webpage,'html.parser')
    products=soup.find_all('div', class_='filterArea')

    product_list_ = []
    for product in products:
        product_list_.append(product.find_all('div', class_='newProductCard pdcrd'))


    title_list = []
    product_link_list = []
    price_list = []
    image_url_list = []
    product_info = []

    product_list = product_list_[0]

    for product in product_list:

        # Info
        info = product.find('p')
        info = info.text
        product_info.append(info)

        # For Product Name
        title = product.find('span', class_='newProductName')
        name = title.text
        name = name.strip() # trim extra spaces
        title_list.append(name)

        # For Product Link
        link_element = product.find('a', class_='pr_search')
        link = link_element['href']
        product_link_list.append(link)

        # For Product Price
        price = product.find('span', class_='newProductPrice')
        price = price.text.strip()
        price_list.append(price)

        # For Image URL
        image = product.find_all('img','productOuterImage')
        image = image[0]
        image_url = image['src']; # image_url = image['data-original']; # print(image_url)
        image_url_list.append(image_url)
        
        # Store data in MongoDB
        zeeLab.insert_one({
            'Title': name,
            'ProductLink': link,
            'Price': price,
            'ImageUrl': image_url,
            'ProductInfo': info
        })


    # print(product_info)

    results = {}
    results['Title'] = title_list
    results['ProductLink'] = product_link_list
    results['Price'] = price_list
    results['ImageUrl'] = image_url_list
    results['ProductInfo'] = product_info


    # for k, v in results.items():
    #   print(f"{k} {v}")

    return render_template('zeelab.html', data=results)

@app.route('/truemeds')
def truemeds_data():
    title_list = []
    product_link_list = []
    price_list = []
    image_url_list = []

    url = "https://www.truemeds.in/categories/diabetes-care-3"

    webpage = requests.get(url).text
    soup = BeautifulSoup(webpage, 'html.parser')

    data_list = soup.find_all('div', class_='sc-13e5f603-1 dSxSDs')

    data_list = data_list[0]

    for product in data_list:
        image = product.find('img')
        image_url = image['src']
        image_url_list.append(image_url)

        prd = product.find('div', class_='sc-70f3a4c3-2 dgYGPC')

        #
        # print(prd)

        # Title
        title = prd.find('span', class_='sc-70f3a4c3-3 jvJzOr')
        title = title.text
        title_list.append(title)

        # Product link
        p = prd.find('a')
        product_link_list.append(p['href'])

        # Price
        price = prd.find('div', class_='sc-70f3a4c3-6 jYrCfO')
        price = price.find_all('span')
        price = price[1].text
        price_list.append(price)
        
        # Store data in MongoDB
        truemeds.insert_one({
            'Title': title,
            'Price': price,
            'ProductLink': p['href'],
            'ImageUrl': image['src']
        })

    results = {}

    results['Title'] = title_list
    results['Price'] = price_list
    results['ProductLink'] = product_link_list
    results['ImageUrl'] = image_url_list
    
    
    return render_template('truemeds.html', data=results)

# ---------------------------------------------------------------------------

@app.route('/netmeds-db')
def netmeds_data_db():
    # Fetch data from the 'netmeds' collection
    data_from_db = list(netmeds.find())

    # Render the data to the respective HTML page
    return render_template('netmeds_db.html', data=data_from_db)

@app.route('/zeelab-db')
def zeelab_data_db():
    # Fetch data from the 'zeeLab' collection
    data_from_db = list(zeeLab.find())

    # Render the data to the respective HTML page
    return render_template('zeelab_db.html', data=data_from_db)

@app.route('/truemeds-db')
def truemeds_data_db():
    # Fetch data from the 'zeeLab' collection
    data_from_db = list(truemeds.find())

    # Render the data to the respective HTML page
    return render_template('truemeds_db.html', data=data_from_db)

# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
