import re
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def parse_page(soup):
    all_result = []
    price_lst = []
    purchases_lst = []
    rating_lst = []
    title_lst = []
    #Цена
    price_elements = soup.find_all(class_='ds-text_color_price-term')
    for elements in price_elements:
        price_txt = elements.get_text(strip=True)
        clean_price = re.search(r'\d+', price_txt)
        if clean_price:
            result_price = clean_price.group()
            price_lst.append(result_price)

    #Покупки
    purchases_elements = soup.find_all(class_='ds-visuallyHidden')
    for p_elements in purchases_elements:
        purchases_txt = p_elements.get_text(strip=True)
        clean_purchases = re.search(r'(\d+)\s*купили', purchases_txt)
        if clean_purchases:
            purchases_result = clean_purchases.group(1)
            purchases_lst.append(purchases_result)


    #Рейтинг
    rating_elements = soup.find_all(class_='ds-visuallyHidden')
    for r_elements in rating_elements:
        rating_txt = r_elements.get_text(strip=True)
        clean_rating = re.search(r'([\d.]+)\s*из', rating_txt)
        if clean_rating:
            rating_result = clean_rating.group(1)
            rating_lst.append(rating_result)


    #Бренд
    brand_elements = soup.find_all('a', href=True)
    for brand in brand_elements:
        brand_link = brand.get('href')
        if '/card/' in brand_link:
            if not brand_link.startswith('https'):
                full_url = 'https://market.yandex.ru' + brand_link
            else:
                full_url = brand_link

            ua = UserAgent()
            headers = {'User-Agent': ua.random}
            try:
                parser_link = requests.get(full_url, headers=headers)
                parser_link.raise_for_status()
                soup_link = BeautifulSoup(parser_link.text, 'html.parser')
                title_brands = soup_link.find(string='Бренд')
                if title_brands:
                    next_element = title_brands.find_next()
                    while next_element and not next_element.get_text(strip=True):
                        next_element = next_element.find_next()
                    if next_element:
                        title_result = next_element.get_text(strip=True)
                        if title_result and not title_result.startswith('(window.'):
                            title_lst.append(title_result)
                        else:
                            title_lst.append('Бренд не указан')

            except requests.exceptions.RequestException as e:
                print(f'Ошибка {e}')
    for price, purchases, rating, title in zip(price_lst, purchases_lst, rating_lst, title_lst):
        items = {
            'price': price,
            'purchases': purchases,
            'rating': rating,
            'title': title
        }
        all_result.append(items)
    return all_result

















