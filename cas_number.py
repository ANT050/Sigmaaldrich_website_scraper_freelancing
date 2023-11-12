import requests


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


def get_product_data_without_price(url, headers, all_products):
    result_list = []
    count = 1
    for product_info in all_products:
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
        print(f'{count}. {result_dict}')
        count += 1
        result_list.append(result_dict)

    return result_list
