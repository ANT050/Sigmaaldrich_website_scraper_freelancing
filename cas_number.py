import requests
from common_settings import threaded_get_product_info


def __getting_cas_number(number):
    cas_number = {
        'operationName': 'PDP',
        'variables': {
            'brandKey': 'sial',
            'productKey': number,
            'catalogType': 'sial',
            'isMarketplaceCatalogEnabled': False,
        },
        'query': '''
            query PDP(
              $brandKey: String!,
              $productKey: String!,
              $catalogType: CatalogType,
              $orgId: String,
              $isMarketplaceCatalogEnabled: Boolean
            ) {
              getProductDetail(input: {
                brandKey: $brandKey,
                productKey: $productKey,
                catalogType: $catalogType,
                orgId: $orgId,
                isMarketplaceCatalogEnabled: $isMarketplaceCatalogEnabled
              }) {
                casNumber
                __typename
              }
            }
        '''
    }
    return cas_number


def get_cas_number(product_info, url, headers):
    product_number = product_info['Product No.']
    param_api = __getting_cas_number(product_number)
    response = requests.post(url, headers=headers, json=param_api).json()
    response_data = response['data']['getProductDetail']['casNumber']

    result_dict = {
        'Product No.': product_number,
        'Description': product_info['Description'],
        'USP Traceability': product_info['USP Traceability'],
        'CAS': response_data
    }

    return result_dict


def get_product_data_without_price(url, headers, all_products, number_threads):
    cas_numbers = threaded_get_product_info(url, headers, all_products, get_cas_number, number_threads)
    return cas_numbers
