import os
from dotenv import load_dotenv
import csv
import pandas as pd
from dadata import Dadata

load_dotenv()

api_key = os.getenv("API_KEY")
secret = os.getenv("SECRET_KEY")

dadata = Dadata(api_key, secret)

df = pd.read_excel("Company.xlsx", sheet_name="Sheet2")
companies = df["name"].dropna().str.strip().tolist()
print(f"Найдено {len(companies)} компаний в файле")

with open("companies_1.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["original_name", "found_name", "inn", "okved"])

    found_count = 0
    for i, company in enumerate(companies, 1):
        try:
            print(f"[{i}/{len(companies)}] Ищем: {company}")

            # Простой поиск
            result = dadata.suggest("party", company, count=1)

            if result and result[0]["data"].get("inn"):
                found_name = result[0]["value"]
                inn = result[0]["data"]["inn"]
                okved = result[0]["data"].get("okved", "")

                writer.writerow([company, found_name, inn, okved])
                found_count += 1
                print(f"Найдено: {found_name}")
            else:
                print(f"Не найдено")

        except Exception as e:
            print(f"Ошибка: {str(e)[:50]}")

print(f"\nИТОГО: Найдено {found_count} из {len(companies)} компаний")


"""query = "4 Пикселя"
result = dadata.suggest("party", query, count=1)
if result:
    company_data = result[0]
    print(f"Найденная организация: {company_data['value']}")
    print(f"ИНН: {company_data['data']['inn']}")
    print(f"Основной ОКВЭД: {company_data['data']['okved']}")
else:
    print("Организация не найдена.")"""
