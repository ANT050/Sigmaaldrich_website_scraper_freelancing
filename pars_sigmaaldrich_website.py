import requests
import re
from api_params import get_product_parameters, get_headers, get_num_pages


# Получение всех traceable продукта из JSON-ответа
def get_all_traceable_values_product(attributes):
    traceable_values = []
    for attribute in attributes:
        if attribute.get("label") == "Agency":
            traceable_values = attribute.get("values", [])
    return traceable_values


# Получение номера traceable to USP продукта из JSON-ответа
def get_traceable_to_usp_value_product(traceable_values):
    traceable_to_usp_value = ''
    for value in traceable_values:
        if value.startswith("traceable to USP"):
            match = re.search(r'\d+', value)
            if match:
                traceable_to_usp_value = match.group()
            break
    return traceable_to_usp_value


# Получение списка продуктов из JSON-ответа
def fetch_product_list(url, headers, page):
    param_api = get_product_parameters(page)
    response = requests.post(url, headers=headers, json=param_api).json()
    product_list = response.get("data", {}).get("getProductSearchResults", {}).get("items", [])
    return product_list


# Получение полей продукта Product No., Description, USP
def get_fields_of_all_products(url, headers, pages):
    description_all_products = []

    for page in range(1, pages + 1):
        list_products_on_page = fetch_product_list(url, headers, page)

        for item in list_products_on_page:
            attributes = item.get("attributes", [])
            traceable_values = get_all_traceable_values_product(attributes)
            traceable_to_usp_value = get_traceable_to_usp_value_product(traceable_values)

            product_dict = {
                'Product No.': item.get("productNumber"),
                'Description': item.get("name"),
                'USP Traceability': traceable_to_usp_value,
            }
            description_all_products.append(product_dict)

    return description_all_products


def main():
    url = 'https://www.sigmaaldrich.com/api'
    headers = get_headers()
    number_pages = get_num_pages(page=1)
    all_products = get_fields_of_all_products(url, headers, number_pages)

    count = 1
    for i in all_products:
        print(f'{count}. {i}')
        count += 1


if __name__ == '__main__':
    main()
