from flask_restful import Resource
from bs4 import BeautifulSoup
import requests
from extensions import db
from models.netmeds import Netmeds


class NetmedsList(Resource):
    
    def get(self):
        
        return {'message': 'Hello, World!'}
    
    def post(self):
        
        title_list = []
        price_list = []
        image_url_list = []
        product_link_list = []

        for i in range(1, 3):
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
                    price = price.text.strip()  # Removing spaces before and after the string
                    price = price[1:]           # Removing '₹' symbol
                    price = price.strip()       # Removing spaces before and after the string
                    price = float(price)

                    # Take Imgae URL
                    image = item.find_all('span', class_="cat-img")
                    image = image[0].find_all('img', class_="product-image-photo")
                    image = image[0]
                    image_url_list.append(image['src'])

                    # Take Title
                    item = item.find_all('a', class_="category_name")
                    item = item[0]

                    # Take Product Link
                    product_link_list.append(item['href'])

                    title = item.find_all('span', class_="clsgetname")
                    title_list.append(title[0].text)
                    price_list.append(price)
                    
                    # Store data in SQLite
                    product = Netmeds(
                        title=title[0].text,
                        price=price,
                        product_link=item['href'],
                        image_url=image['src']
                    )
                    db.session.add(product)
                    db.session.commit()

        results = {'Title': title_list, 'Price': price_list, 'ProductLink': product_link_list,'ImageUrl': image_url_list}

        return {'data': results}