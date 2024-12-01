import struct
import csv
import sys
import argparse

MEMORY_SIZE = 1024
REGISTER_COUNT = 32  # Количество регистров


class VirtualMachine:
    def __init__(self):
        self.memory = [0] * MEMORY_SIZE
        self.registers = [0] * REGISTER_COUNT
        self.accumulator = 0

    def validate_register(self, reg):
        """Проверка, что индекс регистра в допустимом диапазоне"""
        if reg < 0 or reg >= REGISTER_COUNT:
            raise IndexError(f"Invalid register index: {reg}. Register index must be between 0 and {REGISTER_COUNT - 1}.")

    def validate_memory(self, addr):
        """Проверка, что адрес памяти в допустимом диапазоне"""
        if addr < 0 or addr >= MEMORY_SIZE:
            raise IndexError(f"Invalid memory address: {addr}. Memory address must be between 0 and {MEMORY_SIZE - 1}.")

    def validate_memory_range(self, start, end):
        """Проверка диапазона памяти"""
        if start < 0 or start >= MEMORY_SIZE or end < 0 or end >= MEMORY_SIZE or start > end:
            raise ValueError(f"Invalid memory range: {start}:{end}. Range must be within 0 to {MEMORY_SIZE - 1}.")

    def load_const(self, const, reg):
        """Загружает константу в аккумулятор и сохраняет в указанный регистр"""
        self.validate_register(reg)
        self.accumulator = const
        self.registers[reg] = self.accumulator

    def load_mem(self, addr, reg):
        """Загружает данные из памяти в аккумулятор и сохраняет в регистр"""
        self.validate_memory(addr)
        self.validate_register(reg)
        self.accumulator = self.memory[addr]
        self.registers[reg] = self.accumulator

    def store_mem(self, reg, addr):
        """Сохраняет данные из аккумулятора в память по адресу"""
        self.validate_register(reg)
        self.validate_memory(addr)
        self.memory[addr] = self.registers[reg]

    def ge_op(self, reg_a, reg_b, reg_result):
        """Операция сравнения"""
        self.validate_register(reg_a)
        self.validate_register(reg_b)
        self.validate_register(reg_result)
        self.registers[reg_result] = 1 if self.registers[reg_a] >= self.registers[reg_b] else 0

    def add_op(self, reg_a, reg_b, reg_result):
        """Операция сложения"""
        self.validate_register(reg_a)
        self.validate_register(reg_b)
        self.validate_register(reg_result)
        self.registers[reg_result] = self.registers[reg_a] + self.registers[reg_b]

    def sub_op(self, reg_a, reg_b, reg_result):
        """Операция вычитания"""
        self.validate_register(reg_a)
        self.validate_register(reg_b)
        self.validate_register(reg_result)
        self.registers[reg_result] = self.registers[reg_a] - self.registers[reg_b]

    def execute(self, program_path, result_path, mem_range):
        # Проверяем диапазон памяти
        start, end = map(int, mem_range.split(':'))
        self.validate_memory_range(start, end)

        with open(program_path, "rb") as binary, open(result_path, "w", newline='') as result:
            writer = csv.writer(result)
            writer.writerow(["memory_address", "memory_value", "registers", "accumulator"])

            while byte := binary.read(1):
                opcode = struct.unpack("B", byte)[0]
                if opcode == 0x01:  # LOAD_CONST
                    const = struct.unpack("<i", binary.read(4))[0]  # Константа
                    reg = struct.unpack("<B", binary.read(1))[0]  # Регистр
                    self.load_const(const, reg)
                elif opcode == 0x02:  # LOAD_MEM
                    addr = struct.unpack("<I", binary.read(4))[0]  # Адрес памяти
                    reg = struct.unpack("<B", binary.read(1))[0]  # Регистр
                    self.load_mem(addr, reg)
                elif opcode == 0x03:  # STORE_MEM
                    reg = struct.unpack("<B", binary.read(1))[0]  # Регистр
                    addr = struct.unpack("<I", binary.read(4))[0]  # Адрес памяти
                    self.store_mem(reg, addr)
                elif opcode == 0x04:  # GE_OP
                    reg_a = struct.unpack("<B", binary.read(1))[0]
                    reg_b = struct.unpack("<B", binary.read(1))[0]
                    reg_result = struct.unpack("<B", binary.read(1))[0]
                    self.ge_op(reg_a, reg_b, reg_result)
                elif opcode == 0x05:  # ADD_OP
                    reg_a = struct.unpack("<B", binary.read(1))[0]
                    reg_b = struct.unpack("<B", binary.read(1))[0]
                    reg_result = struct.unpack("<B", binary.read(1))[0]
                    self.add_op(reg_a, reg_b, reg_result)
                elif opcode == 0x06:  # SUB_OP
                    reg_a = struct.unpack("<B", binary.read(1))[0]
                    reg_b = struct.unpack("<B", binary.read(1))[0]
                    reg_result = struct.unpack("<B", binary.read(1))[0]
                    self.sub_op(reg_a, reg_b, reg_result)

                # Записываем обновленное состояние
                for addr in range(start, end + 1):
                    writer.writerow([addr, self.memory[addr], self.registers[:10], self.accumulator])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter for virtual machine")
    parser.add_argument("--input", required=True, help="Path to the input binary file")
    parser.add_argument("--output", required=True, help="Path to save the output CSV file")
    parser.add_argument("--range", required=True, help="Memory range to display, in the format start:end")

    args = parser.parse_args()

    vm = VirtualMachine()
    vm.execute(args.input, args.output, args.range)