import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import sys

# Словарь перевода математических символов в человеческие фразы
MATH_DICTIONARY = {
    "∀": "Для любого (каждого) объекта",
    "∃!": "Существует и притом единственный объект",
    "∃": "Существует (найдется хотя бы один) объект",
    "∈": "принадлежащий множеству",
    "∉": "НЕ принадлежащий множеству",
    "⊂": "являющийся подмножеством",
    "⇒": "из этого логически следует, что",
    "⇔": "тогда и только тогда, когда (эквивалентно)",
    "→": "стремится к",
    "R": "действительных (реальных) чисел",
    "N": "натуральных чисел (1, 2, 3...)",
    "Z": "целых чисел (..., -1, 0, 1, ...)",
    "Q": "рациональных чисел (дробей)",
    "∅": "пустое множество (в котором ничего нет)",
    "¬": "отрицание того, что",
    "|": "такой, что",
    ":": "выполняется условие:",
}

# Встроенная расширяемая база данных сложных понятий высшей математики
# Вы можете добавлять сюда новые строчки прямо внутри кода!
CONCEPTS_DATABASE = {
    "Кольцо (Ring)": "💍 КОЛЬЦО в алгебре — это множество элементов, в котором можно без ограничений складывать, вычитать и умножать (как обычные целые числа), и для них работают привычные законы раскрытия скобок.",
    
    "Тензор (Tensor)": "🕸 ТЕНЗОР — это обобщение чисел и матриц. Скаляр (просто число) — это тензор ранга 0. Вектор (стрелка) — это тензор ранга 1. Матрица (таблица чисел) — это тензор ранга 2. Тензор описывает характеристики, которые меняются в зависимости от направления в пространстве (например, внутреннее напряжение в металле при деформации).",
    
    "Поле Галуа (Galois Field)": "🛡 ПОЛЕ ГАЛУА — это конечное множество элементов, в котором можно складывать, вычитать, умножать и делить (кроме деления на 0), но результат никогда не выходит за пределы этого множества. Основа современной криптографии и шифрования.",
    
    "Дифференциал (Differential)": "📉 ДИФФЕРЕНЦИАЛ — это главная, линейная часть приращения функции. Простыми словами, это то, насколько изменится значение функции (Y), если мы сдвинемся по графику на крошечный, почти незаметный шаг dx. Это микро-изменение.",
    
    "Векторное пространство": "🌌 ВЕКТОРНОЕ ПРОСТРАНСТВО — это просто математическая 'песочница', где лежат объекты (векторы), которые можно между собой складывать и умножать на обычные числа, и при этом результат гарантированно остается в этой же песочнице.",
    
    "Градиент (Gradient)": "⛰ ГРАДИЕНТ — это вектор (стрелка), который указывает направление самого крутого, самого быстрого роста какой-то величины (например, температуры в комнате или высоты горы). Если вы стоите на склоне, градиент покажет точно на вершину.",
    
    "Детерминант / Определитель": "📐 ДЕТЕРМИНАНТ (Определитель матрицы) — это число, которое показывает, во сколько раз трансформируется (растягивается или сжимается) площадь или объем пространства после воздействия на него этой самой матрицы."
}

def translate_math():
    input_text = entry_input.get().strip()
    output_area.delete("1.0", tk.END)
    
    if not input_text:
        output_area.insert(tk.END, "Пожалуйста, введите математическое выражение или выберите термин из списка-джойстика.")
        return
        
    translated_steps = []
    
    # Проверяем, есть ли такое точное понятие в нашей базе данных
    if input_text in CONCEPTS_DATABASE:
        translated_steps.append(CONCEPTS_DATABASE[input_text])
    else:
        # Если совпадения нет, пробуем искать вхождение слова (поиск по тексту)
        lower_input = input_text.lower()
        concept_found = False
        for concept, description in CONCEPTS_DATABASE.items():
            if concept.lower().split(" (")[0] in lower_input: # ищем по русскому названию
                translated_steps.append(description)
                concept_found = True
                break
                
        # Если это не текстовый термин, значит разбираем формулу со значками
        if not concept_found:
            translated_steps.append("🔍 ПОШАГОВЫЙ РАЗБОР ФОРМУЛЫ:\n")
            
            # Добавляем пробелы вокруг спецсимволов для корректного деления на токены
            working_text = input_text
            for symbol in MATH_DICTIONARY.keys():
                working_text = working_text.replace(symbol, f" {symbol} ")
                
            tokens = working_text.split()
            
            for token in tokens:
                if token in MATH_DICTIONARY:
                    translated_steps.append(f"• {token}  ➜  {MATH_DICTIONARY[token]}")
                else:
                    translated_steps.append(f"• переменная/число '{token}'")
                    
            translated_steps.append("\n💡 СВЯЗНЫЙ ТЕКСТ НА ЧЕЛОВЕЧЕСКОМ:")
            
            # Собираем красивую фразу с подстановками
            human_sentence = input_text
            for symbol, human_meaning in MATH_DICTIONARY.items():
                human_sentence = human_sentence.replace(symbol, f" [{human_meaning.lower()}] ")
            
            translated_steps.append(human_sentence)

    # Выводим итоговый результат в текстовое поле
    full_output = "\n".join(translated_steps)
    output_area.insert(tk.END, full_output)

def on_joystick_select(event):
    """Функция срабатывает при выборе термина в выпадающем списке (джойстике)"""
    selected_concept = combo_joystick.get()
    entry_input.delete(0, tk.END)
    entry_input.insert(0, selected_concept)
    translate_math()

def insert_symbol(symbol):
    """Позволяет кликать по кнопкам-значкам и вставлять их в поле ввода"""
    entry_input.insert(tk.INSERT, symbol)

def safe_exit():
    """Полное уничтожение процесса без зависания в ОС"""
    root.quit()
    root.destroy()
    sys.exit(0)

# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("🤖 Математический Переводчик v2.0 (Лицензия MIT)")
root.geometry("900x700")
root.configure(bg="#f4f6f9")

root.protocol("WM_DELETE_WINDOW", safe_exit)

# Заголовок
lbl_title = tk.Label(root, text="🚀 Переводчик Высшей Математики на Человеческий", font=("Arial", 14, "bold"), bg="#f4f6f9", fg="#2c3e50")
lbl_title.pack(pady=15)

# --- БЛОК 1: ДЖОЙСТИК (ВЫПАДАЮЩИЙ СПИСОК ПОНЯТИЙ) ---
frame_joystick = tk.LabelFrame(root, text=" 🕹️ Джойстик понятий (Выберите термин для мгновенного разбора) ", bg="#f4f6f9", font=("Arial", 10, "italic"))
frame_joystick.pack(fill=tk.X, padx=20, pady=5)

combo_joystick = ttk.Combobox(frame_joystick, values=list(CONCEPTS_DATABASE.keys()), font=("Arial", 11), state="readonly")
combo_joystick.pack(fill=tk.X, padx=15, pady=10)
combo_joystick.bind("<<ComboboxSelected>>", on_joystick_select)

# --- БЛОК 2: КНОПКИ БЫСТРОГО ВВОДА КВАНТОРОВ ---
frame_symbols = tk.LabelFrame(root, text=" ⌨️ Панель математических знаков (Кликните для ввода) ", bg="#f4f6f9", font=("Arial", 10, "italic"))
frame_symbols.pack(fill=tk.X, padx=20, pady=5)

symbols_to_show = ["∀", "∃", "∃!", "∈", "∉", "⊂", "⇒", "⇔", "→", "R", "N", "Z", "∅", ":"]
for sym in symbols_to_show:
    btn = tk.Button(frame_symbols, text=sym, font=("Arial", 12, "bold"), width=3, bg="white", command=lambda s=sym: insert_symbol(s))
    btn.pack(side=tk.LEFT, padx=4, pady=5, expand=True)

# --- БЛОК 3: ПОЛЕ РУЧНОГО ВВОДА ---
frame_input = tk.Frame(root, bg="#f4f6f9")
frame_input.pack(fill=tk.X, padx=20, pady=15)

lbl_input = tk.Label(frame_input, text="Формула или Ваш термин:", font=("Arial", 11, "bold"), bg="#f4f6f9")
lbl_input.pack(side=tk.LEFT, padx=5)

entry_input = tk.Entry(frame_input, font=("Arial", 12), width=35)
entry_input.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
entry_input.insert(0, "∀ x ∈ R : x > 0") # Базовый пример при старте

btn_translate = tk.Button(frame_input, text="Перевести 🚀", command=translate_math, bg="#28a745", fg="white", font=("Arial", 11, "bold"), width=12)
btn_translate.pack(side=tk.LEFT, padx=5)

# --- БЛОК 4: ОКНО ВЫВОДА РЕЗУЛЬТАТА ---
lbl_output = tk.Label(root, text="📜 Результат перевода (Объяснение):", font=("Arial", 11, "bold"), bg="#f4f6f9")
lbl_output.pack(anchor="w", padx=20, pady=5)

output_area = scrolledtext.ScrolledText(root, font=("Consolas", 11), wrap=tk.WORD, bg="white", bd=2, relief=tk.GROOVE)
output_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

# Кнопка закрытия
btn_exit = tk.Button(root, text="❌ Выйти из программы", command=safe_exit, bg="#dc3545", fg="white", font=("Arial", 10, "bold"))
btn_exit.pack(side=tk.BOTTOM, anchor="e", padx=20, pady=10)

# Сразу переводим стартовый пример, чтобы окно не было пустым
translate_math()

root.mainloop()
