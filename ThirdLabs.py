import numpy as np

def calculate_hamming_code(data_byte):
    hamming_code = ['0'] * 12
    data_bits = format(data_byte, '08b')
    data_index = 0

    for i in range(12):
        if i + 1 not in [1, 2, 4, 8]:  
            hamming_code[i] = data_bits[data_index]
            data_index += 1

    for parity_pos in [1, 2, 4, 8]:
        count = 0
        for i in range(parity_pos - 1, 12, 2 * parity_pos):
            count += sum(1 for j in range(i, min(i + parity_pos, 12)) if hamming_code[j] == '1')
        hamming_code[parity_pos - 1] = '1' if count % 2 != 0 else '0'

    overall_parity = '1' if sum(int(bit) for bit in hamming_code) % 2 != 0 else '0'
    hamming_code.append(overall_parity)
    return ''.join(hamming_code)

def text_to_hamming():
    input_file = input("Введите имя исходного текстового файла: ")
    while True:
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read().encode('utf-8')
            break
        except FileNotFoundError:
            input_file = input(f"Файл '{input_file}' не найден. Введите имя исходного текстового файла заново: ")

    hamming_file = input("Введите имя промежуточного файла (бинарного): ")
    try:
        with open(hamming_file, 'w') as f_hamming:
            for byte in content:
                hamming_code = calculate_hamming_code(byte)
                f_hamming.write(hamming_code + '\n')
        print("Запись с кодом Хэмминга завершена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return hamming_file

def correct_hamming_code(hamming_code):
    hamming_code_np = np.array(list(hamming_code[:-1]), dtype=int)
    overall_parity_bit = int(hamming_code[-1])

    error_pos = 0
    for parity_pos in [1, 2, 4, 8]:
        count = 0
        for i in range(parity_pos - 1, 12, 2 * parity_pos):
            count += np.sum(hamming_code_np[i:min(i + parity_pos, 12)] == 1)
        if count % 2 != 0:
            error_pos += parity_pos

    total_parity_check = (np.sum(hamming_code_np) + overall_parity_bit) % 2 == 0

    if error_pos > 0:
        if total_parity_check:
            return ''.join(hamming_code), 'двойная ошибка'
        else:
            hamming_code_np[error_pos - 1] ^= 1
            return ''.join(hamming_code_np.astype(str)) + str(overall_parity_bit), f'исправлена, позиция {error_pos}'
    elif not total_parity_check:
        overall_parity_bit ^= 1
        return ''.join(hamming_code_np.astype(str)) + str(overall_parity_bit), 'исправлена, позиция 13'

    return ''.join(hamming_code), 'без ошибок'

def hamming_to_text(hamming_file):
    output_file = input("Введите имя файла с восстановленным текстом: ")
    try:
        with open(hamming_file, 'r') as f_hamming:
            hamming_data = f_hamming.readlines()

        decoded_bytes = []
        line_number = 1
        
        for line in hamming_data:
            hamming_code = line.strip()
            
            if len(hamming_code) != 13:
                print(f"Неверная длина кодовой таблицы в букве {line_number}: {hamming_code}")
                line_number += 1
                continue
            
            corrected_code, status = correct_hamming_code(hamming_code)

            if status != 'без ошибок':
                print(f"Буква {line_number}: {status}")

            try:
                data_bits = ''.join(corrected_code[i] for i in range(12) if i + 1 not in [1, 2, 4, 8])
                decoded_byte = int(data_bits, 2)
                decoded_bytes.append(decoded_byte)
            except ValueError:
                print(f"Ошибка декодирования буквы {line_number}. Символ заменён на '?'.")
                decoded_bytes.append(ord('?'))

            line_number += 1

        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(bytearray(decoded_bytes).decode('utf-8', errors='replace'))
        print("Восстановление текста с кодом Хэмминга завершено.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def main_loop():
    while True:
        hamming_file = text_to_hamming()
        
        input("Внесите ошибку в файл, затем нажмите Enter, чтобы продолжить...")
        
        hamming_to_text(hamming_file)

        exit_choice = input("Хотите продолжить? (y/n): ").strip().lower()
        if exit_choice != 'y':
            print("Завершение работы программы.")
            break


if __name__ == '__main__':
    main_loop()
