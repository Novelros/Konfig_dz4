import struct
import json
import sys
import argparse

# Описание команд
COMMANDS = {
    "LOAD_CONST": 0x01,
    "LOAD_MEM": 0x02,
    "STORE_MEM": 0x03,
    "GE_OP": 0x04,
    "ADD_OP": 0x05,
    "SUB_OP": 0x06,
}


def write_command(binary, opcode, *args):
    binary.write(struct.pack("B", opcode) + b''.join(struct.pack("<I", arg) for arg in args))


def assemble(input_path, output_path, log_path):
    try:
        with open(input_path, "r") as source, open(output_path, "wb") as binary, open(log_path, "w") as log:
            log_data = []
            for line in source:
                # Убираем пробелы по краям и игнорируем пустые строки и комментарии
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith('#'):
                    continue

                parts = stripped_line.split()
                cmd = parts[0]
                try:
                    if cmd not in COMMANDS:
                        print(f"Ошибка: неизвестная команда {cmd} в строке: {line}")
                        continue

                    opcode = COMMANDS[cmd]

                    if cmd == "LOAD_CONST":
                        if len(parts) < 3:
                            print(f"Ошибка: недостаточно аргументов для команды {cmd} в строке: {line}")
                            continue
                        const = int(parts[1])
                        reg = int(parts[2])
                        write_command(binary, opcode, const, reg)
                        log_data.append({"command": cmd, "opcode": opcode, "constant": const, "register": reg})

                    elif cmd == "LOAD_MEM":
                        if len(parts) < 3:
                            print(f"Ошибка: недостаточно аргументов для команды {cmd} в строке: {line}")
                            continue
                        addr = int(parts[1])
                        reg = int(parts[2])
                        write_command(binary, opcode, addr, reg)
                        log_data.append({"command": cmd, "opcode": opcode, "address": addr, "register": reg})

                    elif cmd == "STORE_MEM":
                        if len(parts) < 3:
                            print(f"Ошибка: недостаточно аргументов для команды {cmd} в строке: {line}")
                            continue
                        reg = int(parts[1])
                        addr = int(parts[2])
                        write_command(binary, opcode, reg, addr)
                        log_data.append({"command": cmd, "opcode": opcode, "register": reg, "address": addr})

                    elif cmd in {"GE_OP", "ADD_OP", "SUB_OP"}:
                        if len(parts) < 4:
                            print(f"Ошибка: недостаточно аргументов для команды {cmd} в строке: {line}")
                            continue
                        reg_a = int(parts[1])
                        reg_b = int(parts[2])
                        reg_result = int(parts[3])
                        write_command(binary, opcode, reg_a, reg_b, reg_result)
                        log_data.append({
                            "command": cmd,
                            "opcode": opcode,
                            "reg_a": reg_a,
                            "reg_b": reg_b,
                            "reg_result": reg_result
                        })

                except ValueError as e:
                    print(f"Ошибка при обработке строки: {line}. {str(e)}")

            json.dump(log_data, log, indent=4)

    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден - {e}")
    except PermissionError as e:
        print(f"Ошибка: недостаточно прав для доступа к файлу - {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ассемблер для работы с программами УВМ")
    parser.add_argument('--input', required=True, help="Путь к исходному файлу программы")
    parser.add_argument('--output', required=True, help="Путь к выходному бинарному файлу")
    parser.add_argument('--log', required=True, help="Путь к файлу для записи логов")

    args = parser.parse_args()

    assemble(args.input, args.output, args.log)