#!/usr/bin/env python3

import requests
from urllib.parse import quote
import socket
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
    urlencoded = quote(payload, safe="")


url = "https://overpass-api.de/api/interpreter"

socket.AF_INET, socket.AF_INET6 = socket.AF_INET6, socket.AF_INET6 # возможно не нужно, дело было в заголовке referer

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
    hood_response = requests.get(hood_url, headers=hood_headers, params=hood_payload)
    try:
        oleg = hood_response.json()[0]["osm_id"]
    except IndexError:
        print("Район не найден")
        exit(1)
    stepa = 3600000000 + int(oleg)
    # decompressed = gzip.decompress(hood_response.content)
    return stepa
    # return decompressed.decode("utf-8")

def parse_result(oleg: list):
    result2 = [
        {
            "name": e["tags"].get("name"),
            "website": e["tags"].get("website")
        }
        for e in oleg if "tags" in e
    ]
    return result2

def make_request_to_api():
    area_id = gain_hood_id()
    ready = payload.replace("3600000000", str(area_id))
    response = requests.post(url, data={"data": ready}, headers=main_headers)
    sanya = response.json()["elements"]
    return sanya


ivan = make_request_to_api()
parsed_result = parse_result(ivan)
now = datetime.now()
serialized_time = now.strftime("%Y-%m-%d_%H:%M:%S")
filename = f"{sys.argv[1].replace(', ', '_')}_{serialized_time}"
with open(filename, "w") as file:
    file.write(str(json.dumps(parsed_result, indent=2, ensure_ascii=False)))
print(f"Данные записаны в файл {filename}")