def key_exists(array_input, key: str) -> bool:
    try:
        _ = array_input[key]
        return True
    except KeyError:
        return False
