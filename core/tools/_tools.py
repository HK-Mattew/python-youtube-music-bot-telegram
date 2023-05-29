import string


def remove_unnecessary_spaces_from_the_triple_string(string):
    string = string[1:-1].strip()
    number_of_spaces_after_slash_n = 0
    slash_n_detected = None

    for char in string.split(' '):
        if not char:
            number_of_spaces_after_slash_n += 1
        elif '\n' in char and not slash_n_detected:
            number_of_spaces_after_slash_n += 1
            slash_n_detected = True
        elif slash_n_detected:
            break

    string_formated = string.replace(('\n'+' '*number_of_spaces_after_slash_n), '\n')
    return string_formated



def remove_special_characters(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)

    special_chars = [
        char_ for char_ in string.punctuation
    ]
    new_text = ''
    for char in text:
        if char in special_chars:
            continue

        new_text += char

    return new_text