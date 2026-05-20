#!/usr/bin/env python3

import requests
from urllib.parse import quote
import sys
from datetime import datetime
import json


try:
    hood = sys.argv[1]
except IndexError:
    print('Использование скрипта: python3 main.py ["название района"]')
    exit(0)


with open("payload.txt", "r", encoding='utf-8') as f:
    payload = f.read()


url = "https://overpass-api.de/api/interpreter"

main_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://overpass-turbo.eu",
    "Connection": "keep-alive",
    "Referer": "https://overpass-turbo.eu/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Pragma": "no-cache"
}


hood_headers = {
    "Host": "nominatim.openstreetmap.org",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "identity",
    "Origin": "https://overpass-turbo.eu",
    "Connection": "keep-alive",
    "Referer": "https://overpass-turbo.eu/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Priority": "u=0",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
                }




hood_payload = {"X-Requested-With": "overpass-turbo",
                "format": "json",
                "q": f"{hood}"}
hood_url = f"https://nominatim.openstreetmap.org/search"
def gain_hood_id():
    try:
        hood_response = requests.get(hood_url, headers=hood_headers, params=hood_payload, timeout=20)
        hood_response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Время ожидания ответа от сервиса openstreetmap вышло. Попробуйте запустить скрипт снова.")
        exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка ответа сервера: {e.response.status_code}")
        exit(1)
    except requests.exceptions.ConnectionError:
        print ("ошибка подключения")
        exit(1)


    try:
        oleg = hood_response.json()[0]["osm_id"]
    except IndexError:
        print("Район не найден")
        exit(1)
    stepa = 3600000000 + int(oleg)
    return stepa

def parse_result(oleg: list):
    result2 = [
        {k: v for k, v in {
            "name": e["tags"].get("name"),
            "website": e["tags"].get("website"),
            "phone": e["tags"].get("phone"),
            "email": e["tags"].get("email"),
            "addr:city": e["tags"].get("addr:city"),
            "addr:street": e["tags"].get("addr:street"),
            "addr:housenumber": e["tags"].get("addr:housenumber"),
            "addr:postcode": e["tags"].get("addr:postcode")
        }.items() if v is not None}
        for e in oleg if "tags" in e
    ]
    total = len(result2)

    with_website = sum(1 for e in result2 if e.get("website"))
    with_phone = sum(1 for e in result2 if e.get("phone"))
    with_email = sum(1 for e in result2 if e.get("email"))

    print(f"Всего объектов: {total}")
    print(f"С сайтом:       {with_website}")
    print(f"С телефоном:    {with_phone}")
    print(f"С email:        {with_email}")

    return result2

def make_request_to_api():
    area_id = gain_hood_id()
    ready = payload.replace("3600000000", str(area_id))
    try:
        response = requests.post(url, data={"data": ready}, headers=main_headers, timeout=40)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Время ожидания ответа от сервиса OSM вышло. Попробуйте запустить скрипт снова.")
        exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка ответа сервера: {e.response.status_code}")
        exit(1)
    except requests.exceptions.ConnectionError:
        print ("ошибка подключения")
        exit(1)
    sanya = response.json()["elements"]
    return sanya


ivan = make_request_to_api()
parsed_result = parse_result(ivan)
now = datetime.now()
serialized_time = now.strftime("%d-%m-%Y_%H-%M-%S")
filename = f"{sys.argv[1].replace(', ', '_')}_{serialized_time}"
with open(filename, "w") as file:
    file.write(str(json.dumps(parsed_result, indent=2, ensure_ascii=False)))
print(f"Данные записаны в файл {filename}")