"""
Завдання 1.
Оптимізація видачі решти покупцеві.

Реалізовано дві функції:
1. find_coins_greedy(amount) — жадібний алгоритм.
2. find_min_coins(amount) — динамічне програмування.

Набір монет: [50, 25, 10, 5, 2, 1].
"""

import timeit


COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount):
    """
    Повертає словник із кількістю монет кожного номіналу,
    які використовуються для формування заданої суми.

    Алгоритм є жадібним: спочатку вибираються найбільші доступні
    номінали монет.

    Наприклад:
        find_coins_greedy(113) -> {50: 2, 10: 1, 2: 1, 1: 1}
    """
    if amount < 0:
        raise ValueError("Сума не може бути від'ємною")

    result = {}

    for coin in COINS:
        count = amount // coin

        if count > 0:
            result[coin] = count
            amount -= coin * count

    return result


def find_min_coins(amount):
    """
    Повертає словник із кількістю монет кожного номіналу,
    які потрібні для формування заданої суми мінімальною кількістю монет.

    Використовується метод динамічного програмування.
    Для кожної суми від 1 до amount зберігається мінімальна кількість монет,
    необхідна для її формування.

    Наприклад:
        find_min_coins(113) -> {1: 1, 2: 1, 10: 1, 50: 2}
    """
    if amount < 0:
        raise ValueError("Сума не може бути від'ємною")

    min_coins = [0] + [float("inf")] * amount
    last_coin = [0] * (amount + 1)

    for current_amount in range(1, amount + 1):
        for coin in COINS:
            if coin <= current_amount:
                previous_amount = current_amount - coin
                candidate = min_coins[previous_amount] + 1

                if candidate < min_coins[current_amount]:
                    min_coins[current_amount] = candidate
                    last_coin[current_amount] = coin

    result = {}
    current_amount = amount

    while current_amount > 0:
        coin = last_coin[current_amount]
        result[coin] = result.get(coin, 0) + 1
        current_amount -= coin

    return result


def measure_average_time(func, amount, number=100):
    """
    Вимірює середній час виконання функції.

    timeit запускає функцію кілька разів, а потім ми ділимо
    загальний час на кількість запусків.
    """
    total_time = timeit.timeit(lambda: func(amount), number=number)
    return total_time / number


if __name__ == "__main__":
    example_amount = 113

    print(f"Приклад для суми {example_amount}:")
    print("Жадібний алгоритм:", find_coins_greedy(example_amount))
    print("Динамічне програмування:", find_min_coins(example_amount))

    print("\nПорівняння часу виконання:")
    print(f"{'Сума':>10} | {'Greedy, сек':>14} | {'DP, сек':>14}")
    print("-" * 46)

    for amount in [113, 1000, 10000, 100000]:
        greedy_time = measure_average_time(find_coins_greedy, amount, number=1000)
        dp_time = measure_average_time(find_min_coins, amount, number=10)

        print(f"{amount:>10} | {greedy_time:>14.8f} | {dp_time:>14.8f}")
