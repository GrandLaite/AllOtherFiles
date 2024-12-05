import numpy as np

def calculate_hamming_code(data_byte):
    hamming_code = ['0'] * 12
    data_bits = format(data_byte, '08b')
    data_index = 0

    # Заполняем битами данных на позиции, не являющиеся степенями двойки
    for i in range(12):
        if i + 1 not in [1, 2, 4, 8]:  
            hamming_code[i] = data_bits[data_index]
            data_index += 1

    # Вычисляем биты чётности
    for parity_pos in [1, 2, 4, 8]:
        count = 0
        for i in range(parity_pos - 1, 12, 2 * parity_pos):
            count += sum(1 for j in range(i, min(i + parity_pos, 12)) if hamming_code[j] == '1')
        hamming_code[parity_pos - 1] = '1' if count % 2 != 0 else '0'

    # Добавляем бит общей чётности
    overall_parity = '1' if sum(int(bit) for bit in hamming_code) % 2 != 0 else '0'
    hamming_code.append(overall_parity)
    return ''.join(hamming_code)

def text_to_hamming(input_file, hamming_file):
    try:
        with open(input_file, 'rb') as f:
            content = f.read()

        with open(hamming_file, 'w') as f_hamming:
            for byte in content:
                hamming_code = calculate_hamming_code(byte)
                f_hamming.write(hamming_code + '\n')
        
        print(f"Текст успешно преобразован в код Хэмминга и сохранён в файл '{hamming_file}'.")
    except FileNotFoundError:
        print(f"Файл '{input_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def correct_hamming_code(hamming_code):
    hamming_code_np = np.array(list(hamming_code[:-1]), dtype=int)
    overall_parity_bit = int(hamming_code[-1])

    # Определение позиции ошибки по контрольным битам
    error_pos = 0
    for parity_pos in [1, 2, 4, 8]:
        count = 0
        for i in range(parity_pos - 1, 12, 2 * parity_pos):
            count += np.sum(hamming_code_np[i:min(i + parity_pos, 12)] == 1)
        if count % 2 != 0:
            error_pos += parity_pos

    # Проверка на бит общей чётности (13-й бит)
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

def hamming_to_text(hamming_file, restored_file):
    try:
        with open(hamming_file, 'r') as f_hamming:
            hamming_data = f_hamming.readlines()
        
        decoded_bytes = []
        corrected_hamming_data = []
        line_number = 1
        errors_found = False

        for line in hamming_data:
            hamming_code = line.strip()
            
            if len(hamming_code) != 13:
                print(f"Ошибка в длине кодовой строки буквы {line_number}: {hamming_code}")
                corrected_hamming_data.append(hamming_code)  # Сохраняем как есть
                line_number += 1
                continue
            
            corrected_code, status = correct_hamming_code(hamming_code)

            if status != 'без ошибок':
                errors_found = True
                print(f"Буква {line_number}: {status}")

            corrected_hamming_data.append(corrected_code)

            # Извлекаем данные из исправленного кода Хэмминга
            if "исправлена" in status or status == "без ошибок":
                data_bits = ''.join(corrected_code[i] for i in range(12) if i + 1 not in [1, 2, 4, 8])
                decoded_byte = int(data_bits, 2)
                decoded_bytes.append(decoded_byte)

            line_number += 1

        if not errors_found:
            print("В файле ошибок нет.")

        # Сохраняем исправленные коды Хэмминга обратно в файл
        with open(hamming_file, 'w') as f_hamming:
            f_hamming.write('\n'.join(corrected_hamming_data) + '\n')

        # Сохраняем восстановленный текст
        with open(restored_file, 'wb') as f_out:
            f_out.write(bytearray(decoded_bytes))
        
        print(f"Восстановление текста завершено. Файл сохранён как '{restored_file}'.")
    except FileNotFoundError:
        print(f"Файл '{hamming_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def main_loop():
    input_file = input("Введите название исходного файла: ")
    hamming_file = input("Введите название файла для записи кода Хэмминга: ")
    restored_file = input("Введите название файла для сохранения восстановленного текста: ")

    text_to_hamming(input_file, hamming_file)
    
    input(f"Внесите ошибку в файл '{hamming_file}' и нажмите Enter для продолжения...")
    
    hamming_to_text(hamming_file, restored_file)

if __name__ == '__main__':
    main_loop()
