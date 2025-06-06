
# Python Code Analyzer — Веб-інструмент для оцінки якості Python-коду

**Python Code Analyzer** — це веб-орієнтований інструмент, створений для глибокого аналізу, візуалізації та оцінки Python-коду за допомогою широкого набору метрик: підтримуваність, складність, обсяг, архітектура, об'єктно-орієнтований дизайн.

Результати подаються у вигляді дашбордів, графіків, таблиць і загальної оцінки якості проєкту.

---

## 🔧 Запуск

### 1. Клонування проєкту
```bash
git clone https://github.com/tatarine8/python-code-analyzer.git
cd python-code-analyzer
```

### 2. Встановлення залежностей
```bash
python -m venv venv
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

### 3. Запуск додатку
- Запусти файл `start.vbs` подвійним кліком миші.
- Вікно браузера відкриється автоматично.
- Flask-додаток буде запущено у фоновому режимі.

> Якщо запуск блокується, клацни правою кнопкою → “Запустити від імені адміністратора”.

---

## 🔍 Основні можливості

| Розділ            | Опис                                                                 |
|-------------------|----------------------------------------------------------------------|
| Завантаження      | Підтримка .py файлів або ZIP-архівів з проєктом                      |
| Загальний аналіз  | LOC, LLOC, кількість функцій/класів, MI, % коментарів                 |
| Візуалізація      | Гістограми, діаграми, bubble-графіки, radar-оцінка                    |
| OOP метрики       | RFC, WMC, LCOM, NOC, CBO, DIT                                          |
| Архітектурні      | Ca, Ce, Abstractness, Instability, Distance                           |
| Залежності        | Візуальний граф імпортів між модулями + списковий перегляд           |
| Таблиця           | Повна таблиця метрик з кольоровим кодуванням                         |
| Оцінка            | Сумарна оцінка коду + поради щодо покращення                         |
| Експорт           | Збереження результатів у форматах CSV та Excel                       |
| Допомога          | Інтерактивні пояснення всіх використовуваних метрик                  |

---

## 📐 Метрики, що враховуються

- **Maintainability Index**
- **Halstead Metrics**: Volume, Difficulty, Effort, Bugs
- **Cyclomatic Complexity**
- **OOP Metrics**: RFC, WMC, LCOM, CBO, DIT, NOC
- **Architecture**: Ca, Ce, Abstractness, Instability, Distance
- **Raw Stats**: LOC, LLOC, Comments, % Comments

---

## 📁 Структура проєкту

```
├── app.py                     # Flask-сервер
├── metrics_analyser.py        # Аналіз проєкту
├── core/
│   ├── analyze_code.py        # Аналіз одного файлу
│   ├── raw_stats.py
│   ├── complexity.py
│   ├── halstead.py
│   ├── design_metrics.py
│   ├── oop_metrics.py
│   └── utils.py
├── templates/
│   ├── index.html
│   └── result.html
├── static/js/
│   ├── analysis_charts.js
│   ├── functions.js
│   └── dependencies_view.js
├── requirements.txt
├── run_app.bat
├── start.vbs
```

---

## ⚖️ Ліцензія

MIT License — дозволено використовувати, модифікувати та поширювати проєкт з освітньою або практичною метою.

---

## 👤 Автор

> Розроблено в рамках дипломної роботи  
> **Євгеній Татарін**, 2025  
> [github.com/tatarine8](https://github.com/tatarine8)
