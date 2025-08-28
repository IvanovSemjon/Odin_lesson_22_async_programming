import requests
import time


def get_site(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except:
        print(f"Ошибка запроса {url}")



sites = [
    "https://python.org",
    "https://github.com",
    "https://stackoverflow.com"
    ]


start = time.time()

for site in sites:
    print(f"Запрос на {site}")
    r = get_site(site)
    print(r)

end = time.time()  

print(f"Синхронное время выполнения: {end - start:.1f} секунд")

