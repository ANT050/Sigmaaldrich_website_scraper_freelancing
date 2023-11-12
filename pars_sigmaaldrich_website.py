import json
import requests
import pandas as pd
from request_headers import get_headers
from basic_parameters import get_basic_product_parameters, get_num_pages, get_main_product_fields
from additional_api_parameters import get_additional_product_parameters
from cas_number import get_product_data_without_price


def get_all_product_data(url, headers, all_products):
    result_list = []
    count = 1
    for product in all_products:
        product_number = product['Product No.']

        param_api = get_additional_product_parameters(product_number)
        response = requests.post(url, headers=headers, json=param_api).json()

        # Проверяем, есть ли данные в ответе
        if 'data' in response and response['data'] is not None:
            response_data = response['data']['getPricingForProduct'].get('materialPricing', [])
        else:
            response_data = response['errors']

        for pricing_info in response_data:
            result_dict = {
                'Product No.': product_number,
                'Description': product.get('Description'),
                'CAS': product.get('CAS'),
                'Package Size': pricing_info.get("packageSize"),
                'Price (Euro)': f'{pricing_info.get("currency")} {pricing_info.get("listPrice")}',
                'USP Traceability': product.get('USP Traceability')
            }
            print(f'{count}. {result_dict}')
            count += 1
            result_list.append(result_dict)

    return result_list


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

    product_basic_parameters_api = get_basic_product_parameters(pages=1)
    number_pages = get_num_pages(url, headers, product_basic_parameters_api)

    all_products = get_main_product_fields(url, headers, number_pages)
    all_products_with_price = get_product_data_without_price(url, headers, all_products)
    all_product_data = get_all_product_data(url, headers, all_products_with_price)

    write_to_excel(all_product_data, 'product_data.csv')
    write_to_json(all_product_data, 'product_data.json')


if __name__ == '__main__':
    main()
