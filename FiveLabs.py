from decimal import Decimal, getcontext

getcontext().prec = 1000

FREQ_TABLE = [
    ('a', 0.0575), ('b', 0.0128), ('c', 0.0263), ('d', 0.0285),
    ('e', 0.0913), ('f', 0.0173), ('g', 0.0133), ('h', 0.0313),
    ('i', 0.0599), ('j', 0.0006), ('k', 0.0084), ('l', 0.0335),
    ('m', 0.0235), ('n', 0.0596), ('o', 0.0689), ('p', 0.0192),
    ('q', 0.0008), ('r', 0.0508), ('s', 0.0567), ('t', 0.0706),
    ('u', 0.0334), ('v', 0.0069), ('w', 0.0119), ('x', 0.0073),
    ('y', 0.0164), ('z', 0.0007), (' ', 0.1926)
]

def build_cumulative_table(freq_table):
    cumulative = {}
    low = Decimal(0)
    for char, prob in freq_table:
        high = low + Decimal(prob)
        cumulative[char] = {'low': low, 'high': high}
        low = high
    return cumulative

def encode(text, cumulative_table):
    low = Decimal(0)
    high = Decimal(1)

    for char in text:
        range_ = high - low
        high = low + range_ * cumulative_table[char]['high']
        low = low + range_ * cumulative_table[char]['low']

    return (low + high) / 2

def decode(code, cumulative_table, length):
    decoded_text = ''
    for _ in range(length):
        for char, bounds in cumulative_table.items():
            if bounds['low'] <= code < bounds['high']:
                decoded_text += char
                range_ = bounds['high'] - bounds['low']
                code = (code - bounds['low']) / range_
                break
    return decoded_text

if __name__ == "__main__":
    input_file = input("Введите имя исходного текстового файла: ")
    output_file = input("Введите имя файла для записи результата кодирования: ")

    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            text = infile.read().strip().lower()
    except FileNotFoundError:
        print(f"Файл '{input_file}' не найден. Убедитесь, что он существует.")
        exit()

    cumulative_table = build_cumulative_table(FREQ_TABLE)

    encoded_value = encode(text, cumulative_table)

    try:
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write(str(encoded_value))
        print(f"Текст успешно закодирован и сохранён в файл '{output_file}'.")
    except Exception as e:
        print(f"Произошла ошибка при записи файла '{output_file}': {e}")
        exit()

    decoded_text = decode(encoded_value, cumulative_table, len(text))
    print(f"Декодированный текст: {decoded_text}\n")

    if text == decoded_text:
        print("Декодированный текст совпадает с исходным.")
    else:
        print("Текст декодирован с ошибками.")
