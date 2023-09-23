"""
Напишите следующие функции:
    Нахождение корней квадратного уравнения
    Генерация csv файла с тремя случайными числами в каждой строке. 100-1000 строк.
    Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла.
    Декоратор, сохраняющий переданные параметры и результаты работы функции в json файл.
"""
import csv
import json
import random
from math import sqrt
from typing import Callable


def coefficients_from_csv(func: Callable):
    def wrapper(coefficients_collection):
        result = []
        with open(coefficients_collection, mode='r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            for line in reader:
                a, b, c = map(float, line)
                result.append(func(a, b, c))
        return result

    return wrapper


def save_roots_in_json(func: Callable):
    counter = 1
    result = dict()

    def wrapper(*args):
        nonlocal counter, result
        coefficients = str(args)
        roots = str(func(*args))
        result[counter] = {'coefficients': coefficients, 'roots': roots}
        with open('roots.json', mode='w', encoding='UTF-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
            counter += 1
        return result

    return wrapper


def gen_coefficients_collection(quantity: int = 100, file_name: str = 'coefficients.csv'):
    coefficients_collections = []
    for _ in range(quantity):
        a = random.uniform(-quantity, quantity) if random.choice([True, False]) else random.randint(-quantity, quantity)
        if a == 0:
            a += random.random() + 0.1
        b = random.uniform(-quantity, quantity) if random.choice([True, False]) else random.randint(-quantity, quantity)
        c = random.uniform(-quantity, quantity) if random.choice([True, False]) else random.randint(-quantity, quantity)
        coefficients_collections.append([a, b, c])
    with open(file_name, mode='w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        for line in coefficients_collections:
            writer.writerow(line)
    return file_name


@coefficients_from_csv
@save_roots_in_json
def quadratic_equation(a: int | float, b: int | float, c: int | float):
    discriminant = b ** 2 - 4 * a * c
    if discriminant > 0:
        x1 = (-b + sqrt(discriminant)) / (2 * a)
        x2 = (-b - sqrt(discriminant)) / (2 * a)
        return x1, x2
    elif discriminant == 0:
        x = -b / (2 * a)
        return x
    else:
        return 'Корней нет'


quadratic_equation(gen_coefficients_collection())
