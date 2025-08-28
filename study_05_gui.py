import tkinter as tk
import random

root = tk.Tk()
root.title("Гонки")
root.geometry("500x400")

# Словарь для хранения лейблов машин
car_labels = {}
car_positions = {}
race_active = False
distance = 10

# Заголовок
tk.Label(root, text="🏁 Гонки 🏁", font=("Arial", 16)).pack(pady=10)

# Кнопки
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

def update_car(name):
    """Обновляет позицию одной машины"""
    if not race_active or car_positions[name] >= distance:
        return
    
    # Случайно двигаем машину
    if random.random() < 0.3:  # 30% шанс двинуться
        car_positions[name] += 1
    
    # Обновляем отображение
    progress = "█" * car_positions[name] + "░" * (distance - car_positions[name])
    car_labels[name].config(text=f"{name}: {progress} ({car_positions[name]}/{distance})")
    
    # Проверяем победу
    if car_positions[name] >= distance:
        car_labels[name].config(text=f"{name}: 🏆 ПОБЕДИТЕЛЬ! 🏆")
        return
    
    # Продолжаем обновление через 200мс
    root.after(200, lambda: update_car(name))

def start_race():
    """Запускает гонку"""
    global race_active
    race_active = True
    
    # Сбрасываем позиции
    for name in car_positions:
        car_positions[name] = 0
    
    # Запускаем обновление каждой машины
    for name in car_positions:
        update_car(name)

def stop_race():
    """Останавливает гонку"""
    global race_active
    race_active = False

tk.Button(button_frame, text="Старт", command=start_race,
          bg="green", fg="white", width=10).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="Стоп", command=stop_race,
          bg="red", fg="white", width=10).pack(side=tk.LEFT, padx=5)

# Создаем машины
for name, color in [("🚗 Красная", "red"), ("🚙 Синяя", "blue"), ("🚕 Зеленая", "green")]:
    label = tk.Label(root, text=f"{name}: ждёт старта", 
                     font=("Courier", 12), fg=color)
    label.pack(pady=5)
    car_labels[name] = label
    car_positions[name] = 0

root.mainloop()
  