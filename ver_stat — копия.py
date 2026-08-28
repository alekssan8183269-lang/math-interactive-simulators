import tkinter as tk
from tkinter import messagebox
import math

# Настройка бэкенда matplotlib для работы внутри tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def calculate_stats(shoots):
    """Вычисляет среднее, дисперсию и стандартное отклонение"""
    n = len(shoots)
    mean = sum(shoots) / n
    
    # Квадраты отклонений
    variance = sum((x - mean) ** 2 for x in shoots) / n
    std_deviation = math.sqrt(variance)
    
    return mean, variance, std_deviation

def draw_graphs():
    try:
        # Считываем данные из полей ввода
        shoots_a = [float(x) for x in entry_a.get().split()]
        shoots_b = [float(x) for x in entry_b.get().split()]
        
        if len(shoots_a) != 5 or len(shoots_b) != 5:
            raise ValueError("Нужно ввести ровно 5 чисел через пробел!")
    except ValueError as e:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите 5 чисел через пробел для каждого стрелка.\nПример: 9 9 10 10 10")
        return

    # Расчеты
    mean_a, var_a, std_a = calculate_stats(shoots_a)
    mean_b, var_b, std_b = calculate_stats(shoots_b)
    
    # Обновляем текстовые результаты в интерфейсе
    result_text_a.config(text=f"Среднее: {mean_a:.2f}\nДисперсия: {var_a:.2f}\nСтанд. откл (разброс): {std_a:.2f}")
    result_text_b.config(text=f"Среднее: {mean_b:.2f}\nДисперсия: {var_b:.2f}\nСтанд. откл (разброс): {std_b:.2f}")
    
    # Очищаем старый график перед рисованием нового
    ax1.clear()
    ax2.clear()
    
    x_points = [1, 2, 3, 4, 5]
    
    # --- График Стрелка А ---
    ax1.scatter(x_points, shoots_a, color='#1f77b4', s=100, zorder=3, label='Выстрелы А')
    ax1.axhline(y=mean_a, color='#d62728', linestyle='--', linewidth=2, label=f'Среднее ({mean_a:.1f})')
    # Рисуем линии отклонений (показываем рассеивание)
    for x, y in zip(x_points, shoots_a):
        ax1.vlines(x, min(y, mean_a), max(y, mean_a), colors='gray', linestyles='dotted', linewidth=1.5)
    ax1.set_title(f"Стрелок А (Стабильный, откл: {std_a:.2f})", fontsize=10)
    ax1.set_ylim(0, 11)
    ax1.set_xticks(x_points)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='lower left', fontsize=8)
    
    # --- График Стрелка Б ---
    ax2.scatter(x_points, shoots_b, color='#ff7f0e', s=100, zorder=3, label='Выстрелы Б')
    ax2.axhline(y=mean_b, color='#d62728', linestyle='--', linewidth=2, label=f'Среднее ({mean_b:.1f})')
    # Рисуем линии отклонений
    for x, y in zip(x_points, shoots_b):
        ax2.vlines(x, min(y, mean_b), max(y, mean_b), colors='gray', linestyles='dotted', linewidth=1.5)
    ax2.set_title(f"Стрелок Б (С разбросом, откл: {std_b:.2f})", fontsize=10)
    ax2.set_ylim(0, 11)
    ax2.set_xticks(x_points)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='lower left', fontsize=8)
    
    # Обновляем холст в окне tkinter
    canvas.draw()

# --- Создание окна Tkinter ---
root = tk.Tk()
root.title("Вероятность и Статистика 8 класс: Рассеивание данных")
root.geometry("1100x700")  # Сразу сделали окно пошире по умолчанию
root.configure(bg="#f0f0f0")

# Верхняя панель управления (теперь она растягивается по ширине)
top_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10)

# Настраиваем адаптивные колонки для верхней панели
top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=1)
top_frame.columnconfigure(2, weight=1)

# Ввод для Стрелка А
lbl_a = tk.Label(top_frame, text="Стрелок А (5 выстрелов):", bg="#f0f0f0", font=("Arial", 10, "bold"))
lbl_a.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_a = tk.Entry(top_frame, width=20, font=("Arial", 10))
entry_a.insert(0, "9 9 10 10 10")
entry_a.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

result_text_a = tk.Label(top_frame, text="Нажмите 'Рассчитать'", bg="#e0e0e0", width=25, justify=tk.LEFT, font=("Courier", 9))
result_text_a.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

# Ввод для Стрелка Б
lbl_b = tk.Label(top_frame, text="Стрелок Б (5 выстрелов):", bg="#f0f0f0", font=("Arial", 10, "bold"))
lbl_b.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_b = tk.Entry(top_frame, width=20, font=("Arial", 10))
entry_b.insert(0, "5 6 10 9 10")
entry_b.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

result_text_b = tk.Label(top_frame, text="Нажмите 'Рассчитать'", bg="#e0e0e0", width=25, justify=tk.LEFT, font=("Courier", 9))
result_text_b.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

# Кнопка расчета (теперь стоит в отдельной колонке справа)
btn_calc = tk.Button(top_frame, text="📊 Рассчитать и показать графики", command=draw_graphs, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=10)
btn_calc.grid(row=0, column=3, rowspan=2, padx=15, pady=5, sticky="nsew")

# Создаем фигуру Matplotlib для графиков
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
fig.tight_layout(pad=3.0)

# ИСПРАВЛЕНО: Интегрируем график в Tkinter с правильным классом холста
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
# fill=tk.BOTH и expand=True заставляют графики растягиваться при разворачивании окна
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Запускаем приложение
root.mainloop()