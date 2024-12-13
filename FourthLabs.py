import reedsolo

def initialize_reed_solomon():
    rs = reedsolo.RSCodec(4)
    return rs

def bytes_to_bits(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)

def bits_to_bytes(bit_data):
    if len(bit_data) % 8 != 0:
        raise ValueError(f"Длина битовой строки {len(bit_data)} не кратна 8: {bit_data}")
    return bytes(int(bit_data[i:i + 8], 2) for i in range(0, len(bit_data), 8))

def encode_reed_solomon(input_file, rs_file, rs_codec):
    try:
        with open(input_file, 'rb') as f:
            content = f.read()

        with open(rs_file, 'w') as f_rs:
            for byte in content:
                encoded_data = rs_codec.encode(bytes([byte]))
                encoded_bits = bytes_to_bits(encoded_data)
                f_rs.write(encoded_bits + '\n')

        print(f"Данные записаны в файл: {rs_file}")
    except FileNotFoundError:
        print(f"Файл '{input_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def decode_reed_solomon(rs_file, rs_codec):
    try:
        with open(rs_file, 'r') as f_rs:
            encoded_lines = f_rs.readlines()

        decoded_bytes = []
        summary = []

        for index, line in enumerate(encoded_lines, 1):
            encoded_bits = line.strip()
            try:
                encoded_data = bits_to_bytes(encoded_bits)
                corrected_data = rs_codec.decode(encoded_data)
                decoded_byte = corrected_data[0]
                errors_detected = corrected_data[2]
                decoded_bytes.extend(list(decoded_byte))
                summary.append(f"[{index}] Исправлено ошибок: {errors_detected}")
            except reedsolo.ReedSolomonError as e:
                summary.append(f"[{index}] Ошибка декодирования")

        output_file = input("Введите имя файла с восстановленным текстом: ")

        with open(output_file, 'wb') as f_out:
            f_out.write(bytes(decoded_bytes))


        for item in summary:
            print(item)
        print(f"Восстановленные данные сохранены в файл: {output_file}")
    except FileNotFoundError:
        print(f"Файл '{rs_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def main():
    input_file = input("Введите имя исходного текстового файла: ")
    rs_file = input("Введите имя промежуточного файла (бинарного): ")

    rs_codec = initialize_reed_solomon()

    encode_reed_solomon(input_file, rs_file, rs_codec)

    input(f"Внесите ошибку в файл {rs_file}, затем нажмите Enter, чтобы продолжить...")

    decode_reed_solomon(rs_file, rs_codec)

    print("Завершение работы программы.")

if __name__ == '__main__':
    main()
