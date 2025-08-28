import time
import asyncio


async def task(название, секунды):
    print(f"Начинаю {название}")
    await asyncio.sleep(секунды)
    print(f"Закончил {название}")


async def main():
    start = time.time()

    tasks = [
        asyncio.create_task(task("Загрузка файла", 3)),
        asyncio.create_task(task("Отправка email", 2)),
        asyncio.create_task(task("Запись в БД", 1)),
    ]

    await asyncio.wait(tasks)

    end = time.time()

    print(f"Время выполнения: {end - start}")

asyncio.run(main())

# start = time.time()

# task("Загрузка файла", 3)
# task("Отправка email", 2)
# task("Запись в БД", 1)

# end = time.time()

# print(f"Время выполнения: {end - start}")
