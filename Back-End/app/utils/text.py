def clean_entity(text: str, start: int, end: int):
    value = text[start:end]

    if "\n" in value:
        value = value.split("\n", 1)[0]

    left = len(value) - len(value.lstrip())
    right = len(value.rstrip())

    start += left
    end = start + right

    value = text[start:end]
    

    return value, start, end