@echo off
cd /d "%~dp0"

:: 🔹 Очистка папок
if exist uploads rd /s /q uploads
md uploads

if exist project rd /s /q project
md project

:: 🔹 Створення віртуального середовища (venv), якщо ще не існує
if not exist "venv" (
    echo [SETUP] Ініціалізація віртуального середовища Python...
    python -m venv venv
)

:: 🔹 Активація віртуального середовища
call venv\Scripts\activate

:: 🔹 Оновлення менеджера пакетів pip до останньої версії
echo [SETUP] Оновлення pip до останньої версії...
venv\Scripts\python.exe -m pip install --upgrade pip >nul

:: 🔹 Інсталяція залежностей з requirements.txt
echo [SETUP] Встановлення Python-залежностей з requirements.txt...
venv\Scripts\python.exe -m pip install -r requirements.txt >nul

:: 🔹 Запуск Flask-додатку (локальний веб-сервер)
echo [RUN] Запуск Flask-додатку...
start "" http://127.0.0.1:5000
venv\Scripts\python.exe app.py

echo [ERROR] Додаток завершився. Натисніть будь-яку клавішу...
pause
