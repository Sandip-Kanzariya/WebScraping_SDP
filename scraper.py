from flask import Flask, render_template
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import csv

app = Flask(__name__)

@app.route('/')
def index():
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

    return render_template('index.html', data=results)

if __name__ == '__main__':
    app.run(debug=True)
