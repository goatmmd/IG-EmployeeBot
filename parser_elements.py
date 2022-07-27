def parse_web_elements(elements: iter) -> list:
    account_list = list()

    for elem in elements:
        account_list.append(
            elem.text.split('\n')[0]
        )

    return account_list
