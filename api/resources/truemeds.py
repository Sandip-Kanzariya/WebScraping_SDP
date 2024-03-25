from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource
import requests
from api.schemas.truemeds import TruemedsSchema
from extensions import db
from models.truemeds import Truemeds

# http://127.0.0.1:5050/product/truemeds/
class TruemedsList(Resource):
    
    def get(self):
        
        name_filter = request.args.get('name')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')


        truemeds_query = Truemeds.query

        if name_filter:
            truemeds_query = truemeds_query.filter(Truemeds.title.like(f'%{name_filter}%'))
        if min_price:
            truemeds_query = truemeds_query.filter(Truemeds.price >= min_price)   
        if max_price:
            truemeds_query = truemeds_query.filter(Truemeds.price <= max_price)

        truemeds_list = Truemeds.query.all()
        
        schema = TruemedsSchema(many=True) # For Reteriving multiple users many = True

        return {'results': schema.dump(truemeds_list)} # marshmallow serialize it to json
    
    def post(self):
        
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
            price = float(price)
            price_list.append(price)
            

            # Store data in SQLite
            product = Truemeds(
                title=title,
                price=price,
                product_link=p['href'],
                image_url=image['src']
            )
            db.session.add(product)
            db.session.commit()

        
        results = {'Title': title_list, 'Price': price_list, 'ProductLink': product_link_list,'ImageUrl': image_url_list}

        return {'data': results}
                