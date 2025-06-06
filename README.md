# 🧠 Python Code Analyzer — Інструмент оцінки якості коду

Цей проєкт — це **веб-інструмент для аналізу, візуалізації та оцінки якості Python-коду**, що розраховує численні метрики підтримуваності, складності, обсягу, архітектури та об'єктно-орієнтованого дизайну.  
Результати виводяться у вигляді дашбордів, таблиць і графіків.

---

## 🚀 Як запустити

### 1. Клонувати репозиторій:
```bash
git clone https://github.com/your-username/python-code-analyzer.git
cd python-code-analyzer
```

### 2. Встановити залежності:
Рекомендується створити віртуальне середовище:

```bash
python -m venv venv
venv\Scripts\activate  # для Windows
source venv/bin/activate  # для Linux/Mac
pip install -r requirements.txt
```

### 3. Запустити додаток:
```bash
python app.py
```

---

## 📦 Функціонал

| Розділ             | Опис                                                                 |
|--------------------|----------------------------------------------------------------------|
| 📥 Завантаження    | Завантаження `.py` файлу або `.zip` проєкту                         |
| 📊 Загальний аналіз| LOC, LLOC, % коментарів, MI, кількість класів/функцій               |
| 📈 Візуалізація    | Гістограми, діаграми, bubble-графіки, radar-графік                  |
| 🧩 OOP метрики     | RFC, WMC, LCOM, NOC, CBO, DIT                                       |
| 🏗 Архітектурні     | Ca, Ce, Abstractness, Instability, Distance                         |
| 📎 Залежності      | Граф імпортів між модулями + списковий перегляд                     |
| 📋 Таблиця         | Табличне подання всіх метрик з кольоровим виділенням                |
| 🧠 Оцінка          | Загальна оцінка коду за 6 критеріями + поради по покращенню         |
| 📤 Експорт         | Експорт результатів у CSV та Excel                                  |
| 🆘 Допомога        | Інструкції та пояснення всіх метрик                                 |

---

## 🧮 Метрики

Використовуються такі метрики:
- **Maintainability Index (MI)**
- **Halstead Metrics**: Volume, Bugs, Difficulty тощо
- **Cyclomatic Complexity**
- **OOP Metrics**: RFC, WMC, LCOM, CBO, DIT, NOC
- **Architecture**: Abstractness, Instability, Distance
- **Raw**: LOC, LLOC, Comments, % коментарів

---

## 📁 Структура

\`\`\`
├── app.py                  # Flask-сервер
├── metrics_analyser.py     # Аналіз проєкту
├── analyze_code.py         # Аналіз одного файлу
├── core/
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
\`\`\`

---

## 📄 Ліцензія

MIT License — використовуй в освітніх або практичних цілях без обмежень.

---

## 🧑‍💻 Автор

> **Розроблено в рамках дипломної роботи для оцінки Python-проєктів.**  
> Автор: *Євгеній Татарін*
