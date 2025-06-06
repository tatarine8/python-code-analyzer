import ast
import math

# Обчислює Halstead метрики для дерева розбору Python-коду
def compute_halstead(tree):
    operators = set()   # Унікальні оператори (типи вузлів)
    operands = set()    # Унікальні операнди (імена, значення)
    N1 = N2 = 0         # Загальна кількість операторів і операндів

    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.Return, ast.If, ast.For, ast.While, ast.Call, ast.Import, ast.AugAssign, ast.Expr)):
            operators.add(type(node).__name__)
            N1 += 1
        elif isinstance(node, (ast.Name, ast.Constant)):
            val = getattr(node, 'id', None) or getattr(node, 'value', None)
            if val is not None:
                operands.add(str(val))
                N2 += 1

    h1, h2 = len(operators), len(operands)
    vocabulary = h1 + h2
    length = N1 + N2
    calculated_length = round((h1 * math.log2(h1) + h2 * math.log2(h2)), 2) if h1 and h2 else 0
    volume = round(length * math.log2(vocabulary), 2) if vocabulary else 0
    difficulty = round((h1 / 2) * (N2 / h2), 2) if h2 else 0
    effort = round(volume * difficulty, 2)
    time = round(effort / 18, 2)  # середній час реалізації (в секундах)
    bugs = round(volume / 3000, 3)  # емпірична оцінка дефектів

    return {
        'vocabulary': vocabulary,
        'length': length,
        'calculated_length': calculated_length,
        'volume': volume,
        'difficulty': difficulty,
        'effort': effort,
        'time': time,
        'bugs': bugs
    }
