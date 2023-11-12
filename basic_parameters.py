import re
import requests


def get_basic_product_parameters(pages):
    basic_parameters = {
        "operationName": "CategoryProductSearch",
        "variables": {
            "searchTerm": None,
            "page": pages,
            "perPage": 20,
            "sort": "relevance",
            "selectedFacets": [
                {"key": "facet_web_product_area", "options": ["S176"]},
                {"key": "facet_web_special_grade", "options": ["pharmaceutical secondary standard"]}
            ],
            "facetSet": [
                "facet_product_category", "facet_feature", "facet_web_agency_method",
                "facet_web_anal_stand_form", "facet_web_special_grade", "facet_web_refmatl_rmtype",
                "facet_brand"
            ]
        },
        "query": """
            query CategoryProductSearch(
                $searchTerm: String,
                $page: Int!,
                $perPage: Int!,
                $sort: Sort,
                $selectedFacets: [FacetInput!],
                $facetSet: [String]
            ) {
                getProductSearchResults(
                    input: {
                        searchTerm: $searchTerm,
                        pagination: {page: $page, perPage: $perPage},
                        sort: $sort,
                        group: product,
                        facets: $selectedFacets,
                        facetSet: $facetSet
                    }
                ) {...CategoryProductSearchFields}
            }

            fragment CategoryProductSearchFields on ProductSearchResults {
                metadata {itemCount page perPage numPages}
                items {... on Product {...CategorySubstanceProductFields}}
                facets {key numToDisplay isHidden isCollapsed multiSelect prefix
                    options {value count}
                }
            }

            fragment CategorySubstanceProductFields on Product {
                name
                displaySellerName
                productNumber
                productKey
                isMarketplace
                marketplaceOfferId
                marketplaceSellerId
                attributes {key label values}
                brand {key erpKey name color}
                images {altText smallUrl mediumUrl largeUrl}
                description
                paMessage
            }
        """
    }

    return basic_parameters


def get_num_pages(url, headers, param_api):
    response = requests.post(url, headers=headers, json=param_api).json()
    num_pages = response.get("data", {}).get("getProductSearchResults", {}).get("metadata", {}).get("numPages")

    return num_pages


# Удаления HTML-тегов из текста
def __clean_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# Получение всех traceable продукта из JSON-ответа
def __get_all_traceable_values_product(attributes):
    traceable_values = []
    for attribute in attributes:
        if attribute.get("label") == "Agency":
            traceable_values = attribute.get("values", [])
    return traceable_values


# Получение номера traceable to USP продукта из JSON-ответа
def __get_traceable_to_usp_value_product(traceable_values):
    traceable_to_usp_value = ''
    for value in traceable_values:
        if value.startswith("traceable to USP"):
            match = re.search(r'\d+', value)
            if match:
                traceable_to_usp_value = match.group()
            break
    return traceable_to_usp_value


# Получение списка продуктов из JSON-ответа
def __fetch_product_list(url, headers, page):
    param_api = get_basic_product_parameters(page)
    response = requests.post(url, headers=headers, json=param_api).json()
    product_list = response.get("data", {}).get("getProductSearchResults", {}).get("items", [])
    return product_list


def get_main_product_fields(url, headers, pages=1):
    description_all_products = []
    count = 1
    for page in range(1, 2):
        list_products_on_page = __fetch_product_list(url, headers, page)

        for item in list_products_on_page:
            attributes = item.get("attributes", [])
            traceable_values = __get_all_traceable_values_product(attributes)
            traceable_to_usp_value = __get_traceable_to_usp_value_product(traceable_values)

            product_dict = {
                'Product No.': item.get("productNumber"),
                'Description': __clean_html_tags(item.get("name")),
                'USP Traceability': traceable_to_usp_value,
            }
            print(f'{count}. {product_dict}')
            count += 1
            description_all_products.append(product_dict)

    sorted_products = sorted(description_all_products, key=lambda x: (x['Product No.'], int(x['Product No.'][3:])))

    return sorted_products
