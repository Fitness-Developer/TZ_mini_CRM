"""
utils.py
- choose_operator: Выбор активного оператора для источника на основе весов и текущей нагрузки.
"""

import random
from .models import SourceOperatorWeight, Contact


def choose_operator(session, source_id):
    """
    Выбирает оператора для данного источника на основе весов и текущей нагрузки.

    Логика:
    1. Получаем все назначения операторов для источника.
    2. Отбираем только активных операторов, у которых текущая нагрузка меньше load_limit.
    3. Выбираем оператора случайным образом с учётом весов.

    Возвращает:
    - Объект Operator, если найден подходящий оператор
    - None, если подходящего оператора нет
    """
    # Получаем все назначения операторов для источника
    assignments = session.query(SourceOperatorWeight).filter_by(source_id=source_id).all()
    if not assignments:
        return None

    # Отбираем доступных операторов
    available = []
    for assignment in assignments:
        operator = assignment.operator
        if operator.active:
            # Проверяем текущую нагрузку оператора
            current_load = session.query(Contact).filter(Contact.operator_id == operator.id).count()
            if current_load < operator.load_limit:
                available.append(assignment)

    if not available:
        return None

    # Составляем список весов для случайного выбора
    weights = [a.weight for a in available]

    # Выбираем одного оператора случайно с учётом весов
    chosen_assignment = random.choices(available, weights=weights, k=1)[0]
    return chosen_assignment.operator