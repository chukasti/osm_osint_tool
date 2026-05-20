import requests
from urllib.parse import urlencode, quote, quote_plus
import socket
with open("payload.txt", "r", encoding='utf-8') as f:
    payload = f.read()
    urlencoded = quote(payload, safe="")


url = "https://overpass-api.de/api/interpreter"

#payload = "data=%5Bout%3Ajson%5D+%5Btimeout%3A25%5D%3B%0A+area(id%3A3600446114)+-%3E+.area_0%3B%0A(%0A++node%5B%22building%22%5D%5B%22website%22%5D(area.area_0)%3B%0A++way%5B%22building%22%5D%5B%22website%22%5D(area.area_0)%3B%0A++relation%5B%22building%22%5D%5B%22website%22%5D(area.area_0)%3B%0A)%3B%0A%0Aconvert+item+%3A%3A%3D%3A%3A%2C%0A++name+%3D+t%5B%22name%22%5D%2C%0A++website+%3D+t%5B%22website%22%5D%2C%0A++street+%3D+t%5B%22addr%3Astreet%22%5D%3B%0A%0Aout%3B"

socket.AF_INET, socket.AF_INET6 = socket.AF_INET6, socket.AF_INET6

our_headers = {
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


hood = input("введите район для поиска: ") # переделать на sys.argv

hood_payload = {"X-Requested-With": "overpass-turbo",
                "format": "json",
                "q": f"{hood}"}
hood_payload_encoded = urlencode(hood_payload)
hood_url = f"https://nominatim.openstreetmap.org/search?{hood_payload_encoded}"
def gain_hood_id():
    hood_response = requests.get(hood_url, headers=hood_headers)
    print(hood_response.url)
    oleg = hood_response.json()[0]["osm_id"]
    stepa = 3600000000 + int(oleg)
    # decompressed = gzip.decompress(hood_response.content)
    return stepa
    # return decompressed.decode("utf-8")

def make_request_to_api():
    response = requests.post(url, data={"data": payload}, headers=our_headers)
    return response.text
ivan = gain_hood_id()
print(ivan)
