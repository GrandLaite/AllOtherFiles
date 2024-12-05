import reedsolo

def initialize_reed_solomon():
    """Инициализация кодировщика Рида-Соломона."""
    rs = reedsolo.RSCodec(4)  # Кратно 2
    return rs


def bytes_to_bits(byte_data):
    """Преобразует байтовую строку в строку бит."""
    return ''.join(format(byte, '08b') for byte in byte_data)


def bits_to_bytes(bit_data):
    """Преобразует строку бит в байты."""
    if len(bit_data) % 8 != 0:
        raise ValueError(f"Длина битовой строки {len(bit_data)} не кратна 8: {bit_data}")
    return bytes(int(bit_data[i:i + 8], 2) for i in range(0, len(bit_data), 8))


def encode_reed_solomon(input_file, rs_file, rs_codec):
    """Кодирует данные Рида-Соломона и записывает в файл."""
    try:
        with open(input_file, 'rb') as f:
            content = f.read()

        with open(rs_file, 'w') as f_rs:
            for byte in content:
                # Кодируем каждый байт
                encoded_data = rs_codec.encode(bytes([byte]))
                # Преобразуем закодированные данные в битовый формат
                encoded_bits = bytes_to_bits(encoded_data)
                f_rs.write(encoded_bits + '\n')

        print(f"Данные закодированы и сохранены в файл: {rs_file}")
    except FileNotFoundError:
        print(f"Файл '{input_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def decode_reed_solomon(rs_file, output_file, rs_codec):
    """Декодирует данные Рида-Соломона из файла."""
    try:
        with open(rs_file, 'r') as f_rs:
            encoded_lines = f_rs.readlines()

        decoded_bytes = []
        error_summary = []

        for index, line in enumerate(encoded_lines, 1):
            encoded_bits = line.strip()
            try:
                # Преобразуем битовую строку обратно в байты
                encoded_data = bits_to_bytes(encoded_bits)
                # Декодируем данные
                corrected_data = rs_codec.decode(encoded_data)
                decoded_byte = corrected_data[0]
                errors_detected = corrected_data[2]  # Количество исправленных ошибок
                decoded_bytes.append(decoded_byte[0])
                error_summary.append(f"[{index}] Исправлено ошибок: {errors_detected}")
            except reedsolo.ReedSolomonError:
                error_summary.append(f"[{index}] Ошибка декодирования")

        # Сохраняем декодированные байты
        with open(output_file, 'wb') as f_out:
            f_out.write(bytes(decoded_bytes))

        print(f"Восстановленные данные сохранены в файл: {output_file}")
        for item in error_summary:
            print(item)
    except FileNotFoundError:
        print(f"Файл '{rs_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def main():
    input_file = input("Введите путь к исходному файлу: ")
    rs_file = input("Введите путь для сохранения закодированного файла: ")
    restored_file = input("Введите путь для сохранения восстановленного файла: ")

    rs_codec = initialize_reed_solomon()

    encode_reed_solomon(input_file, rs_file, rs_codec)

    input("Внесите ошибки в закодированный файл и нажмите Enter для продолжения...")

    decode_reed_solomon(rs_file, restored_file, rs_codec)

if __name__ == '__main__':
    main()
