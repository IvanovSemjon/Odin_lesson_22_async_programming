import asyncio
import random
import sys
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn


# Настройка кодировки для Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')
    # Настройка stdout для UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Поднимаем веб сервер
app = FastAPI(title="Гонки машин")


race_data = {
    "cars": ["Машина № 1", "Машина № 2", "Машина № 3"],
    "positions": [0, 0, 0],
    "distance": 10,
    "racing": False,
    "winner": None
}


@app.get("/", response_class=HTMLResponse)
def home():
    return open("index.html", "r", encoding="utf-8").read()


# логика гоночной платформы
async def car_race(car_index, distance = 10):
    global race_data

    while race_data["positions"][car_index] < race_data["distance"] and race_data["racing"]:
        # случайная скорость машины
        await asyncio.sleep(random.uniform(0.5, 1.5))
        race_data["positions"][car_index] += 1


@app.get("/start")
async def start_race():
    """Запускает гонку"""
    global race_data
    if race_data["racing"]:
        return {"message": "Гонка уже идет!"}
    # Сбрасываем состояние
    race_data["positions"] = [0, 0, 0]
    race_data["racing"] = True
    race_data["winner"] = None

    # Создаем задачи для каждой машины
    tasks = [asyncio.create_task(car_race(i)) for i in range(3)]

    # tasks = [car_race(name) for name in ["Красная", "Синяя", "Зеленая"]]
    # await asyncio.gather(*tasks)

    return {"message": "Гонка началась!"}


@app.get("/reset")
async def start_race():
    """Сбрасывает гонку"""
    race_data["positions"] = [0, 0, 0]
    race_data["racing"] = True
    race_data["winner"] = None
    return {"message": "Готов к гонкам!"}


@app.get("/status")
def get_status():
    """Возвращает текущее состояние гонок"""
    return {
        "cars": race_data["cars"],
        "positions": race_data["positions"],
        "distance": race_data["distance"],
        "racing": race_data["racing"],
        "winner": race_data["winner"]
    }



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


