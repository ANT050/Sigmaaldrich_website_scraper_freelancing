import requests
import re
from api_params import get_data_pages, get_headers


def get_num_pages(settings):
    num_pages = settings.get("data", {}).get("getProductSearchResults", {}).get("metadata", {}).get("numPages")

    return num_pages


def get_all_traceable_values_product(attributes):
    traceable_values = []
    for attribute in attributes:
        if attribute.get("label") == "Agency":
            traceable_values = attribute.get("values", [])
    return traceable_values


def get_traceable_to_usp_value_product(traceable_values):
    traceable_to_usp_value = ''
    for value in traceable_values:
        if value.startswith("traceable to USP"):
            match = re.search(r'\d+', value)
            if match:
                traceable_to_usp_value = match.group()
            break
    return traceable_to_usp_value


def get_product_values(url, headers):
    param_api = get_data_pages()
    response = requests.post(url, headers=headers, json=param_api).json()

    items = response.get("data", {}).get("getProductSearchResults", {}).get("items", [])
    description_all_products = []

    for item in items:
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

    # number_pages = get_num_pages(response)
    all_products = get_product_values(url, headers)

    for i in all_products:
        print(i)


if __name__ == '__main__':
    main()
