# Данная функция выполняет генерацию шк накладной, для правильного сканирования номера накладной на ТСД


def get_value_after_or(input_string):
    if 'OR' in input_string:
        parts = input_string.split('ORA-E')
        result = 'А-Е' + parts[1].strip()
        return result if len(parts) > 1 else None
    return None


def is_digit(char):
    return char.isdigit()


def replace_russian_chars(text):
    replacement_dict = {
        "а": "f", "б": "$f", "в": "d", "г": "u", "д": "l", "е": "t", "ё": "$t",
        "ж": "$p", "з": "p", "и": "b", "й": "q", "к": "r", "л": "k", "м": "v",
        "н": "y", "о": "j", "п": "g", "р": "h", "с": "c", "т": "n", "у": "e",
        "ф": "a", "х": "$w", "ц": "w", "ч": "x", "ш": "i", "щ": "o", "ь": "m",
        "ъ": "$m", "ы": "s", "э": "$a", "ю": "$y", "я": "z",
        "А": "F", "Б": "$F", "В": "D", "Г": "U", "Д": "L", "Е": "T", "Ё": "$T",
        "Ж": "$P", "З": "P", "И": "B", "Й": "Q", "К": "R", "Л": "K", "М": "V",
        "Н": "Y", "О": "J", "П": "G", "Р": "H", "С": "C", "Т": "N", "У": "E",
        "Ф": "A", "Х": "$W", "Ц": "W", "Ч": "X", "Ш": "I", "Щ": "O", "Ь": "M",
        "Ъ": "$M", "Ы": "S", "Э": "$A", "Ю": "$Y", "Я": "Z"
    }
    return ''.join(replacement_dict.get(c, c) for c in text)


def ascii_code(char):
    return str(ord(char))


def generate_barcode(doc_number, doc_sum):
    rounded_sum = int(doc_sum)
    data = f"{doc_number},{rounded_sum}"
    PREFIX_MY_ASSEMBLY = "999"
    PREFIX_DIGIT_SET = "0"
    PREFIX_NON_DIGIT_SET = "1"

    result = PREFIX_MY_ASSEMBLY

    length = len(data)
    i = 0

    while i < length:
        current_char = data[i]

        if is_digit(current_char):
            buffer = ""
            while i < length and is_digit(data[i]):
                buffer += data[i]
                i += 1
            buffer_length = len(buffer)
            result += PREFIX_DIGIT_SET + str(len(str(buffer_length))) + str(buffer_length) + buffer
        else:
            buffer = ""
            while i < length and not is_digit(data[i]):
                buffer += data[i]
                i += 1
            buffer = replace_russian_chars(buffer)
            buffer2 = "".join(ascii_code(c) for c in buffer)
            buffer2_length = len(buffer2)
            result += PREFIX_NON_DIGIT_SET + str(len(str(buffer2_length))) + str(buffer2_length) + buffer2

    return result


if __name__ == '__main__':
    # Пример использования функции
    document_number = "28ORA-E702267"
    document_sum = 11157.07
    doc_num = get_value_after_or(document_number)
    print(doc_num)
    barcode = generate_barcode(doc_num, document_sum)
    print(barcode)
