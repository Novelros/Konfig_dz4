import unittest
import subprocess
import csv
import os


class TestVectorAddition(unittest.TestCase):
    def setUp(self):
        # Создаем текстовую программу
        self.assembly_code = """\
#LOAD_CONST 4 1 0
STORE_MEM 6 0 0
LOAD_CONST 4 2 1
STORE_MEM 6 1 1
LOAD_CONST 4 3 2
STORE_MEM 6 2 2
LOAD_CONST 4 4 3
STORE_MEM 6 3 3
LOAD_CONST 4 5 4
STORE_MEM 6 4 4
LOAD_CONST 4 6 5
STORE_MEM 6 5 5

LOAD_CONST 4 10 6
STORE_MEM 6 6 6
LOAD_CONST 4 20 7
STORE_MEM 6 7 7
LOAD_CONST 4 30 8
STORE_MEM 6 8 8
LOAD_CONST 4 11 9
STORE_MEM 6 9 9
LOAD_CONST 4 12 10
STORE_MEM 6 10 10
LOAD_CONST 4 10 11
STORE_MEM 6 11 11

LOAD_MEM 3 0 0
LOAD_MEM 3 6 6
ADD_OP 2 0 6
STORE_MEM 6 0 0
LOAD_MEM 3 1 1
LOAD_MEM 3 7 7
ADD_OP 2 1 7
STORE_MEM 6 1 1
LOAD_MEM 3 2 2
LOAD_MEM 3 8 8
ADD_OP 2 2 8
STORE_MEM 6 2 2
LOAD_MEM 3 3 3
LOAD_MEM 3 9 9
ADD_OP 2 3 9
STORE_MEM 6 3 3
LOAD_MEM 3 4 4
LOAD_MEM 3 10 10
ADD_OP 2 4 10
STORE_MEM 6 4 4
LOAD_MEM 3 5 5
LOAD_MEM 3 11 11
ADD_OP 2 5 11
STORE_MEM 6 5 5
"""
        self.program_file = "vector_addition.txt"
        self.binary_file = "vector_addition.bin"
        self.log_file = "vector_addition_log.csv"
        self.output_file = "vector_result.csv"

        # Записываем векторную программу в файл
        with open(self.program_file, "w") as f:
            f.write(self.assembly_code)

    def test_vector_addition(self):
        # Ассемблируем (вместо subprocess вызываем функцию сборщика)
        try:
            self.assemble_program()
        except subprocess.CalledProcessError as e:
            self.fail(f"Assembly failed with error: {e}")

        # Интерпретируем (вместо subprocess вызываем интерпретатор)
        try:
            self.run_interpreter()
        except subprocess.CalledProcessError as e:
            self.fail(f"Interpretation failed with error: {e}")

        # Проверяем результаты
        with open(self.output_file, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Пропускаем заголовок
            results = [int(row[1]) for row in reader]

        expected = [11, 22, 33, 44, 55, 66]  # Ожидаемый результат сложения
        self.assertEqual(results, expected)

    def assemble_program(self):
        # Проверка на существование файла assemble.py
        if not os.path.exists("assemble.py"):
            raise FileNotFoundError("assemble.py not found in the current directory.")

        # Запуск процесса сборки
        result = subprocess.run([
            "python", "assemble.py",
            "--input", self.program_file,
            "--output", self.binary_file,
            "--log", self.log_file
        ], check=True, capture_output=True, text=True)

        # Выводим stdout и stderr для диагностики ошибок
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

    def run_interpreter(self):
        # Проверка на существование файла interpreter.py
        if not os.path.exists("interpreter.py"):
            raise FileNotFoundError("interpreter.py not found in the current directory.")

        # Запуск интерпретатора
        result = subprocess.run([
            "python", "interpreter.py",
            "--input", self.binary_file,
            "--output", self.output_file,
            "--range", "0:40"
        ], check=True, capture_output=True, text=True)

        # Выводим stdout и stderr для диагностики ошибок
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

    # def tearDown(self):
    #     # Удаляем временные файлы
    #     for file in [self.program_file, self.binary_file, self.log_file, self.output_file]:
    #         if os.path.exists(file):
    #             os.remove(file)


if __name__ == "__main__":
    unittest.main()