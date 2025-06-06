from radon.raw import analyze as raw_analyze
from radon.metrics import mi_visit

# Обчислює базові метрики з сирого коду (LOC, LLOC, коментарі, MI)
def compute_raw_metrics(code):
    raw = raw_analyze(code)          # Аналіз рядків коду
    mi = mi_visit(code, False)       # Індекс підтримуваності (Maintainability Index)

    # Відсоток коментарів від загальної кількості рядків
    comment_ratio = round((raw.comments / raw.loc * 100), 2) if raw.loc > 0 else 0.0

    return {
        'loc': raw.loc,                 # Кількість усіх рядків
        'lloc': raw.lloc,              # Кількість логічних (непорожніх) рядків
        'comments': raw.comments,      # Кількість рядків з коментарями
        'comment_ratio': comment_ratio,
        'mi': mi                       # Maintainability Index
    }
