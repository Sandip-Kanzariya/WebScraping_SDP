from flask_restful import Resource
from bs4 import BeautifulSoup
import requests
from extensions import db
from models.netmeds import Netmeds

class ZeelabList(Resource):
    
    def get(self):
        
        return {'message': 'Hello, World!'}
    
    def post(self):
        pass        
