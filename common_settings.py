import concurrent.futures


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


def threaded_get_product_info(url, headers, all_products, info_function, number_threads):
    result_list = []
    count = 1

    with concurrent.futures.ThreadPoolExecutor(number_threads) as executor:
        futures = [executor.submit(info_function, product_info, url, headers) for product_info in all_products]

        for future in concurrent.futures.as_completed(futures):
            result_data = future.result()
            print(f'{count}. {result_data}')
            count += 1
            result_list.append(result_data)

    return result_list
