from flask import Flask, render_template
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import csv

app = Flask(__name__)

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

    results = {'Title': title_list, 'Price': price_list, 'Url': image_url_list}

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


    # print(product_info)

    results = {}
    results['Title'] = title_list
    results['Product Link'] = product_link_list
    results['Product Price'] = price_list
    results['Image Url'] = image_url_list
    results['Product Info'] = product_info


    # for k, v in results.items():
    #   print(f"{k} {v}")

    # Your data
    data = results

    return render_template('zeelab.html', data=results)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
