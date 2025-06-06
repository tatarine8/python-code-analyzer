import os

# Перетворює шлях до .py-файлу у форматі файлової системи на модульну назву (a/b/c.py → a.b.c)
def path_to_module(file_path, root_path):
    rel_path = os.path.relpath(file_path, root_path)          # Відносний шлях від кореня
    no_ext = rel_path.replace('.py', '')                      # Видалення розширення
    parts = no_ext.replace(os.sep, '.').split('.')            # Розбивка на частини
    parts = [p for p in parts if p.isidentifier()]            # Фільтр коректних ідентифікаторів
    return '.'.join(parts)

# Нормалізує ім'я імпортованого модуля до єдиного формату
def normalize_import(name: str, root_package: str = '') -> str:
    if not name:
        return ''

    name = name.replace("/", ".").replace("\\", ".").replace(".py", "").strip()
    parts = [p for p in name.split(".") if p and p.isidentifier()]

    # Видаляє root-префікс, якщо він співпадає з першим сегментом
    if root_package and parts and parts[0] == root_package:
        parts = parts[1:]

    # Видаляє останній сегмент, якщо це, ймовірно, клас або функція
    if len(parts) > 1 and (parts[-1][0].isupper() or not parts[-1].islower()):
        parts = parts[:-1]

    return ".".join(parts)
