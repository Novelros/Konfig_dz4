import struct
import json
import sys
import argparse

# Описание команд
COMMANDS = {
    "LOAD_CONST": 0x01,  # Загрузка константы в регистр
    "LOAD_MEM": 0x02,    # Загрузка значения из памяти в регистр
    "STORE_MEM": 0x03,   # Запись значения регистра в память
    "GE_OP": 0x04,       # Операция сравнения (>=)
    "ADD_OP": 0x05,      # Сложение
    "SUB_OP": 0x06,      # Вычитание
}

def assemble(input_path, output_path, log_path):
    with open(input_path, "r") as source, open(output_path, "wb") as binary, open(log_path, "w") as log:
        log_data = []
        for line in source:
            parts = line.strip().split()

            # Пропускаем пустые строки
            if not parts:
                continue

            cmd = parts[0]
            if cmd == "LOAD_CONST":
                if len(parts) < 3:
                    print(f"Ошибка: недостаточно аргументов для команды {cmd} в строке: {line}")
                    continue
                opcode = COMMANDS[cmd]
                const = int(parts[1])
                reg = int(parts[2])
                binary.write(struct.pack("B", opcode))
                binary.write(struct.pack("<i", const))  # Константа
                binary.write(struct.pack("<B", reg))   # Регистр
                log_data.append({"command": "LOAD_CONST", "opcode": opcode, "constant": const, "register": reg})
            elif cmd == "LOAD_MEM":
                if len(parts) < 3:
                    print(f"Ошибка: недостаточно аргументов для команды {cmd} в строке: {line}")
                    continue
                opcode = COMMANDS[cmd]
                addr = int(parts[1])
                reg = int(parts[2])
                binary.write(struct.pack("B", opcode))
                binary.write(struct.pack("<I", addr))  # Адрес памяти
                binary.write(struct.pack("<B", reg))   # Регистр
                log_data.append({"command": "LOAD_MEM", "opcode": opcode, "address": addr, "register": reg})
            elif cmd == "STORE_MEM":
                if len(parts) < 3:
                    print(f"Ошибка: недостаточно аргументов для команды {cmd} в строке: {line}")
                    continue
                opcode = COMMANDS[cmd]
                reg = int(parts[1])
                addr = int(parts[2])
                binary.write(struct.pack("B", opcode))
                binary.write(struct.pack("<B", reg))   # Регистр
                binary.write(struct.pack("<I", addr))  # Адрес памяти
                log_data.append({"command": "STORE_MEM", "opcode": opcode, "register": reg, "address": addr})
            elif cmd == "GE_OP":
                if len(parts) < 4:
                    print(f"Ошибка: недостаточно аргументов для команды {cmd} в строке: {line}")
                    continue
                opcode = COMMANDS[cmd]
                reg_a = int(parts[1])
                reg_b = int(parts[2])
                reg_result = int(parts[3])
                binary.write(struct.pack("B", opcode))
                binary.write(struct.pack("<B", reg_a))  # Регистр A
                binary.write(struct.pack("<B", reg_b))  # Регистр B
                binary.write(struct.pack("<B", reg_result))  # Регистр для результата
                log_data.append({"command": "GE_OP", "opcode": opcode, "reg_a": reg_a, "reg_b": reg_b, "reg_result": reg_result})
            elif cmd == "ADD_OP":
                if len(parts) < 4:
                    print(f"Ошибка: недостаточно аргументов для команды {cmd} в строке: {line}")
                    continue
                opcode = COMMANDS[cmd]
                reg_a = int(parts[1])
                reg_b = int(parts[2])
                reg_result = int(parts[3])
                binary.write(struct.pack("B", opcode))
                binary.write(struct.pack("<B", reg_a))  # Регистр A
                binary.write(struct.pack("<B", reg_b))  # Регистр B
                binary.write(struct.pack("<B", reg_result))  # Регистр для результата
                log_data.append({"command": "ADD_OP", "opcode": opcode, "reg_a": reg_a, "reg_b": reg_b, "reg_result": reg_result})
            elif cmd == "SUB_OP":
                if len(parts) < 4:
                    print(f"Ошибка: недостаточно аргументов для команды {cmd} в строке: {line}")
                    continue
                opcode = COMMANDS[cmd]
                reg_a = int(parts[1])
                reg_b = int(parts[2])
                reg_result = int(parts[3])
                binary.write(struct.pack("B", opcode))
                binary.write(struct.pack("<B", reg_a))  # Регистр A
                binary.write(struct.pack("<B", reg_b))  # Регистр B
                binary.write(struct.pack("<B", reg_result))  # Регистр для результата
                log_data.append({"command": "SUB_OP", "opcode": opcode, "reg_a": reg_a, "reg_b": reg_b, "reg_result": reg_result})

        # Записываем лог в JSON
        json.dump(log_data, log, indent=4)

if __name__ == "__main__":
    # Используем argparse для обработки аргументов командной строки
    parser = argparse.ArgumentParser(description="Ассемблер для работы с программами УВМ")
    parser.add_argument('--input', required=True, help="Путь к исходному файлу программы")
    parser.add_argument('--output', required=True, help="Путь к выходному бинарному файлу")
    parser.add_argument('--log', required=True, help="Путь к файлу для записи логов")

    args = parser.parse_args()

    assemble(args.input, args.output, args.log)