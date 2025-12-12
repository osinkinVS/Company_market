import pandas as pd
import requests
import csv
import time
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("CHECKO_API")

df = pd.read_csv("companies_1.csv", delimiter=";", encoding="utf-8-sig")
inn_list = df["inn"].dropna().tolist()


def get_checko_contacts(inn):
    url = f"https://api.checko.ru/v2/company?key={api_key}&inn={inn}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        data = response.json()

        if data.get("data"):
            company = data["data"]

            # КОНТАКТЫ
            contacts = company.get("Контакты", {})

            # ШТАТ (два варианта: новое поле СЧР за 2024 или старое employees)
            employees = company.get("СЧР", "")  # Новое поле 2024
            if not employees:
                employees = company.get("employees", "")

            return {
                "inn": inn,
                "name": company.get("НаимСокр", company.get("НаимПолн", "")),
                "phone": "; ".join(contacts.get("Тел", [])),
                "email": "; ".join(contacts.get("Емэйл", [])),
                "web": contacts.get("ВебСайт", ""),
                "employees": employees,
            }
    except Exception as e:
        print(f"Ошибка для ИНН {inn}: {e}")

    return None


results = []
for i, inn in enumerate(inn_list, 1):
    print(f"[{i}/{len(inn_list)}] ИНН: {inn}")

    data = get_checko_contacts(inn)

    if data:
        results.append(data)
        print(f"Найдено: {data['name'][:30]}...")
        print(f"Телефон: {data['phone'] or 'нет'}")
        print(f"Почта: {data['email'] or 'нет'}")
        print(f"Сайт: {data['web'] or 'нет'}")
        print(f"Штат: {data['employees'] or 'нет'}")
    else:
        print(f"Нет данных в Checko")

    time.sleep(1)

# Сохраняем в CSV
if results:
    with open("checko_contacts.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "inn", "phone", "email", "web", "employees"],
            delimiter=";",
        )
        writer.writeheader()
        writer.writerows(results)
