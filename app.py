import os
import zipfile
import shutil
import io
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, send_file
from metrics_analyser import analyze_project

# Ініціалізація Flask-додатку
app = Flask(__name__)

# Налаштування повного логування з ротацією у logs/app.log
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file_path = os.path.join(LOG_DIR, "app.log")

handler = RotatingFileHandler(log_file_path, maxBytes=1024*1000, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Конфігурація директорій та обмеження розміру файлу
UPLOAD_FOLDER = 'uploads'
PROJECT_FOLDER = 'project'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROJECT_FOLDER'] = PROJECT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

# Створення директорій, якщо їх ще немає
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROJECT_FOLDER, exist_ok=True)

# Кеш для збереження результатів аналізу
analyze_project_data_cache = None

# Головна сторінка (форма для завантаження)
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Збереження завантаженого файлу у тимчасову директорію
def save_uploaded_file(file):
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filename, filepath

# Підготовка шляху для розпакування або копіювання файлу
def prepare_extraction_dir(filename):
    project_name = os.path.splitext(filename)[0]
    extract_path = os.path.join(app.config['PROJECT_FOLDER'], project_name)
    os.makedirs(extract_path, exist_ok=True)
    return extract_path

# Розпакування архіву або копіювання звичайного файлу у цільову директорію
def extract_or_copy(filepath, extract_path, filename):
    if zipfile.is_zipfile(filepath):
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    else:
        shutil.copy(filepath, os.path.join(extract_path, filename))

# Обробка завантаженого файлу та запуск аналізу
@app.route('/analyze', methods=['POST'])
def analyze():
    global analyze_project_data_cache

    if 'code_file' not in request.files:
        return 'Файл не завантажено', 400

    file = request.files['code_file']
    if file.filename == '':
        return 'Файл не вибрано', 400

    # Збереження файлу та підготовка директорії для аналізу
    filename, filepath = save_uploaded_file(file)
    extract_path = prepare_extraction_dir(filename)

    try:
        app.logger.info(f"Аналіз файлу: {filename}")
        extract_or_copy(filepath, extract_path, filename)
        result = analyze_project(extract_path)
        analyze_project_data_cache = result
        app.logger.info("Аналіз успішно завершено")
    except Exception as e:
        app.logger.exception("Помилка при аналізі файлу")
        return f'Помилка аналізу: {str(e)}', 500
    finally:
        os.remove(filepath)
        shutil.rmtree(extract_path)
        app.logger.info("Тимчасові файли очищено")

    return render_template('result.html', result=result)

# Побудова плоского представлення метрик для експорту
def build_flat_metrics(data):
    flat_data = []
    for file in data['files']:
        hal = file.get('halstead', {})
        flat_data.append({
            'filename': file.get('filename'),
            'module': file.get('module_name'),
            'loc': file.get('loc'),
            'lloc': file.get('lloc'),
            'comments': file.get('comments'),
            'comment_ratio': file.get('comment_ratio'),
            'functions': file.get('function_count'),
            'classes': file.get('class_count'),
            'mi': file.get('mi'),
            'rfc': file.get('rfc'),
            'wmc': file.get('wmc'),
            'lcom': file.get('lcom'),
            'noc': file.get('noc'),
            'cbo': file.get('cbo'),
            'halstead_volume': hal.get('volume'),
            'halstead_bugs': hal.get('bugs'),
            'ca': file.get('ca'),
            'ce': file.get('ce'),
            'abstractness': file.get('abstractness'),
            'instability': file.get('instability'),
            'distance': file.get('distance'),
            'imports_count': len(file.get('imports', []))
        })
    return flat_data

# Експорт результатів у форматі CSV
@app.route('/export/csv')
def export_csv():
    if not analyze_project_data_cache:
        return 'Немає збережених результатів', 400

    df = pd.DataFrame(build_flat_metrics(analyze_project_data_cache))
    csv_io = io.StringIO()
    df.to_csv(csv_io, index=False)
    return send_file(
        io.BytesIO(csv_io.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='analysis_results.csv'
    )

# Експорт результатів у форматі Excel
@app.route('/export/excel')
def export_excel():
    if not analyze_project_data_cache:
        return 'Немає збережених результатів', 400

    df = pd.DataFrame(build_flat_metrics(analyze_project_data_cache))
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Code Metrics')
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='analysis_results.xlsx'
    )

# Запуск сервера 
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1", port=5000)
