import json
import requests
import pandas as pd
from common_settings import get_headers
from basic_parameters import get_basic_product_parameters, get_num_pages, get_main_product_fields
from additional_api_parameters import get_additional_product_parameters
from cas_number import get_product_data_without_price
from common_settings import threaded_get_product_info


def get_product_data(product_info, url, headers):
    product_number = product_info['Product No.']

    param_api = get_additional_product_parameters(product_number)
    response = requests.post(url, headers=headers, json=param_api).json()

    if 'data' in response and response['data'] is not None:
        response_data = response['data']['getPricingForProduct'].get('materialPricing', [])
    else:
        response_data = response['errors']

    result_list = []
    for pricing_info in response_data:
        result_dict = {
            'Product No.': product_number,
            'Description': product_info['Description'],
            'CAS': product_info['CAS'],
            'Package Size': pricing_info.get("packageSize", ""),
            'Price (Euro)': f'{pricing_info.get("currency", "")} {pricing_info.get("listPrice", "")}',
            'USP Traceability': product_info['USP Traceability']
        }

        result_list.append(result_dict)

    return result_list


def get_all_product_data(url, headers, all_products, number_threads):
    pricing_info = threaded_get_product_info(url, headers, all_products, get_product_data, number_threads)
    return pricing_info


def sorted_list_products(products):
    sorted_list = [item for product in products for item in product]

    sorted_products = sorted(sorted_list, key=lambda x: x['Product No.'])

    return sorted_products


def write_to_csv(data, filename) -> None:
    df = pd.DataFrame(data)
    df.columns = [
        'Product No.',
        'Description',
        'CAS',
        'Package Size',
        'Price (Euro)',
        'USP Traceability'
    ]
    df.to_csv(filename, index=False)


def write_to_json(data, filename) -> None:
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def main():
    url = 'https://www.sigmaaldrich.com/api'
    headers = get_headers()
    number_threads = 13

    product_basic_parameters_api = get_basic_product_parameters(pages=1)
    number_pages = get_num_pages(url, headers, product_basic_parameters_api)

    all_products = get_main_product_fields(url, headers, number_pages)
    all_products_with_price = get_product_data_without_price(url, headers, all_products, number_threads)
    all_product_data = get_all_product_data(url, headers, all_products_with_price, number_threads)
    sorted_products = sorted_list_products(all_product_data)

    write_to_csv(sorted_products, 'product_data.csv')
    write_to_json(sorted_products, 'product_data.json')


if __name__ == '__main__':
    main()
