def group_list_dict(data: list[dict], key: str) -> list | dict:
    unique_key = unique_key_value(data, key)
    if len(unique_key) <= 1:
        return data

    result = dict()
    for k in unique_key:
        result[k] = list(filter(lambda item: item[key] == k, data))

    return result


def unique_key_value(data: list[dict], key: str) -> list:
    unique = set(item[key] for item in data)
    return list(unique)
