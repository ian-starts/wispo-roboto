def key_exists(array: [], key: str) -> bool:
    try:
        _ = array[key]
        return True
    except KeyError:
        return False
