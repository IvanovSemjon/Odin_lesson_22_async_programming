# Импорт необходимых библиотек
import asyncio  # Для асинхронного программирования
import random   # Для генерации случайных чисел
import sys      # Для работы с системными параметрами
import os       # Для выполнения системных команд
from fastapi import FastAPI  # Веб-фреймворк для создания API
from fastapi.responses import HTMLResponse  # Для возврата HTML-ответов
import uvicorn  # ASGI сервер для запуска FastAPI

# Настройка кодировки UTF-8 для корректного отображения русских символов в Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')  # Устанавливаем кодовую страницу UTF-8
    sys.stdout.reconfigure(encoding='utf-8')  # Настраиваем вывод в UTF-8
    sys.stderr.reconfigure(encoding='utf-8')  # Настраиваем вывод ошибок в UTF-8

# Создаем экземпляр FastAPI приложения
app = FastAPI(title="🏁 Гонки машин 🏁")

# Глобальное состояние гонки - хранит данные о текущем состоянии
race_data = {
    "cars": ["Машина № 1", "Машина № 2", "Машина № 3"],  # Названия машин
    "positions": [0, 0, 0],  # Текущие позиции каждой машины
    "distance": 10,          # Дистанция гонки
    "racing": False,         # Флаг - идет ли гонка сейчас
    "winner": None           # Победитель гонки
}


# Главная страница - возвращает HTML файл
@app.get("/", response_class=HTMLResponse)
def home():
    """Отдает главную HTML страницу с интерфейсом гонки"""
    return open("index.html", "r", encoding="utf-8").read()


# Асинхронная функция для симуляции движения одной машины
async def car_race(car_index):
    """Симулирует движение машины с заданным индексом"""
    global race_data
    
    # Машина движется пока не достигнет финиша и гонка активна
    while race_data["positions"][car_index] < race_data["distance"] and race_data["racing"]:
        # Случайная задержка имитирует разную скорость машин
        await asyncio.sleep(random.uniform(0.5, 1.5))
        # Увеличиваем позицию машины на 1
        race_data["positions"][car_index] += 1
        
        # Проверяем, достигла ли машина финиша
        if race_data["positions"][car_index] >= race_data["distance"]:
            # Если еще нет победителя, объявляем эту машину победителем
            if race_data["winner"] is None:
                race_data["winner"] = race_data["cars"][car_index]
                race_data["racing"] = False  # Останавливаем гонку


# API endpoint для запуска гонки
@app.get("/start")
async def start_race():
    """Запускает новую гонку"""
    global race_data
    
    # Проверяем, не идет ли уже гонка
    if race_data["racing"]:
        return {"message": "Гонка уже идет!"}
    
    # Сбрасываем состояние гонки к начальным значениям
    race_data["positions"] = [0, 0, 0]  # Все машины на старте
    race_data["racing"] = True           # Гонка активна
    race_data["winner"] = None           # Победителя пока нет

    # Создаем асинхронные задачи для каждой машины
    # Каждая машина будет двигаться независимо в своей корутине
    tasks = [asyncio.create_task(car_race(i)) for i in range(3)]

    return {"message": "Гонка началась!"}


# API endpoint для сброса состояния гонки
@app.get("/reset")
async def reset_race():
    """Сбрасывает состояние гонки к начальным значениям"""
    global race_data
    
    # Возвращаем все параметры к исходному состоянию
    race_data["positions"] = [0, 0, 0]  # Все машины на старте
    race_data["racing"] = False          # Гонка не активна
    race_data["winner"] = None           # Победителя нет
    
    return {"message": "Готов к гонкам!"}


# API endpoint для получения текущего состояния гонки
@app.get("/status")
def get_status():
    """Возвращает текущее состояние гонки в формате JSON"""
    # Отправляем клиенту все данные о текущем состоянии
    return {
        "cars": race_data["cars"],           # Названия машин
        "positions": race_data["positions"], # Текущие позиции
        "distance": race_data["distance"],   # Дистанция гонки
        "racing": race_data["racing"],       # Статус гонки
        "winner": race_data["winner"]        # Победитель (если есть)
    }



# Запуск сервера только при прямом выполнении файла
if __name__ == "__main__":
    # Запускаем ASGI сервер uvicorn с нашим FastAPI приложением
    # host="127.0.0.1" - локальный адрес
    # port=8000 - порт для подключения
    uvicorn.run(app, host="127.0.0.1", port=8000)


