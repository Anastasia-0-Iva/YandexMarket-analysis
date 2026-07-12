import requests
from fake_useragent import UserAgent
import time
from bs4 import BeautifulSoup
from parser import parse_page
import pandas as pd

def data():
    url = 'https://market.yandex.ru/search?text=автомобильный%20фильтр&hid=6101352&hid=90449&hid=13477846&hid=90442&hid=90443&rs=eJwz8qxi5Xix6QvTJ0Z1DgaBhYdYJRgUQHyFi4dYFa6d38amcArIOH2IVaNz0wdWDSDjLyMDEPQygcipYHIFE0gHAB2WGgE%2C&rt=9'
    ua = UserAgent()

    headers = {'User-Agent': ua.random}

    all_data = []
    for page in range(1, 100):
        response = requests.get(f'{url}&page={page}', headers=headers)
        try:
            response.raise_for_status()
            time.sleep(15)
            soup = BeautifulSoup(response.text, 'html.parser')
            res = parse_page(soup)
            if res:
                all_data.extend(res)
            print(f'Страница {page}: {len(res)} товаров')
            time.sleep(10)

        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                print('Страницы закончились')
                break
            else:
                print('Ошибка {e}')
    return all_data

if __name__ == '__main__':
    products  = data()
    df = pd.DataFrame(products)
    df.to_excel('Yandex.xlsx', index=False)
    print(f'Собрано {len(products)} карточек товаров')
