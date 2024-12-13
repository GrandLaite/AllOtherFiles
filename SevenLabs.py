import sys

def compress(uncompressed):
    """Функция для сжатия строки с использованием алгоритма LZW"""
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])
    return result

def decompress(compressed):
    from io import StringIO

    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}

    result = StringIO()

    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError("Некорректный сжатый код: %s" % k)
        result.write(entry)

        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result.getvalue()

def read_file_as_string(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return None

def write_compressed_file(filename, compressed):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            compressed_str = ' '.join(map(str, compressed))
            f.write(compressed_str)
        print(f"Сжатые данные записаны в файл {filename}")
    except IOError:
        print(f"Ошибка при записи в файл {filename}.")

def read_compressed_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            compressed_str = f.read()
            compressed = list(map(int, compressed_str.strip().split()))
            return compressed
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return None
    except ValueError:
        print(f"Файл {filename} содержит некорректные данные.")
        return None

def write_decompressed_file(filename, decompressed):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(decompressed)
        print(f"Распакованные данные записаны в файл {filename}")
    except IOError:
        print(f"Ошибка при записи в файл {filename}.")

def main():
    while True:
        print("\nВыберите действие:")
        print("1. Сжать")
        print("2. Распаковать")
        print("3. Выход")
        choice = input("Введите номер действия (1/2/3): ").strip()

        if choice == '1':
            input_file = input("Введите имя файла для сжатия: ").strip()
            output_file = input("Введите имя файла для сохранения сжатых данных: ").strip()
            data = read_file_as_string(input_file)
            if data is not None:
                compressed = compress(data)
                write_compressed_file(output_file, compressed)

        elif choice == '2':
            input_file = input("Введите имя файла для распаковки: ").strip()
            output_file = input("Введите имя файла для сохранения распакованных данных: ").strip()
            compressed = read_compressed_file(input_file)
            if compressed is not None:
                try:
                    decompressed = decompress(compressed)
                    write_decompressed_file(output_file, decompressed)
                except ValueError as e:
                    print(f"Ошибка при распаковке: {e}")

        elif choice == '3':
            print("Выход из программы.")
            sys.exit(0)
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
