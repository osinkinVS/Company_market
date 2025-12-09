import os
from dotenv import load_dotenv
import csv

load_dotenv()

api_key = os.getenv('API_KEY')
secret = os.getenv('SECRET_KEY')

from dadata import Dadata

dadata = Dadata(api_key, secret)








'''query = "4 Пикселя"
result = dadata.suggest("party", query, count=1)
if result:
    company_data = result[0]
    print(f"Найденная организация: {company_data['value']}")
    print(f"ИНН: {company_data['data']['inn']}")
    print(f"Основной ОКВЭД: {company_data['data']['okved']}")
else:
    print("Организация не найдена.")'''