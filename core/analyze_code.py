import os
import ast
from core.raw_stats import compute_raw_metrics
from core.complexity import compute_complexity
from core.halstead import compute_halstead
from core.oop_metrics import compute_oop_metrics
from core.design_metrics import analyze_design_metrics
from core.utils import path_to_module

# Аналіз одного Python-файлу: обчислення метрик складності, OOP, архітектури тощо
def analyze_code(file_path, all_sources=None, root_path=None):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
    except UnicodeDecodeError:
        return None  # Пропустити файл, якщо він не читається як UTF-8

    tree = ast.parse(code)

    # Обчислення базових метрик
    raw_metrics = compute_raw_metrics(code)
    cyclomatic_data, wmc = compute_complexity(code)
    halstead_data = compute_halstead(tree)
    oop_data = compute_oop_metrics(tree)

    # Отримання модульного імені для подальшого аналізу зв’язків
    module_name = path_to_module(file_path, root_path or os.getcwd())

    # Архітектурні метрики: імпорти, абстрактність, стабільність, відстань
    design_data = analyze_design_metrics(
        module_name,
        tree,
        all_sources or {},
        root_path or os.getcwd()
    )

    # Формування результату аналізу
    result = {
        'filename': os.path.basename(file_path),
        'module_name': module_name,
        'loc': raw_metrics['loc'],
        'lloc': raw_metrics['lloc'],
        'comments': raw_metrics['comments'],
        'comment_ratio': raw_metrics['comment_ratio'],
        'function_count': len(cyclomatic_data),
        'class_count': oop_data['class_count'],
        'cyclomatic_complexity': cyclomatic_data,
        'mi': raw_metrics['mi'],
        'halstead': halstead_data,
        'rfc': oop_data['rfc'],
        'wmc': wmc,
        'dit': oop_data['dit'],
        'lcom': oop_data['lcom'],
        'noc': oop_data['noc'],
        'cbo': oop_data['cbo'],
        'is_oop': oop_data['class_count'] > 0,
        'ca': design_data['ca'],
        'ce': design_data['ce'],
        'abstractness': design_data['abstractness'],
        'instability': design_data['instability'],
        'distance': design_data['distance'],
        'imports': design_data.get('imports', [])
    }

    return result
