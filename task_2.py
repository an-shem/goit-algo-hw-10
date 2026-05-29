"""
Завдання 2.
Обчислення визначеного інтеграла методом Монте-Карло.

Потрібно обчислити значення інтеграла функції методом Монте-Карло,
перевірити результат за допомогою scipy.integrate.quad та зробити висновки.

Для прикладу використано функцію f(x) = x^2 на відрізку [0, 2].
"""

import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad


def f(x):
    """Функція, інтеграл якої обчислюється."""
    return x ** 2


def monte_carlo_integral(func, a, b, num_points=100000, seed=42):
    """
    Обчислює визначений інтеграл методом Монте-Карло.

    Алгоритм:
    1. Створюється прямокутник, який містить область під графіком.
    2. Усередині прямокутника генеруються випадкові точки.
    3. Підраховується частка точок, які потрапили під графік.
    4. Площа прямокутника множиться на цю частку.

    Повертає наближене значення інтеграла.
    """
    random.seed(seed)

    x_values = np.linspace(a, b, 1000)
    y_max = max(func(x) for x in x_values)

    points_under_curve = 0

    for _ in range(num_points):
        x = random.uniform(a, b)
        y = random.uniform(0, y_max)

        if y <= func(x):
            points_under_curve += 1

    rectangle_area = (b - a) * y_max
    return rectangle_area * points_under_curve / num_points


def create_integration_plot(func, a, b, file_name="monte_carlo_integral.png"):
    """
    Створює графік функції та зафарбовує область інтегрування.
    """
    x = np.linspace(-0.5, 2.5, 400)
    y = func(x)

    fig, ax = plt.subplots()

    ax.plot(x, y, "r", linewidth=2)

    ix = np.linspace(a, b)
    iy = func(ix)
    ax.fill_between(ix, iy, color="gray", alpha=0.3)

    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axvline(x=a, color="gray", linestyle="--")
    ax.axvline(x=b, color="gray", linestyle="--")
    ax.set_title("Графік інтегрування f(x) = x^2 від 0 до 2")
    ax.grid()

    plt.savefig(file_name, dpi=120)
    plt.close()


def create_convergence_plot(samples, results, exact_value, file_name="monte_carlo_convergence.png"):
    """
    Створює графік збіжності методу Монте-Карло.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(samples, results, marker="o", label="Монте-Карло")
    plt.axhline(y=exact_value, linestyle="--", label="Точне значення")
    plt.xscale("log")
    plt.xlabel("Кількість випадкових точок")
    plt.ylabel("Значення інтеграла")
    plt.title("Збіжність методу Монте-Карло")
    plt.legend()
    plt.grid()
    plt.savefig(file_name, dpi=120)
    plt.close()


if __name__ == "__main__":
    a = 0
    b = 2

    quad_result, error = quad(f, a, b)
    analytical_result = (b ** 3 - a ** 3) / 3

    sample_sizes = [100, 1000, 10000, 100000]
    monte_carlo_results = []

    print(f"Результат scipy.integrate.quad: {quad_result}")
    print(f"Аналітичний результат: {analytical_result}")
    print(f"Оцінка абсолютної помилки quad: {error}")

    print("\nМетод Монте-Карло:")
    print(f"{'Кількість точок':>18} | {'Результат':>14} | {'Похибка':>14}")
    print("-" * 54)

    for num_points in sample_sizes:
        result = monte_carlo_integral(f, a, b, num_points=num_points, seed=42)
        monte_carlo_results.append(result)
        absolute_error = abs(result - quad_result)

        print(f"{num_points:>18} | {result:>14.8f} | {absolute_error:>14.8f}")

    print("\nВисновок:")
    print(
        "Метод Монте-Карло дає наближене значення інтеграла. "
        "Результат близький до значення, отриманого за допомогою "
        "scipy.integrate.quad та аналітичного обчислення. "
        "Зі збільшенням кількості випадкових точок точність зазвичай покращується, "
        "але через випадковий характер методу результат може трохи коливатися."
    )

    create_integration_plot(f, a, b)
    create_convergence_plot(sample_sizes, monte_carlo_results, quad_result)

    print("\nГрафіки збережено у файлах:")
    print("- monte_carlo_integral.png")
    print("- monte_carlo_convergence.png")
