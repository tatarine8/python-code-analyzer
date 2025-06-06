import ast
import os
from typing import Dict, Set
from core.utils import normalize_import

# Визначає назву кореневого пакета на основі шляху до папки
def infer_root_package(root_path: str) -> str:
    return os.path.basename(os.path.abspath(root_path))

# Рахує efferent coupling (Ce) — кількість унікальних модулів, які імпортує цей модуль
def count_efferent_coupling(tree, module_name, root_package, own_modules: Set[str] = None):
    imported_modules = set()
    current_pkg_parts = module_name.split('.')[:-1]  # Частини шляху до поточного пакета

    for node in ast.walk(tree):
        # Простий import
        if isinstance(node, ast.Import):
            for alias in node.names:
                norm = normalize_import(alias.name, root_package)
                if norm:
                    if not own_modules or norm in own_modules:
                        imported_modules.add(norm)

        # Відносний або абсолютний import from
        elif isinstance(node, ast.ImportFrom):
            level = node.level
            mod = node.module or ''
            prefix_len = len(current_pkg_parts) - level + 1 if level > 0 else 0
            prefix_parts = current_pkg_parts[:prefix_len] if prefix_len > 0 else []
            full_base = '.'.join(prefix_parts + ([mod] if mod else []))

            for alias in node.names:
                full_name = full_base + '.' + alias.name if full_base else alias.name
                norm = normalize_import(full_name, root_package)
                if norm:
                    if not own_modules or norm in own_modules:
                        imported_modules.add(norm)

    return len(imported_modules), imported_modules

# Рахує afferent coupling (Ca) — кількість модулів, які імпортують цей модуль
def count_afferent_coupling(target_module: str, all_sources: Dict[str, str], root_package: str):
    count = 0
    for name, code in all_sources.items():
        if name == target_module:
            continue
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                full_name = normalize_import(node.module or "", root_package)
                if full_name.startswith(target_module):
                    count += 1
                    break
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imp_name = normalize_import(alias.name, root_package)
                    if imp_name.startswith(target_module):
                        count += 1
                        break

    return count

# Обчислює Instability (I = Ce / (Ca + Ce))
def compute_instability(ca, ce):
    return round(ce / (ca + ce), 2) if (ca + ce) > 0 else 0.0

# Обчислює Abstractness (A = кількість абстрактних класів / загальна кількість класів)
def compute_abstractness(tree):
    total_classes = 0
    abstract_classes = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            total_classes += 1

            # Пошук спадкування від ABC
            has_abstract_base = any(
                (isinstance(base, ast.Name) and base.id == 'ABC') or
                (isinstance(base, ast.Attribute) and base.attr == 'ABC')
                for base in node.bases
            )

            # Пошук методів з декоратором @abstractmethod
            has_abstract_method = any(
                (isinstance(dec, ast.Name) and dec.id == 'abstractmethod') or
                (isinstance(dec, ast.Attribute) and dec.attr == 'abstractmethod')
                for stmt in node.body if isinstance(stmt, ast.FunctionDef)
                for dec in getattr(stmt, 'decorator_list', [])
            )

            if has_abstract_base or has_abstract_method:
                abstract_classes += 1

    return round(abstract_classes / total_classes, 2) if total_classes > 0 else 0.0

# Обчислює відстань до головної послідовності (Main Sequence): D = |A + I - 1|
def compute_distance_from_main_sequence(A, I):
    return round(abs(A + I - 1), 2)

# Основна функція для аналізу архітектурних метрик модуля
def analyze_design_metrics(module_name: str, tree, all_sources: Dict[str, str], root_path: str = ''):
    root_package = infer_root_package(root_path) if root_path else ''
    own_modules = set(all_sources.keys())

    # Рахуємо efferent та afferent coupling
    ce, imported = count_efferent_coupling(tree, module_name, root_package, own_modules)
    ca = count_afferent_coupling(module_name, all_sources, root_package)

    # Обчислюємо абстрактність, нестабільність та відстань до ідеалу
    A = compute_abstractness(tree)
    I = compute_instability(ca, ce)
    D = compute_distance_from_main_sequence(A, I)

    return {
        "ce": ce,
        "ca": ca,
        "abstractness": A,
        "instability": I,
        "distance": D,
        "imports": list(imported)
    }
