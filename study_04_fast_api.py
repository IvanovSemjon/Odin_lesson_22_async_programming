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


@app.get("/", response_class=HTMLResponse)
def home():
    return {"OK": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# логика гоночной платформы
async def car(name, distance = 10):
    position = 0
    
    while position < distance:
        speed = random.uniform(0.5, 2)        
        await asyncio.sleep(speed)
        position += 1
        print(f"🚗 {name}: {'█' * position}{'░' * (distance - position)} ({position}/{distance})")
        
    print(f"🏆 {name} финишировала!")    
    return name

async def race():
    
    tasks = [
        asyncio.create_task(car("Машина-1")),
        asyncio.create_task(car("Машина-2")),
        asyncio.create_task(car("Машина-3"))
    ]
    await asyncio.gather(*tasks)
    

# asyncio.run(race())

