from radon.complexity import cc_visit
from radon.visitors import Function

# Обчислення цикломатичної складності коду
def compute_complexity(code):
    # Отримання списку об'єктів з оцінками складності
    complexity_scores = cc_visit(code)

    # Витягуємо тільки функції/методи та їх характеристики
    cyclomatic_data = [
        {
            "name": obj.name,
            "complexity": obj.complexity,
            "lineno": obj.lineno,
            "type": type(obj).__name__
        }
        for obj in complexity_scores if isinstance(obj, Function)
    ]

    # WMC (Weighted Method Count) — сумарна складність усіх функцій
    wmc = sum(item["complexity"] for item in cyclomatic_data)

    return cyclomatic_data, wmc
