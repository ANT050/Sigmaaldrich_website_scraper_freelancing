import requests


def get_product_parameters(pages):
    parameters = {
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

    return parameters


def get_headers():
    headers = {
        'authority': 'www.sigmaaldrich.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'x-gql-access-token': 'ee91d871-7e90-11ee-ab08-e33b69fb32b8',
        'x-gql-country': 'ES',
        'x-gql-language': 'en'
    }

    return headers


def get_num_pages(page=1):
    param_api = get_product_parameters(page)
    url = 'https://www.sigmaaldrich.com/api'
    headers = get_headers()

    response = requests.post(url, headers=headers, json=param_api).json()
    num_pages = response.get("data", {}).get("getProductSearchResults", {}).get("metadata", {}).get("numPages")

    return num_pages
