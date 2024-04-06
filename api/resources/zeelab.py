from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from bs4 import BeautifulSoup
import requests
from api.schemas.zeelab import ZeelabSchema
from auth.decorators import auth_role
from extensions import db
from models.netmeds import Netmeds
from models.zeelab import Zeelab

# http://127.0.0.1:5050/product/zeelab/
# http://127.0.0.1:5050/product/zeelab?category=bone-joints
class ZeelabList(Resource):
    
    def get(self):

        name_filter = request.args.get('name') 
        content_filter = request.args.get('q') 
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')


        zeelab_query = Zeelab.query

        if name_filter:
            zeelab_query = zeelab_query.filter(Zeelab.title.like(f'%{name_filter}%'))
        if content_filter:
            zeelab_query = zeelab_query.filter(Zeelab.product_info.like(f'%{content_filter}%'))
        if min_price:
            zeelab_query = zeelab_query.filter(Zeelab.price >= min_price)   
        if max_price:
            zeelab_query = zeelab_query.filter(Zeelab.price <= max_price)

        zeelab_list = zeelab_query.all()
        schema = ZeelabSchema(many=True) # For Reteriving multiple users many = True

        return {"results" : schema.dump(zeelab_list)} # marshmallow serialize it to json
        
    @jwt_required()
    @auth_role("admin")
    def post(self):

        category = request.args.get('category', 'bone-joints')  # Default is 'bone-joints'
        url = f"https://zeelabpharmacy.com/health/{category}"
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
            price = price.text.strip()    # Removing spaces before and after the string
            price = price[1:]             # Removing '₹' symbol
            price = price.strip()         # Removing spaces before and after the string
            price = float(price)
            price_list.append(price)

            # For Image URL
            image = product.find_all('img','productOuterImage')
            image = image[0]
            image_url = image['src']; # image_url = image['data-original']; # print(image_url)
            image_url_list.append(image_url)
            

            # Store data in SQLite
            product = Zeelab(
                title=name,
                price=price,
                product_link=link,
                image_url=image_url,
                product_info=info
            )

            db.session.add(product)
            db.session.commit()

        results = {'Title': title_list, 'Price': price_list, 'ProductLink': product_link_list,'ImageUrl': image_url_list, 'ProductInfo': product_info}

        # Create a new list to store objects
        new_list = []

        # Iterate through the lists simultaneously and create objects
        for title, price, product_link, image_url, product_info in zip(results['Title'], results['Price'], results['ProductLink'], results['ImageUrl'], results['ProductInfo']):
            new_object = {
                'Title': title,
                'Price': price,
                'ProductLink': product_link,
                'ImageUrl': image_url,
                'ProductInfo': product_info
            }
            new_list.append(new_object)

        return {'data': new_list}
    
