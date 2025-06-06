import os
from core.analyze_code import analyze_code
from core.utils import path_to_module

def analyze_project(folder_path):
    results = []             # Список з результатами аналізу кожного модуля
    all_sources = {}         # Вміст усіх модулів у форматі {module_name: code}
    module_paths = {}        # Шляхи до кожного модуля у форматі {module_name: path}

    # Обхід директорій для пошуку валідних Python-файлів
    for root, dirs, files in os.walk(folder_path):
        # Фільтрація службових папок
        dirs[:] = [d for d in dirs if d.lower() not in ('venv', '.venv', 'env', '__pycache__', '.git')]
        for file in files:
            # Вибір тільки звичайних .py файлів (без службових, тестових тощо)
            if (
                file.endswith('.py')
                and not file.startswith(('test_', 'setup'))
                and file not in ('__init__.py', '__main__.py')
            ):
                path = os.path.abspath(os.path.join(root, file))
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        module_name = path_to_module(path, folder_path)
                        all_sources[module_name] = f.read()
                        module_paths[module_name] = path
                except Exception:
                    continue  # Ігнорування файлів з помилками читання

    # Ініціалізація агрегаторів для всіх метрик
    total = {k: 0 for k in [
        'loc', 'lloc', 'comments', 'function_count', 'class_count',
        'mi_sum', 'mi_count', 'comment_ratio_sum',
        'rfc', 'wmc', 'dit', 'lcom_sum', 'lcom_count', 'noc', 'cbo',
        'ca', 'ce', 'abstractness_sum', 'instability_sum', 'distance_sum', 'design_count'
    ]}
    total['cyclomatic_complexity'] = []

    # Окрема агрегація метрик Halstead
    halstead_fields = ["vocabulary", "length", "calculated_length", "volume", "difficulty", "effort", "time", "bugs"]
    halstead_total = {k: 0 for k in halstead_fields}
    halstead_count = 0

    oop_files = 0  # Кількість файлів, які містять об'єктно-орієнтовану структуру

    # Аналіз кожного знайденого модуля
    for module_name, path in module_paths.items():
        result = analyze_code(path, all_sources=all_sources, root_path=folder_path)
        if result is None:
            continue

        if result['is_oop']:
            oop_files += 1

        results.append(result)

        # Агрегація метрик у загальні лічильники
        for key in total:
            if key in result:
                total[key] += result[key]

        total['mi_sum'] += result['mi']
        total['mi_count'] += 1
        total['comment_ratio_sum'] += result['comment_ratio']
        total['cyclomatic_complexity'].extend(result['cyclomatic_complexity'])
        total['lcom_sum'] += result['lcom']
        total['lcom_count'] += 1

        # Обробка Halstead-метрик, якщо вони наявні
        if 'halstead' in result and result['halstead'].get('vocabulary', 0) > 0:
            for k in halstead_fields:
                halstead_total[k] += result['halstead'][k]
            halstead_count += 1

        # Обробка архітектурних метрик, якщо вони наявні
        if 'abstractness' in result:
            total['abstractness_sum'] += result['abstractness']
            total['instability_sum'] += result['instability']
            total['distance_sum'] += result['distance']
            total['design_count'] += 1

    # Побудова списку імен модулів
    module_names = {r['module_name'] for r in results}

    # Побудова графа залежностей між модулями
    edges = []
    edges_set = set()
    for source in results:
        source_module = source['module_name']
        source_imports = source.get('imports', [])
        for imp in source_imports:
            for target in module_names:
                if target == source_module:
                    continue
                if target == imp or target.startswith(imp + '.') or imp.startswith(target + '.'):
                    edge = (source_module, target)
                    if edge not in edges_set:
                        edges.append({"from": source_module, "to": target})
                        edges_set.add(edge)

    # Формування фінального словника з усіма метриками та структурою проєкту
    project_summary = {
        'loc': total['loc'],
        'lloc': total['lloc'],
        'comments': total['comments'],
        'comment_ratio': round(total['comment_ratio_sum'] / total['mi_count'], 2) if total['mi_count'] > 0 else 0.0,
        'function_count': total['function_count'],
        'class_count': total['class_count'],
        'mi': round(total['mi_sum'] / total['mi_count'], 2) if total['mi_count'] > 0 else 0,
        'cyclomatic_complexity': total['cyclomatic_complexity'],
        'rfc': total['rfc'],
        'wmc': total['wmc'],
        'dit': total['dit'],
        'lcom': round(total['lcom_sum'] / total['lcom_count'], 2) if total['lcom_count'] > 0 else 0.0,
        'noc': total['noc'],
        'cbo': total['cbo'],
        'halstead': {
            k: round(halstead_total[k] / halstead_count, 2) for k in halstead_fields
        } if halstead_count > 0 else {},
        'is_oop': oop_files > 0,
        'ca': total['ca'],
        'ce': total['ce'],
        'abstractness': round(total['abstractness_sum'] / total['design_count'], 2) if total['design_count'] > 0 else 0.0,
        'instability': round(total['instability_sum'] / total['design_count'], 2) if total['design_count'] > 0 else 0.0,
        'distance': round(total['distance_sum'] / total['design_count'], 2) if total['design_count'] > 0 else 0.0,
        'files': results,                         # Результати аналізу по кожному файлу
        'edges': edges,                           # Залежності між модулями
        'own_modules': list(module_names),        # Унікальні модулі
        'is_single_file': len(results) == 1       # Чи був лише один файл
    }

    return project_summary
