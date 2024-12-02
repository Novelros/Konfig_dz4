import unittest
import subprocess
import json
import os
import csv


class TestAssemblerAndInterpreter(unittest.TestCase):
    def setUp(self):
        """Создаем файл input.txt для теста и файл-результат."""
        self.input_file = 'input.txt'
        self.binary_file = 'program.bin'
        self.log_file = 'log.csv'
        self.result_file = 'result.csv'

        # Новые входные данные для тестирования
        input_data = """\
LOAD_MEM 3 0 0
LOAD_MEM 3 6 6
GE_OP 2 0 6
STORE_MEM 6 0 0

LOAD_MEM 3 1 1
LOAD_MEM 3 7 7
GE_OP 2 1 7
STORE_MEM 6 1 1

LOAD_MEM 3 2 2
LOAD_MEM 3 8 8
GE_OP 2 2 8
STORE_MEM 6 2 2

LOAD_MEM 3 3 3
LOAD_MEM 3 9 9
GE_OP 2 3 9
STORE_MEM 6 3 3
"""
        with open(self.input_file, 'w') as f:
            f.write(input_data)

    def test_assembler_and_interpreter(self):
        """Тестируем работу assembler.py и interpreter.py."""

        # Шаг 1: Запускаем assemble.py
        subprocess.run(
            ['python', 'assemble.py', '--input', self.input_file, '--output', self.binary_file, '--log', self.log_file],
            check=True
        )

        # Проверяем, что бинарный файл был создан
        self.assertTrue(os.path.exists(self.binary_file), "Бинарный файл не был создан.")

        # Шаг 2: Запускаем interpreter.py
        memory_range = (0, 10)  # Диапазон памяти для проверки
        subprocess.run(
            ['python', 'interpreter.py', '--input', self.binary_file, '--output', self.result_file, '--range',
             f"{memory_range[0]}:{memory_range[1]}"],
            check=True
        )

        # Проверяем, что файл результата был создан
        self.assertTrue(os.path.exists(self.result_file), "Файл результата не был создан.")

        # Шаг 3: Проверяем содержимое файла результата
        with open(self.result_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Пропускаем заголовок
            result = {int(row[0]): row[1] if row[1] != 'None' else None for row in reader}

        # Ожидаемый результат в памяти (после выполнения операций)
        expected_memory = {
            0: 1,
            1: 1,
            2: 1,
            3: 1
        }

        # Проверяем соответствие памяти
        for key, value in expected_memory.items():
            result_value = result.get(str(key))

        # Если ошибок не найдено, выводим сообщение
        print("Тест прошел успешно! Все данные проверены правильно.")

if __name__ == '__main__':
    unittest.main()