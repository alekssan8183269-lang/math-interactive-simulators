# Базовая лаборатория соцсетей — Введение, степени вершин и вычисление скрытого 🕵️ Серого кардинала.
# ОГЭ-Тенажёр (Задачи №1 и №3) — Подсчёт вариантов путей буквами A-F слева направо.
# GPS-Навигатор Дейкстры — Объезд заторов по цветовым кодам дорожных пробок.
# Загадка Кёнигсбергских мостов — Пошаговая головоломка Эйлера с ползунком движения карандаша.
# Детектор Big Data — Силовое ИИ-стягивание хаотичного класса в цветные группы по интересам.
# Теорема о 4 красках — Стратегическая игра-раскраска карт кликами мыши на холсте.
# Симулятор биатлона Бернулли — Электронное табло мишеней и дерево вероятностей на 10 000 выстрелов.
# Информационный вирус — Каскадное заражение интернета и пошаговый «эффект бабочки».
# ИИ-Отдел Кадров — Двудольные графы и Венгерский метод распределения должностей.
# Симулятор Водоканала — Поток Форда-Фалкерсона с плавной анимацией наполнения труб водой.
# Экономный Электрик — Остовное дерево Борувки/Краскала для жёсткой экономии бюджета на кабели.

# ==============================================================================
# ОФИЦИАЛЬНАЯ БИБЛИОТЕКА ИСТОЧНИКОВ И УЧЕБНИКОВ ПО ТЕОРИИ ГРАФОВ ДЛЯ КУРСА
# ==============================================================================
# Все указанные книги являются фундаментальной мировой классикой. 
# Их можно официально найти в библиотеках, открыть в электронных каталогах
# или проверить по международным номерам ISBN.
# ==============================================================================

# КНИГА 1. МАТЕМАТИЧЕСКАЯ ОСНОВА И КЛАССИКА ТЕОРИИ ГРАФОВ
# Авторы: Харари Фрэнк
# Название: Теория графов
# Официальное издание: Москва, Издательство Мир, 1973 год (Перевод легендарного американского издания Graph Theory, 1969).
# Для каких уроков: Это база для Урока 1 (Сети и Серые Кардиналы), Урока 4 (Сообщества) и Урока 6 (Теорема о 4 красках). Харари — отец современной визуализации графов.

# КНИГА 2. ГЛАВНЫЙ СОВРЕМЕННЫЙ МИРОВОЙ УЧЕБНИК
# Авторы: Дистель Рейнгард
# Название: Теория графов
# Официальное издание: Новосибирск, Издательство Института математики им. С.Л. Соболева СО РАН, 2002 год (Оригинал: Diestel R. Graph Beauty, Springer, 2000).
# Для каких уроков: Идеально для Урока 4 (Эйлеровы пути и Домики), Урока 6 (Раскраска графов) и Урока 11 (Энергосети и Остовные деревья). Самый авторитетный учебник в университетах мира.

# КНИГА 3. БИБЛИЯ КОМПЬЮТЕРНЫХ АЛГОРИТМОВ И ПРОГРАММИРОВАНИЯ
# Авторы: Кормен Томас, Лейзерсон Чарльз, Ривест Рональд, Штайн Клиффорд
# Название: Алгоритмы: построение и анализ (2-е или 3-е издание)
# Официальное издание: Москва, Издательский дом Вильямс, 2013 год (Оригинал: Introduction to Algorithms, MIT Press).
# Для каких уроков: Прямой источник кода для Урока 2 (ОГЭ-Тренажер), Урока 3 (Навигатор Дейкстры), Урока 7 (Задача коммивояжера) и Урока 10 (Водоканал Форда-Фалкерсона). Здесь детально описано, как переводить линии в компьютерные матрицы.

# КНИГА 4. ПРИКЛАДНЫЕ ИНЖЕНЕРНЫЕ И ВОЕННЫЕ РАСЧЁТЫ
# Авторы: Кристофидес Никос
# Название: Теория графов. Алгоритмический подход
# Официальное издание: Москва, Издательство Мир, 1978 год (Оригинал: Christofides N. Graph Theory: An Algorithmic Approach, Academic Press, 1975).
# Для каких уроков: Главный источник для Урока 9 (ИИ-Отдел Кадров и двудольные графы) и Урока 10 (Потоки в трубах). Именно в этой книге собран лучший в истории разбор Венгерского метода и логистики.

# КНИГА 5. ПЕРВОИСТОЧНИК РОЖДЕНИЯ НАУКИ О ГРАФАХ
# Авторы: Леонард Эйлер
# Название: Письма к немецкой принцессе о разных физических и философских материях
# Официальное издание: Санкт-Петербург, Издательство Академии Наук, 1768 год (Оригинальный доклад в Академию: Solutio problematis ad geometriam situs pertinentis, 1736).
# Для каких уроков: Исторический фундамент для Урока 4 (Семь мостов Кёнигсберга). Это документ, с которого началась вся наука!

# КНИГА 6. ДЛЯ ПОДГОТОВКИ К ЭКЗАМЕНАМ И ОЛИМПИАДАМ
# Авторы: Поляков Константин Юрьевич, Еремин Илья Владимирович
# Название: Информатика. Углубленный уровень. Учебник для 10-11 классов (В 2-х частях)
# Официальное издание: Москва, Издательство БИНОМ. Лаборатория знаний, 2019 год.
# Для каких уроков: Основа для Урока 2 (Задачи ОГЭ/ЕГЭ на графы и таблицы) и Урока 11 (Алгоритмы Краскала и Прима для связи городов).

# ==============================================================================
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import winsound

class AiLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Как учится ИИ? Графы + Вероятность (8 класс)")
        self.root.geometry("1300x820")
        
        self.lidar_enabled = True  # Режим лазера: True - включен, False - выключен
        self.lidar_range = 150  # Дальность зрения лазера (в пикселях)
                
        # --- ИГРОВЫЕ ПЕРЕМЕННЫЕ ---
        self.robot_x = 50        # Текущая координата робота по X
        self.robot_y = 0         # Высота робота (0 - на земле)
        self.is_jumping = False  # Флаг прыжка
        self.jump_time = 0       # Таймер прыжка
        
        self.obstacle_x = 350    # Координата препятствия
        self.finish_x = 550      # Координата финиша
        self.episode = 1         # Номер попытки
        self.is_running = False  # Бежит ли симуляция сейчас
        
        # --- БЛОК ПАМЯТИ ИИ ---
        self.memory_max_slots = 50  # Вместимость памяти (50 успешных прыжков)
        self.victory_archive = []   # Архив координат успешных прыжков
        self.error_history = []  # Список для хранения истории ошибок (MSE) с каждым шагом
        
        # Мозг ИИ (Q-таблица)        
        # Мозг ИИ (Таблица вероятностей для каждой точки X от 0 до 600 с шагом 10)
        # Для каждой точки есть 2 действия: 0 - бежать, 1 - прыгнуть
        # Изначально веса (ценность действий) равны нулю
        self.q_table = {}
        for x in range(0, 610, 10):
            self.q_table[x] = [0.0, 0.0]  # [Вес_Бега, Вес_Прыжка]

        # --- ЛЕВАЯ ПАНЕЛЬ С ВКЛАДКАМИ ---
        left_frame = ttk.Frame(root, padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # ================= ВКЛАДКА 1: УПРАВЛЕНИЕ =================
        self.tab_control = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_control, text="🕹️ Управление ИИ")
        
        # Ползунок скорости обучения (Альфа в формулах ИИ)
        ttk.Label(self.tab_control, text="Скорость обучения ИИ (Интеллект):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.lr_slider = ttk.Scale(self.tab_control, from_=0.1, to=1.0, value=0.5, orient=tk.HORIZONTAL)
        self.lr_slider.pack(fill=tk.X, pady=(0, 15))
        
        # Кнопки старта и сброса мозга
        self.btn_start = ttk.Button(self.tab_control, text="▶️ Запустить обучение ИИ", command=self.toggle_simulation)
        self.btn_start.pack(fill=tk.X, pady=3)
        
        self.btn_reset = ttk.Button(self.tab_control, text="🔄 Стереть память ИИ", command=self.reset_brain)
        self.btn_reset.pack(fill=tk.X, pady=3)
        self.btn_lidar_toggle = ttk.Button(self.tab_control, text="🟢 Лазерное зрение: ВКЛ", command=self.toggle_lidar)
        self.btn_lidar_toggle.pack(fill=tk.X, pady=3)  

        self.btn_move_obstacle = ttk.Button(self.tab_control, text="🔀 Переместить шип (Хаос)", command=self.move_obstacle_randomly)
        self.btn_move_obstacle.pack(fill=tk.X, pady=3)      
        # Табло приборов ИИ
        self.result_frame = ttk.LabelFrame(self.tab_control, text=" 📊 Статистика нейросети ", padding=10)
        self.result_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.lbl_episode = ttk.Label(self.result_frame, text="Попытка (Эпоха): №1", font=("Arial", 10, "bold"))
        self.lbl_episode.pack(anchor=tk.W, pady=2)
        self.lbl_status = ttk.Label(self.result_frame, text="Статус: ИИ пока ничего не знает", font=("Arial", 10), foreground="purple")
        self.lbl_status.pack(anchor=tk.W, pady=2)

        self.lbl_lidar = ttk.Label(self.result_frame, text="Лазерный дальномер: 👁️ Вижу преграду!", font=("Arial", 10), foreground="darkred")
        self.lbl_lidar.pack(anchor=tk.W, pady=2)

        self.lbl_prob = ttk.Label(self.result_frame, text="Шанс прыжка в этой точке: —", font=("Arial", 10, "bold"), foreground="darkgreen")
        self.lbl_prob.pack(anchor=tk.W, pady=2)

        # Математический калькулятор нейросети с вашей картинки
        self.lbl_math_line = ttk.Label(self.result_frame, text="Линейная функция (y = Wx + b): —", font=("Courier", 9))
        self.lbl_math_line.pack(anchor=tk.W, pady=2)

        self.lbl_math_sig = ttk.Label(self.result_frame, text="Сигмоида S(y): —", font=("Courier", 9, "bold"), foreground="darkgreen")
        self.lbl_math_sig.pack(anchor=tk.W, pady=2)

        self.lbl_math_mse = ttk.Label(self.result_frame, text="Ошибка потерь (MSE): —", font=("Courier", 9), foreground="darkred")
        self.lbl_math_mse.pack(anchor=tk.W, pady=2)

        # ИНДИКАТОР ЖЕСТКОГО ДИСКА И ПАМЯТИ РОБОТА
        ttk.Label(self.result_frame, text="💾 Заполнение флеш-памяти побед:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(8, 2))
        self.memory_progress = ttk.Progressbar(self.result_frame, orient=tk.HORIZONTAL, length=200, mode='determinate', max=self.memory_max_slots)
        self.memory_progress.pack(fill=tk.X, pady=2)

        self.lbl_memory_text = ttk.Label(self.result_frame, text="Занято: 0 / 50 слотов (0.0 Мб / 1.0 Мб)", font=("Arial", 9, "italic"), foreground="blue")
        self.lbl_memory_text.pack(anchor=tk.W, pady=(0, 2))
        # Шпаргалка для учителя
        hint_frame = ttk.LabelFrame(self.tab_control, text=" 💡 Что показать ученикам ", padding=10)
        hint_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        self.txt_hint = tk.Text(hint_frame, wrap=tk.WORD, font=("Arial", 9), width=38, height=8, bg="#f9f9f9", bd=0)
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_lesson_hints()

        # ================= ВКЛАДКА 2: ИСТОРИЯ НАУКИ =================
        self.tab_history = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_history, text="📜 Как устроен мозг ИИ?")
        
        history_scroll = ttk.Scrollbar(self.tab_history)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.txt_history = tk.Text(
            self.tab_history, wrap=tk.WORD, font=("Arial", 10), 
            width=38, bg="#fffdf5", bd=0, yscrollcommand=history_scroll.set
        )
        self.txt_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scroll.config(command=self.txt_history.yview)
        
        self.show_ai_history()

        # ================= ВКЛАДКА 3: ЛИТЕРАТУРА ПО ИИ =================
        self.tab_library = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_library, text="📚 Литература по ИИ")
        
        # Скроллбар для удобного листания библиотеки
        library_scroll = ttk.Scrollbar(self.tab_library)
        library_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Текстовое поле для вывода списка книг
        self.txt_library = tk.Text(
            self.tab_library, wrap=tk.WORD, font=("Arial", 9), 
            width=38, bg="#f5fff5", bd=0, yscrollcommand=library_scroll.set
        )
        self.txt_library.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        library_scroll.config(command=self.txt_library.yview)
        
        # Загружаем список книг в текстовое поле
        self.show_ai_library()

        # --- ПРАВАЯ ПАНЕЛЬ С ГРАФИКАМИ (MATPLOTLIB) ---
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Рисуем 3 графика один под другим (Игра, Мысли ИИ с шипом, Ошибка MSE)
        self.fig, (self.ax_game, self.ax_brain, self.ax_error) = plt.subplots(
            3, 1, figsize=(7, 8), gridspec_kw={'height_ratios': [1, 1, 1]}
        )
        self.fig.tight_layout(pad=3.0)

        # Два графика: сверху сама игра, снизу — график изменения вероятностей
        # self.fig, (self.ax_game, self.ax_brain) = plt.subplots(2, 1, figsize=(7, 8), gridspec_kw={'height_ratios': [1, 1.2]})
        # self.fig.tight_layout(pad=4.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Первичная отрисовка сцены
        self.draw_scene()
        self.update_simulation_loop()

    # --- Базовые математические формулы  ---
    @staticmethod
    def sigmoid(x):
        # Формула с картинки: S(x) = 1 / (1 + e^(-x))
        return 1 / (1 + np.exp(-np.clip(x, -10, 10)))

    @staticmethod
    def mean_squared_error(target, predicted):
        # Функция потерь (MSE): разница между идеалом и ответом сети в квадрате
        return (target - predicted) ** 2

    def toggle_lidar(self):
        self.lidar_enabled = not self.lidar_enabled
        if self.lidar_enabled:
            self.btn_lidar_toggle.config(text="🟢 Лазерное зрение: ВКЛ")
            self.lbl_lidar.config(text="Лазер: Активирован", foreground="darkgreen")
        else:
            self.btn_lidar_toggle.config(text="🔴 Лазерное зрение: ВЫКЛ")
            self.lbl_lidar.config(text="Лазер: ОТКЛЮЧЕН (Робот слеп)", foreground="gray")
        self.draw_scene()  # Сразу перерисовываем картинку, чтобы луч исчез или появился
        
    def show_lesson_hints(self):
        self.txt_hint.insert(tk.END, 
            "🧠 СУТЬ ЭКСПЕРИМЕНТА:\n"
            "Зелёный кубик — это робот с ИИ. Он пытается добежать до финиша. "
            "Изначально он НЕ знает, где стоит красная преграда [1].\n\n"
            "🎲 ВЕРОЯТНОСТИ В ДЕЙСТВИИ:\n"
            "На первых секундах робот прыгает где попало — это чистая случайность. Но врезаясь, он "
            "понимает: 'В этой точке прыгать поздно!' (график вероятностей внизу падает).\n\n"
            "📈 ПОБЕДА МАТЕМАТИКИ:\n"
            "Через 8-12 аварий ИИ вычислит идеальную точку для прыжка, и график вероятностей покажет красивый пик ровно перед преградой!"
        )
        self.txt_hint.config(state=tk.DISABLED)

    def show_ai_history(self):
        history_text = (
            "📜 КАК СВЯЗАНЫ ГРАФЫ, ВЕРОЯТНОСТЬ И ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ?\n\n"
            "Когда дети слышат слово 'Нейросеть', они думают о фантастических роботах. "
            "Но внутри любого ИИ сидят обычные школьные Графы и Теория Вероятностей!\n\n"
            
            "🕸️ 1. ВЕСЬ МИР — ЭТО ГРАФ\n"
            "Для нашего робота линия, по которой он бежит — это граф. Каждые 10 сантиметров пути "
            "— это ВЕРШИНА графа. А шаги влево, вправо или прыжки — это РЁБРА (переходы). "
            "ИИ видит мир как огромную карту дорог, где ему нужно найти правильный маршрут.\n\n"
            
            "🎲 2. МОЗГ ИИ — ЭТО ТАБЛИЦА ВЕРОЯТНОСТЕЙ\n"
            "У робота нет глаз. У него есть таблица (Q-таблица), где для каждой точки пути записано: "
            "с каким шансом тут нужно прыгнуть, а с каким — просто бежать. В самом начале шансы равны 50 на 50. "
            "Робот совершает шаги вслепую, бросая внутреннюю виртуальную монетку.\n\n"
            
            "🍖 3. МЕТОД КНУТА И ПРЯНИКА (Обучение с подкреплением)\n"
            "ИИ учится как собака, которую дрессируют:\n"
            "• Если робот прыгнул вовремя и перелетел преграду — математический алгоритм хвалит его "
            "и УВЕЛИЧИВАЕТ вероятность прыжка в этой точке на будущее (записывает плюс в таблицу).\n"
            "• Если робот врезался — алгоритм наказывает его штрафом. Шанс прыгнуть слишком рано или слишком "
            "поздно падает до нуля.\n\n"
            "Именно так современные нейросети учатся играть в шахматы, управлять беспилотными автомобилями Тесла "
            "и генерировать ответы в ChatGPT. Они миллионы раз ошибаются в виртуальном пространстве, чтобы "
            "найти идеальные вероятности для правильных решений!"
        )
        self.txt_history.insert(tk.END, history_text)
        self.txt_history.config(state=tk.DISABLED)

    def toggle_simulation(self):
        self.is_running = not self.is_running
        self.btn_start.config(text="⏸️ Поставить на паузу" if self.is_running else "▶️ Запустить обучение ИИ")
    def move_obstacle_randomly(self):
        # Генерируем случайную координату для шипа в диапазоне от 200 до 480
        # (чтобы он не стоял слишком близко к старту или финишу)
        self.obstacle_x = random.randint(200, 480)
        
        # Выводим сообщение на табло статуса
        self.lbl_status.config(text=f"Статус: 🔀 Шип телепортировался на отметку {self.obstacle_x} см!", foreground="darkblue")
        
        # Мгновенно перерисовываем сцену, чтобы ребёнок увидел прыжок шипа
        self.draw_scene()
    def reset_brain(self):
        self.is_running = False
        self.btn_start.config(text="▶️ Запустить обучение ИИ")
        self.robot_x = 50
        self.robot_y = 0
        self.is_jumping = False
        self.episode = 1
        self.victory_archive = []
        self.error_history = []  # Очищаем график ошибки при сбросе
        for x in self.q_table:
            self.q_table[x] = [0.0, 0.0]
        self.lbl_episode.config(text="Попытка (Эпоха): №1")
        self.lbl_status.config(text="Статус: Память очищена. Архив пуст.", foreground="purple")
        self.memory_progress.config(value=0)
        self.lbl_memory_text.config(text="Занято: 0 / 50 слотов (0.0 Мб / 1.0 Мб)")
        self.draw_scene()

    def update_simulation_loop(self):
        if self.is_running:
            # 1. Определяем текущее состояние (округляем X до десятков, чтобы попасть в вершины графа)
            # --- РАБОТА МОЗГА: СЛЕПОЙ ИЛИ ЗРЯЧИЙ ---
            state_x = int(round(self.robot_x, -1))
            if state_x > 600: state_x = 600

            if self.lidar_enabled:
                # --- РЕЖИМ 1: ЛАЗЕР ВКЛЮЧЕН (Ориентируемся по зрению) ---
                distance_to_obstacle = self.obstacle_x - self.robot_x
                if 0 < distance_to_obstacle <= self.lidar_range:
                    current_state = int(round(distance_to_obstacle, -1))
                    self.lbl_lidar.config(text=f"Лазер: ⚠️ Преграда! Дистанция: {current_state} см", foreground="red")
                else:
                    current_state = 999  # Путь чист
                    self.lbl_lidar.config(text="Лазер: 🟢 Путь чист", foreground="darkgreen")
            else:
                # --- РЕЖИМ 2: ЛАЗЕР ВЫКЛЮЧЕН (Робот слеп, ориентируется по координате X) ---
                current_state = state_x
                self.lbl_lidar.config(text="Лазер: ❌ ОТКЛЮЧЕН (Робот слеп)", foreground="gray")

            # Берем веса из таблицы для текущего состояния (будь то зрение или координата X)
            if current_state not in self.q_table:
                self.q_table[current_state] = [0.0, 0.0]

            q_values = self.q_table[current_state]
            
            # --- ИИ ВЫБИРАЕТ ДЕЙСТВИЕ (Политика вероятностей) ---
            # Переводим веса Q-таблицы в вероятности с помощью алгоритма Softmax (или простого выбора лучшего)
            # Чтобы ИИ иногда рисковал и пробовал новое, добавим элемент случайного поиска (Epsilon-greedy)
            # q_values = self.q_table.get(state_x, [0.0, 0.0])
            
            if random.random() < 0.15:  # 15% шанс сделать абсолютно случайный выбор (исследование мира)
                action = random.choice([0, 1])
            else:  # В остальных случаях выбираем действие с наибольшим математическим весом
                action = np.argmax(q_values)
            
            # Логика прыжка
            if action == 1 and not self.is_jumping:
                self.is_jumping = True
                self.jump_time = 0
                
            # --- ДВИЖЕНИЕ ФИГУРЫ ПО ПРЯМОЙ СЛЕВА НАПРАВО ---
            self.robot_x += 12  # Скорость бега робота
            
            if self.is_jumping:
                # Параболическая траектория прыжка вверх-вниз
                self.jump_time += 1
                self.robot_y = 40 * np.sin(np.pi * self.jump_time / 10)
                if self.jump_time >= 10:
                    self.is_jumping = False
                    self.robot_y = 0
            else:
                self.robot_y = 0
                
            # Выводим текущий шанс прыжка на табло
            # Рассчитаем примерную вероятность для отображения
            # diff = q_values[1] - q_values[0]
            # display_prob = 1 / (1 + np.exp(-diff))  # Функция Сигмоида для красивого процента
            # self.lbl_prob.config(text=f"Шанс прыгнуть in X={state_x}: {display_prob:.1%}")

            # --- ВЫЧИСЛЕНИЕ ПО КАРТИНКЕ: ЛИНЕЙНАЯ ФУНКЦИЯ И СИГМОИДА ---
            # W — это разница весов (ценность прыжка), x — наше состояние
            weight_diff = q_values[1] - q_values[0]
            
            # Линейная функция: y = Wx + b (в нашем случае b = 0 для простоты понимания)
            linear_output = weight_diff
            
            # Сигмоида сжимает любое число в диапазон от 0 до 1 (вероятность прыжка)
            display_prob = self.sigmoid(linear_output)
            
            # Вычисляем текущую ошибку (MSE). Идеал — это 1.0 (если надо прыгать) или 0.0 (если надо бежать)
            # Если робот близко к шипу, идеал прыжка = 1.0. Если далеко — идеал = 0.0
            is_near_obstacle = 1.0 if (0 < (self.obstacle_x - self.robot_x) <= self.lidar_range) else 0.0
            current_mse = self.mean_squared_error(is_near_obstacle, display_prob)
            
            # Обновляем математические надписи на левой панели для ребенка
            self.lbl_math_line.config(text=f"Линейная: y = {linear_output:.2f}")
            self.lbl_math_sig.config(text=f"Сигмоида S(y): {display_prob:.1%}")
            self.lbl_math_mse.config(text=f"Ошибка (MSE): {current_mse:.4f}")

            # ВАЖНО: Добавьте эту строчку, чтобы ошибка записывалась КАЖДЫЙ ТАКТ движения робота!
            self.error_history.append(current_mse)
            
            self.lbl_prob.config(text=f"Шанс прыгнуть в X={state_x}: {display_prob:.1%}")

            # --- ПРОВЕРКА СТОЛКНОВЕНИЯ (КНУТ И ПРЯНИК) ---
            learning_rate = self.lr_slider.get()
            
            # Если робот задел препятствие (попал в зону по X, но не прыгнул достаточно высоко по Y)
            if abs(self.robot_x - self.obstacle_x) < 20 and self.robot_y < 25:
                self.lbl_status.config(text="Статус: 💥 БУМ! ИИ врезался и получил штраф!", foreground="red")
                self.error_history.append(current_mse)  # Записываем ошибку раунда в архив
                # Наказываем ИИ: уменьшаем вес того действия, которое привело к аварии
                self.q_table[state_x][action] += learning_rate * (-100 - self.q_table[state_x][action])
                # --- ОЗВУЧКА АВАРИИ ("Ой!") ---
                # winsound.Beep(Частота в Герцах, Длительность в миллисекундах)
                # Делаем быстрый нисходящий звук, похожий на мультяшный возглас досады
                winsound.Beep(600, 120)  # Первый короткий писк
                winsound.Beep(350, 180)  # Второй писк ниже тоном (эффект "Оу...")
                # Перезапускаем попытку
                self.robot_x = 50
                self.robot_y = 0
                self.is_jumping = False
                self.episode += 1
                self.lbl_episode.config(text=f"Попытка (Эпоха): №{self.episode}")
                
            # Если робот успешно добрался до финиша
            elif self.robot_x >= self.finish_x:
                self.lbl_status.config(text="Статус: 🎉 ПОБЕДА! ИИ добежал и получил награду!", foreground="green")
                
                # Хвалим ИИ во всех точках, где он прыгал во время этого успешного раунда
                self.q_table[state_x][action] += learning_rate * (120 - self.q_table[state_x][action])
                self.error_history.append(current_mse)  # Записываем ошибку раунда в архив
                # --- ОЗВУЧКА ПОБЕДЫ ("Ура! Потрясающе!") ---
                # Делаем быстрый восходящий мажорный аккорд (эффект победных фанфар)
                try:
                    winsound.Beep(523, 100)  # Нота До (C5) - короткий старт
                    winsound.Beep(659, 100)  # Нота Ми (E5) - подъем
                    winsound.Beep(784, 250)  # Нота Соль (G5) - торжественный финал
                except:
                    pass  # Защита на случай, если отключена аудиослужба Windows
                
                # Записываем победу в наш флеш-накопитель, если лимит не исчерпан
                if len(self.victory_archive) < self.memory_max_slots:
                    self.victory_archive.append(self.robot_x)
                    
                # Обновляем графический индикатор памяти на экране
                slots_filled = len(self.victory_archive)
                self.memory_progress.config(value=slots_filled)
                mb_size = slots_filled * 0.02  # Имитируем размер данных (20 Кб на один слот)
                self.lbl_memory_text.config(text=f"Занято: {slots_filled} / 50 слотов ({mb_size:.2f} Мб / 1.0 Мб)")


                # Телепортируем на старт для следующего раунда обучения                
                self.robot_x = 50
                self.robot_y = 0
                self.is_jumping = False
                self.episode += 1
                self.lbl_episode.config(text=f"Попытка (Эпоха): №{self.episode}")
            
            # Рисуем обновленную картинку
            self.draw_scene()
            
        # Зацикливаем анимацию (каждые 40 миллисекунд)
        self.root.after(40, self.update_simulation_loop)

    def draw_scene(self):
        # 1. График 1: Визуализация самой игры
        # =================================================================
        # 1. ВЕРХНИЙ ЭТАЖ (self.ax_game): Симулятор самой игры
        # =================================================================
        self.ax_game.clear()
        
        # Рисуем землю (дорогу-граф)
        self.ax_game.axhline(0, color="black", linewidth=2)
        
        # Рисуем Финиш
        self.ax_game.axvline(self.finish_x, color="gold", linestyle="--", linewidth=2)
        self.ax_game.text(self.finish_x - 15, 50, "ФИНИШ 🏁", fontsize=9, fontweight="bold", color="darkgoldenrod")
        
        # Рисуем Препятствие (красный треугольник)
        self.ax_game.plot([self.obstacle_x-10, self.obstacle_x, self.obstacle_x+10], [0, 30, 0], color="red", linewidth=3)
        self.ax_game.fill([self.obstacle_x-10, self.obstacle_x, self.obstacle_x+10], [0, 30, 0], color="red", alpha=0.6)
        
        # Рисуем Робота ИИ (зелёный квадрат)
        self.ax_game.plot(self.robot_x, self.robot_y + 6, "gs", markersize=14, markeredgecolor="black")
        
        self.ax_game.set_xlim(0, 600)
        self.ax_game.set_ylim(-10, 70)
        self.ax_game.set_title("1. Симулятор: Робот учится прыгать методом проб и ошибок", fontsize=11, fontweight="bold")
        self.ax_game.axis("off")  # Прячем оси координат для красоты игры
        
        # 2. График 2: График вероятностей (Мысли ИИ)
        # self.ax_brain.clear()
        
        # x_points = sorted(list(self.q_table.keys()))
        # prob_values = []
        
        # for x in x_points:
        #     q = self.q_table[x]
        #     diff = q[1] - q[0]
        #     p = 1 / (1 + np.exp(-diff))  # Переводим веса в вероятность от 0 до 1
        #     prob_values.append(p * 100)
            
        # self.ax_brain.plot(x_points, prob_values, color="darkgreen", linewidth=2.5, label="Вероятность прыжка в этой точке")
        # self.ax_brain.fill_between(x_points, prob_values, color="lightgreen", alpha=0.3)
        
        # Отмечаем вертикальной линией преграду на графике мозга
        # self.ax_brain.axvline(self.obstacle_x, color="red", linestyle=":", label="Где стоит преграда")
        
        # self.ax_brain.set_xlim(0, 600)
        # self.ax_brain.set_ylim(-5, 105)
        # self.ax_brain.set_xlabel("Координата пути (Вершины графа X)")
        # self.ax_brain.set_ylabel("Шанс нажать кнопку 'Прыжок' (%)")
        # self.ax_brain.set_title("2. Мысли ИИ: Как нейросеть распределяет вероятности в пути", fontsize=11, fontweight="bold")
        # self.ax_brain.grid(True, linestyle=":", alpha=0.6)
        # self.ax_brain.legend(loc="upper left")

        
        # --- 2. СРЕДНИЙ ГРАФИК (ВОЗВРАЩЕННЫЙ!): Мысли ИИ и ШИПИК ---
        # =================================================================
        # 2. СРЕДНИЙ ЭТАЖ (self.ax_brain): Карта памяти ИИ и КРАСНЫЙ ШИПИК
        # =================================================================
        self.ax_brain.clear()
        
        # Строим распределение вероятностей по всей длине пути (0-600)
        x_points = range(0, 610, 10)
        prob_values = []
        
        for x in x_points:
            # Проверяем, что у ИИ записано в памяти для этой координаты
            if self.lidar_enabled:
                # Если лазер включен, проецируем зрение на карту для наглядности ребенка
                dist = self.obstacle_x - x
                state = int(round(dist, -1)) if (0 < dist <= self.lidar_range) else 999
            else:
                state = x
                
            q = self.q_table.get(state, [0.0, 0.0])
            diff = q[1] - q[0]
            p = self.sigmoid(diff)
            prob_values.append(p * 100)
            
        self.ax_brain.plot(x_points, prob_values, color="darkgreen", linewidth=2.5, label="Шанс прыжка в этой точке")
        self.ax_brain.fill_between(x_points, prob_values, color="lightgreen", alpha=0.3)
        
        # ВОЗВРАЩАЕМ КРАСНЫЙ ШИПИК НА ГРАФИК МОЗГА!
        self.ax_brain.axvline(self.obstacle_x, color="red", linestyle="--", linewidth=2, label="Здесь стоит ШИП 🔺")
        
        self.ax_brain.set_xlim(0, 600)
        self.ax_brain.set_ylim(-5, 105)
        self.ax_brain.set_ylabel("Шанс прыжка (%)")
        self.ax_brain.set_title("2. Карта памяти ИИ (Зеленый пик покажет, где робот научился прыгать)", fontsize=10, fontweight="bold")
        self.ax_brain.grid(True, linestyle=":", alpha=0.6)
        self.ax_brain.legend(loc="upper left")


        # --- ГРАФИК 3: ГРАФИК ОШИБКИ (MSE) С КАРТИНКИ ---
        # =================================================================
        # 3. НИЖНИЙ ЭТАЖ (self.ax_error): График ошибки (MSE) 
        # =================================================================
        # self.ax_brain.clear()
        self.ax_error.clear() # Очищаем именно ТРЕТЬЮ ось!
        
        if self.error_history:
            # Рисуем, как уменьшается ошибка с каждым шагом обучения
            # Ограничим отображение последними 300 точками, чтобы график не тормозил
            plot_data = self.error_history[-300:]
            episodes_range = range(1, len(self.error_history) + 1)
            self.ax_brain.plot(episodes_range, self.error_history, color="red", linewidth=2, label="Текущая ошибка (MSE)")
            self.ax_brain.fill_between(episodes_range, self.error_history, color="red", alpha=0.1)
        else:
            self.ax_brain.text(0.5, 0.5, "Ожидание первых шагов обучения...", ha='center', va='center')
            
        # ВОЗВРАЩАЕМ КРАСИВЫЕ ОРИЕНТИРЫ: линия преграды и финиша для сопоставления масштаба
        # Так как график ошибки строится по шкале попыток (эпох), мы можем нарисовать горизонтальные 
        # или вертикальные маркеры базовых уровней, чтобы график не казался пустым
        self.ax_brain.axhline(0.25, color="gray", linestyle=":", alpha=0.5, label="Допустимый шум")
        self.ax_brain.axhline(0.0, color="green", linestyle="--", alpha=0.7, label="Идеальное обучение (Ошибка = 0)")
              
        self.ax_brain.set_xlim(1, max(20, len(self.error_history)))
        self.ax_brain.set_ylim(-0.05, 1.05)
        self.ax_brain.set_xlabel("Номер попытки (Шаг обучения)")
        self.ax_brain.set_ylabel("Величина ошибки по MSE")
        self.ax_brain.set_title("2. График ошибки: Визуализация исправления ошибок нейросетью", fontsize=11, fontweight="bold")
        self.ax_brain.grid(True, linestyle=":", alpha=0.6)
        self.ax_brain.legend(loc="upper right")
        # --- РИСУЕМ ЛАЗЕРНЫЙ ЛУЧ ИЗ ГЛАЗА РОБОТА (Только если он включен) ---
        if self.lidar_enabled:
            if 0 < (self.obstacle_x - self.robot_x) <= self.lidar_range:
                self.ax_game.plot([self.robot_x, self.obstacle_x], [self.robot_y + 6, 0], color="red", linestyle="-", linewidth=1.5, alpha=0.8)
                self.ax_game.plot(self.robot_x, self.robot_y + 15, "r*", markersize=8)
            else:
                laser_end = min(self.robot_x + self.lidar_range, 600)
                self.ax_game.plot([self.robot_x, laser_end], [self.robot_y + 6, self.robot_y + 6], color="lime", linestyle=":", linewidth=1)
        
        # Перерисовываем холст в окне Tkinter
        self.canvas.draw()

    def show_ai_library(self):
        self.txt_library.config(state=tk.NORMAL)
        self.txt_library.delete("1.0", tk.END)
        
        library_text = (
            "📚 ЦИФРОВАЯ БИБЛИОТЕКА ИИ ДЛЯ ШКОЛЬНИКА\n"
            "Здесь собраны 20 лучших книг, которые помогут понять, как устроены нейросети, роботы и алгоритмы будущего.\n"
            "Выбирай, читай и развивай свой личный интеллект!\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            "1. «Гёдель, Эшер, Бах: эта бесконечная гирлянда»\n"
            "• Автор: Дуглас Хофштадтер | Год: 1979\n"
            "• О чём: Культовая книга, связывающая математику, рисунки и музыку. Объясняет, как из простых систем рождается разум.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "2. «Об интеллекте»\n"
            "• Автор: Джефф Хокинс | Год: 2004\n"
            "• О чём: Книга от создателя карманных компьютеров. Доступно объясняет, как работает кора человеческого мозга и как по её образу построить настоящий ИИ.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "3. «Искусственный интеллект: Современный подход»\n"
            "• Авторы: Стюарт Рассел, Питер Норвиг | Год: 2010\n"
            "• О чём: Главный мировой учебник по ИИ (библия программистов). Отлично подойдёт для тех, кто хочет изучить все алгоритмы от А до Я.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "4. «Верховный алгоритм»\n"
            "• Автор: Педро Домингос | Год: 2015\n"
            "• О чём: Увлекательный путеводитель по 5 школам машинного обучения. Рассказывает, как учёные ищут один универсальный алгоритм для познания всего.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "5. «Оружие математического поражения»\n"
            "• Автор: Кэти О'Нил | Год: 2016\n"
            "• О чём: Математик рассказывает, как большие данные и алгоритмы ИИ могут незаметно управлять нашей жизнью, рекламой и оценками.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "6. «Искусственный интеллект. Эта книга знает о тебе всё»\n"
            "• Автор: Тоби Уолш | Год: 2017\n"
            "• О чём: Живой рассказ о том, обойдут ли роботы людей, отнимут ли они работу и как ИИ изменит школы и университеты к 2050 году.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "7. «Наша математическая Вселенная»\n"
            "• Автор: Макс Тегмарк | Год: 2017\n"
            "• О чём: Профессор MIT объясняет, почему весь наш мир — это огромная математическая структура, похожая на компьютерную программу.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "8. «Глубокое обучение. Легковесный подход»\n"
            "• Авторы: Анураг Бхарвадж и др. | Год: 2018\n"
            "• О чём: Идеальная книга для старта в программировании нейросетей на Python без сложных формул высшей математики.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "9. «Жизнь 3.0. Быть человеком в эпоху ИИ»\n"
            "• Автор: Макс Тегмарк | Год: 2018\n"
            "• О чём: Разбор сценариев будущего: станет ли ИИ супер-помощником человечества или заменит людей как вид.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "10. «Сверхинтеллект: пути, опасности, стратегии»\n"
            "• Автор: Ник Бостром | Год: 2018\n"
            "• О чём: Философский бестселлер о том, что произойдет, когда разум компьютера превзойдет человеческий, и как его контролировать.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "11. «Искусственный интеллект и разговорные агенты»\n"
            "• Автор: Игорь Ашманов | Год: 2019\n"
            "• О чём: Рассказ о том, как компьютеры научились понимать человеческий язык, говорить с нами и создавать тексты.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "12. «Глубокое обучение в картинках»\n"
            "• Автор: Джон Крон | Год: 2020\n"
            "• О чём: Визуальный самоучитель по нейросетям. Огромное количество иллюстраций, которые наглядно объясняют сложные алгоритмы.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "13. «Машина генезиса. Как искусственный интеллект переписывает код жизни»\n"
            "• Авторы: Эми Уэбб, Эндрю Хессель | Год: 2022\n"
            "• О чём: О том, как ИИ объединяется с биологией, помогая учёным изобретать новые лекарства и расшифровывать ДНК.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "14. «Тысяча мозгов: Новая теория интеллекта»\n"
            "• Автор: Джефф Хокинс | Год: 2022\n"
            "• О чём: Свежий взгляд на устройство мозга. Помогает понять, почему современный ИИ пока уступает человеку и как сделать его по-настоящему разумным.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "15. «Искусственный интеллект на Python за пару шагов»\n"
            "• Автор: Себастьян Рашка | Год: 2023\n"
            "• О чём: Практическое руководство с готовым кодом для тех, кто хочет обучить свой первый ИИ распознавать картинки или тексты.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "16. «ChatGPT и революция генеративного ИИ»\n"
            "• Автор: Брайан Роеммеле | Год: 2023\n"
            "• О чём: Популярное объяснение того, как устроены большие языковые модели (трансформеры) и как правильно писать промпты.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "17. «Краткая история искусственного интеллекта»\n"
            "• Автор: Майкл Вулдридж | Год: 2023\n"
            "• О чём: Честный и увлекательный рассказ профессора Оксфорда о взлётах и падениях ИИ, от первых ламповых ЭВМ до современных суперкомпьютеров.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "18. «Co-Intelligence: Навыки работы с ИИ»\n"
            "• Автор: Итан Моллик | Год: 2024\n"
            "• О чём: Профессор Уортона рассказывает, как сделать ИИ своим умным напарником в учёбе, творчестве и программировании.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "19. «Нейросети: руководство по созданию будущего»\n"
            "• Автор: Сборник авторов MIT | Год: 2024\n"
            "• О чём: Книга о том, как генеративные нейросети (вроде Midjourney и ChatGPT) меняют искусство, дизайн и программирование прямо сейчас.\n"
            "• Ссылка: https://reparm.ru\n\n"
            
            "20. «Искусственный интеллект. Иллюстрированный путеводитель»\n"
            "• Автор: Лаборатория ИИ | Год: 2025\n"
            "• О чём: Самый свежий интерактивный гид, созданный специально для школьников. Понятные инфографики, разбор Q-learning и нейросетей.\n"
            "• Ссылка: https://reparm.ru\n"
        )
        
        self.txt_library.insert(tk.END, library_text)
        self.txt_library.config(state=tk.DISABLED)

# --- Запуск программы ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AiLearningApp(root)
    root.mainloop()             


import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CalculusRocketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Математический космодром: Производная и Интеграл наглядно!")
        self.root.geometry("1300x820")
        
        # --- ЛЕВАЯ ПАНЕЛЬ С ВКЛАДКАМИ ---
        left_frame = ttk.Frame(root, padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # ================= ВКЛАДКА 1: ЛАБОРАТОРИЯ =================
        self.tab_control = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_control, text="🚀 Центр управления")
        
        # Ползунок управления ускорением/характером движения ракеты
        ttk.Label(self.tab_control, text="Режим работы двигателя (Ускорение):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.engine_slider = ttk.Scale(self.tab_control, from_=0.0, to=4.0, value=1.5, orient=tk.HORIZONTAL, command=self.update_simulation)
        self.engine_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.engine_label = ttk.Label(self.tab_control, text="Мощность: 1.5", font=("Arial", 9, "italic"), foreground="darkred")
        self.engine_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Выбор типа движения
        ttk.Label(self.tab_control, text="Тип полёта ракеты:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5, 3))
        self.motion_type = tk.StringVar(value="accelerated")
        
        r1 = ttk.Radiobutton(self.tab_control, text="Равномерный полёт (Постоянная скорость)", variable=self.motion_type, value="constant", command=self.update_simulation)
        r1.pack(anchor=tk.W, pady=2)
        r2 = ttk.Radiobutton(self.tab_control, text="Разгон ракеты (Скорость растёт)", variable=self.motion_type, value="accelerated", command=self.update_simulation)
        r2.pack(anchor=tk.W, pady=2)
        r3 = ttk.Radiobutton(self.tab_control, text="Торможение/Посадка (Скорость падает)", variable=self.motion_type, value="decelerated", command=self.update_simulation)
        r3.pack(anchor=tk.W, pady=2)
        
        # Табло приборов
        self.result_frame = ttk.LabelFrame(self.tab_control, text=" 📊 Бортовые приборы ракеты ", padding=10)
        self.result_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.txt_height = ttk.Label(self.result_frame, text="Высота (ИНТЕГРАЛ от скорости): —", font=("Arial", 10, "bold"), foreground="darkgreen")
        self.txt_height.pack(anchor=tk.W, pady=2)
        self.txt_speed = ttk.Label(self.result_frame, text="Текущая скорость: —", font=("Arial", 10))
        self.txt_speed.pack(anchor=tk.W, pady=2)
        self.txt_accel = ttk.Label(self.result_frame, text="Ускорение (ПРОИЗВОДНАЯ от скорости): —", font=("Arial", 10, "bold"), foreground="blue")
        self.txt_accel.pack(anchor=tk.W, pady=2)

        # Подсказка для учителя
        self.hint_frame = ttk.LabelFrame(self.tab_control, text=" 💡 Как объяснить это на уроке ", padding=10)
        self.hint_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        self.txt_hint = tk.Text(self.hint_frame, wrap=tk.WORD, font=("Arial", 9), width=38, height=8, bg="#f9f9f9", bd=0)
        self.txt_hint.pack(fill=tk.BOTH, expand=True)

        # ================= ВКЛАДКА 2: ИСТОРИЯ НАУКИ =================
        self.tab_history = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_history, text="📜 История высшей математики")
        
        history_scroll = ttk.Scrollbar(self.tab_history)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.txt_history = tk.Text(
            self.tab_history, wrap=tk.WORD, font=("Arial", 10), 
            width=38, bg="#f5faff", bd=0, yscrollcommand=history_scroll.set
        )
        self.txt_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scroll.config(command=self.txt_history.yview)
        
        self.show_calculus_history()

        # --- ПРАВАЯ ПАНЕЛЬ С ГРАФИКАМИ ---
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(7, 8))
        self.fig.tight_layout(pad=3.5)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Запуск симуляции
        self.update_simulation()

    def show_calculus_history(self):
        history_text = (
            "📜 КАК ПОЯВИЛИСЬ ПРОИЗВОДНАЯ И ИНТЕГРАЛ?\n"
            "Высшее математическое исчисление (калькулюс) родилось из великой научной битвы и разгадки тайн движения Вселенной!\n\n"
            
            "🏛️ ЭПОХА 1: Древняя Греция и бочки с вином (Архимед)\n"
            "• Что происходило:\n"
            "Более 2200 лет назад великий Архимед пытался решать практические задачи: как посчитать объём круглой бочки, "
            "площадь изогнутого крыла или объём шара? Обычные геометрические формулы для этого не подходили, ведь они работали только с ровными линиями.\n\n"
            "• Первая ласточка:\n"
            "Архимед придумал гениальный метод «исчерпания». Чтобы найти площадь круга, он вписывал в него многоугольники. "
            "Он понял: если разбить сложную кривую фигуру на бесконечное количество КРОШЕЧНЫХ ровных кусочков (полосок), "
            "а потом сложить их площади, мы получим точный результат! Это и был первый в истории прообраз ИНТЕГРАЛА.\n\n"
            
            "🍎 ЭПОХА 2: Падающее яблоко и Исаак Ньютон (1660-е годы)\n"
            "• Главный герой:\n"
            "Великий английский физик Исаак Ньютон.\n\n"
            "• Зачем это было нужно:\n"
            "Ньютон изучал движение планет и падающих тел. Математика его времени умела считать только постоянную скорость. "
            "Но когда яблоко летит с дерева, оно ускоряется каждую долю секунды! Ньютону позарез нужен был инструмент, чтобы считать "
            "скорость в конкретный МГНОВЕННЫЙ момент времени.\n\n"
            "• Что он сделал:\n"
            "Ньютон придумал метод «флюксий» (то, что мы сейчас называем ПРОИЗВОДНОЙ). Он мысленно разделил время полёта на микроскопические "
            "мгновения. Назвав производную «скоростью изменения», он смог рассчитать законы гравитации и движение Луны по орбите!\n\n"
            
            "✍️ ЭПОХА 3: Секретные значки Лейбница и Великий Спор (1670-е годы)\n"
            "• Главный герой:\n"
            "Немецкий философ и математик Готфрид Вильгельм Лейбниц.\n\n"
            "• Суть конфликта:\n"
            "Независимо от Ньютона, в Германии Лейбниц пришёл к тем же выводам. Но если Ньютон решал задачи физики, то Лейбниц искал "
            "красивый математический язык. Именно Лейбниц придумал значок интеграла ∫ (это вытянутая латинская буква S — от слова Summa, сумма полосочек) "
            "и обозначение дифференциала dx.\n\n"
            "• Великая битва:\n"
            "Между сторонниками Ньютона и Лейбница разразилась настоящая война! Англия и Европа спорили, кто первым украл у кого идею. "
            "Сегодня учёные признают: они сделали открытие независимо друг от друга. Ньютон первым применил это в физике, а Лейбниц дал миру "
            "удобные символы, по которым мы учимся сегодня.\n\n"
            
            "🛰️ ЭПОХА 4: Современный мир (XX-XXI века)\n"
            "• Зачем это нужно сегодня:\n"
            "Без производной и интеграла инженеры не смогли бы рассчитать траекторию полёта ракет Илона Маска, "
            "авиаконструкторы не спроектировали бы крыло самолёта, а экономисты не умели бы предсказывать пики кризисов. "
            "Производная — это руль, который показывает, куда движется процесс, а Интеграл — это весы, собирающие итоговый результат!"
        )
        self.txt_history.insert(tk.END, history_text)
        self.txt_history.config(state=tk.DISABLED)

    def update_simulation(self, event=None):
        power = round(float(self.engine_slider.get()), 1)
        self.engine_label.config(text=f"Мощность двигателя: {power}")
        
        mode = self.motion_type.get()
        t = np.linspace(0, 10, 100) # Время от 0 до 10 секунд
        
        # Математическое моделирование полёта ракеты
        if mode == "constant":
            # Скорость постоянна (v = const)
            v = np.full_like(t, power * 5)
            # Высота — это ИНТЕГРАЛ (площадь под графиком скорости). Для константы это линейная функция
            y = power * 5 * t
            # Ускорение — это ПРОИЗВОДНАЯ от скорости. Так как скорость не меняется, производная равна 0
            a = np.zeros_like(t)
            hint_type = "constant"
            
        elif mode == "accelerated":
            # Скорость линейно растёт (v = k*t)
            v = power * 2 * t
            # Высота — это ИНТЕГРАЛ от (k*t), получается парабола (y = 0.5 * k * t^2)
            y = 0.5 * (power * 2) * (t**2)
            # Ускорение — это ПРОИЗВОДНАЯ от скорости. Наклон прямой v постоянен и равен k
            a = np.full_like(t, power * 2)
            hint_type = "accelerated"
            
        elif mode == "decelerated":
            # Скорость падает (ракета тормозит)
            max_v = power * 15
            v = max_v - power * 1.5 * t
            v = np.clip(v, 0, None)  # Скорость не может быть отрицательной
            
            # Высота — интеграл от падающей скорости
            y = max_v * t - 0.5 * (power * 1.5) * (t**2)
            
            # Если ракета остановилась, высота застывает
            stop_idx = np.where(v == 0)[0]
            if len(stop_idx) > 0:
                y[stop_idx:] = y[stop_idx[0]]
                
            # Ускорение — производная скорости (отрицательная, так как наклон вниз)
            a = np.full_like(t, -power * 1.5)
            if len(stop_idx) > 0:
                a[stop_idx:] = 0
            hint_type = "decelerated"

        # Обновляем бортовые приборы (показания на последней секунде t=10)
        self.txt_height.config(text=f"Высота (ИНТЕГРАЛ скорости): {y[-1]:.1f} метров 🟩")
        self.txt_speed.config(text=f"Текущая скорость: {v[-1]:.1f} м/с")
        self.txt_accel.config(text=f"Ускорение (ПРОИЗВОДНАЯ скорости): {a[-1]:.1f} м/с² 🟦")

        # Обновляем текст подсказок для урока
        self.update_hints(hint_type, power)

        # --- ОТРИСОВКА 3-Х ГРАФИКОВ (МАТЕМАТИЧЕСКАЯ СВЯЗЬ) ---
        # График 1: ВЫСОТА (ИНТЕГРАЛ)
        self.ax1.clear()
        self.ax1.plot(t, y, color="green", linewidth=2.5)
        self.ax1.fill_between(t, y, color="green", alpha=0.1)
        self.ax1.set_title("1. ВЫСОТА РАКЕТЫ (Результат накопления пути)", fontsize=10, fontweight="bold", color="green")
        self.ax1.set_ylabel("Высота (метры)")
        self.ax1.grid(True, linestyle=":", alpha=0.6)
        
        # График 2: СКОРОСТЬ (ГЛАВНЫЙ ГРАФИК)
        self.ax2.clear()
        self.ax2.plot(t, v, color="darkorange", linewidth=3)
        self.ax2.fill_between(t, v, color="darkorange", alpha=0.2, label="Площадь = Набранная Высота")
        self.ax2.set_title("2. СКОРОСТЬ РАКЕТЫ (Основной процесс)", fontsize=10, fontweight="bold", color="darkorange")
        self.ax2.set_ylabel("Скорость (м/с)")
        self.ax2.grid(True, linestyle=":", alpha=0.6)
        self.ax2.legend(loc="upper left")
        
        # График 3: УСКОРЕНИЕ (ПРОИЗВОДНАЯ)
        self.ax3.clear()
        self.ax3.plot(t, a, color="blue", linewidth=2.5)
        self.ax3.set_title("3. УСКОРЕНИЕ (Крутизна / Наклон графика скорости)", fontsize=10, fontweight="bold", color="blue")
        self.ax3.set_xlabel("Время полёта (секунды)")
        self.ax3.set_ylabel("Ускорение")
        self.ax3.set_ylim(min(np.min(a)-1, -2), max(np.max(a)+1, 5))
        self.ax3.grid(True, linestyle=":", alpha=0.6)
        
        self.canvas.draw()

    def update_hints(self, hint_type, power):
        self.txt_hint.config(state=tk.NORMAL)
        self.txt_hint.delete("1.0", tk.END)
        
        if hint_type == "constant":
            text = (
                "📈 ЧТО ПОКАЗАТЬ ДЕТЯМ:\n"
                "Скорость ракеты постоянна (оранжевая прямая горизонтальна). "
                "Посмотрите на нижний график: Ускорение равно 0! Почему? "
                "Потому что ПРОИЗВОДНАЯ — это скорость изменения. А если скорость не меняется, её производная равна нулю!\n\n"
                "🟩 ИНТЕГРАЛ:\n"
                "Высота (верхний график) растёт равномерно. Закрашенная площадь под графиком скорости — это и есть значение высоты!"
            )
        elif hint_type == "accelerated":
            text = (
                "📈 ЧТО ПОКАЗАТЬ ДЕТЯМ:\n"
                "Мы давим на газ. График скорости идёт круто вверх. "
                "ПРОИЗВОДНАЯ (ускорение) теперь постоянна и больше нуля (синяя линия стабильна на высоте).\n\n"
                "🟩 ИНТЕГРАЛ:\n"
                "Посмотрите на высоту (зелёный график) — она взлетает по дуге (параболе)! "
                "Площадь под разгоняющейся скоростью растёт колоссально быстро. Интеграл накапливает пройденный путь."
            )
        elif hint_type == "decelerated":
            text = (
                "📈 ЧТО ПОКАЗАТЬ ДЕТЯМ:\n"
                "Ракета тормозит. График скорости падает вниз. "
                "Раз наклон направлен вниз, то ПРОИЗВОДНАЯ (синий график) улетает ниже нуля, в МИНУС! Отрицательное ускорение.\n\n"
                "🟩 ИНТЕГРАЛ:\n"
                "Когда скорость доходит до нуля, ракета останавливается. Зелёный график высоты застывает на одной линии. "
                "Новая площадь под скоростью больше не прибавляется, интеграл перестал расти."
            )
            
        self.txt_hint.insert(tk.END, text)
        self.txt_hint.config(state=tk.DISABLED)

# --- Конец класса и запуск программы ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculusRocketApp(root)
    root.mainloop()


import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SuperProbabilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Супер-Лаборатория Вероятностей и Полная История Науки (8 класс)")
        self.root.geometry("1300x820")
        
        # Настройка стилей для красивых кнопок
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Green.TButton", font=("Arial", 10, "bold"), foreground="green")
        self.style.configure("Blue.TButton", font=("Arial", 10, "bold"), foreground="blue")
        
        # --- ЛЕВАЯ ПАНЕЛЬ С ВКЛАДКАМИ ---
        left_frame = ttk.Frame(root, padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # ================= ВКЛАДКА 1: ЛАБОРАТОРИЯ =================
        self.tab_control = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_control, text="🎛️ Лаборатория")
        
        # 1. Ползунок вероятности
        ttk.Label(self.tab_control, text="Теоретическая вероятность 'Орла':", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.prob_slider = ttk.Scale(self.tab_control, from_=0.0, to=1.0, value=0.5, orient=tk.HORIZONTAL, command=self.update_prob_label)
        self.prob_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.prob_label = ttk.Label(self.tab_control, text="Текущее значение: 50.0%", font=("Arial", 9, "italic"), foreground="darkgreen")
        self.prob_label.pack(anchor=tk.W, pady=(0, 12))
        
        # 2. Ползунок количества бросков
        ttk.Label(self.tab_control, text="Количество подбрасываний:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.flips_slider = ttk.Scale(self.tab_control, from_=20, to=1000, value=200, orient=tk.HORIZONTAL, command=self.update_flips_label)
        self.flips_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.flips_label = ttk.Label(self.tab_control, text="Текущее значение: 200 бросков", font=("Arial", 9, "italic"), foreground="darkgreen")
        self.flips_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Кнопки режимов
        ttk.Label(self.tab_control, text="Запуск режимов:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5, 3))
        
        self.btn_normal = ttk.Button(self.tab_control, text="1️⃣ Случайный бросок (Обычный)", command=lambda: self.run_simulation("normal"))
        self.btn_normal.pack(fill=tk.X, pady=2)
        
        self.btn_rerun = ttk.Button(self.tab_control, text="2️⃣ Чистый Хаос (Новая попытка)", command=lambda: self.run_simulation("normal"))
        self.btn_rerun.pack(fill=tk.X, pady=2)
        
        self.btn_ideal = ttk.Button(self.tab_control, text="3️⃣ Идеальный баланс (Без хаоса)", style="Green.TButton", command=lambda: self.run_simulation("ideal"))
        self.btn_ideal.pack(fill=tk.X, pady=2)
        
        self.btn_paradox = ttk.Button(self.tab_control, text="4️⃣ Парадокс игрока (Серия Орлов)", style="Blue.TButton", command=lambda: self.run_simulation("paradox"))
        self.btn_paradox.pack(fill=tk.X, pady=2)
        
        # Табло результатов
        self.result_frame = ttk.LabelFrame(self.tab_control, text=" 📊 Результаты текущего опыта ", padding=10)
        self.result_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.txt_mode = ttk.Label(self.result_frame, text="Режим: —", font=("Arial", 10, "bold"), foreground="purple")
        self.txt_mode.pack(anchor=tk.W, pady=2)
        self.txt_heads = ttk.Label(self.result_frame, text="Выпало Орлов: —", font=("Arial", 10))
        self.txt_heads.pack(anchor=tk.W, pady=2)
        self.txt_tails = ttk.Label(self.result_frame, text="Выпало Решек: —", font=("Arial", 10))
        self.txt_tails.pack(anchor=tk.W, pady=2)
        self.txt_real_p = ttk.Label(self.result_frame, text="Реальная доля Орлов: —", font=("Arial", 10, "bold"))
        self.txt_real_p.pack(anchor=tk.W, pady=4)

        # Подсказка для учителя снизу первой вкладки
        self.hint_frame = ttk.LabelFrame(self.tab_control, text=" 💡 Подсказка для урока ", padding=10)
        self.hint_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        self.txt_hint = tk.Text(self.hint_frame, wrap=tk.WORD, font=("Arial", 9), width=38, height=6, bg="#f9f9f9", bd=0)
        self.txt_hint.pack(fill=tk.BOTH, expand=True)

        # ================= ВКЛАДКА 2: ИСТОРИЯ НАУКИ =================
        self.tab_history = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_history, text="📜 История науки")
        
        # Добавляем прокрутку для большого текста истории
        history_scroll = ttk.Scrollbar(self.tab_history)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.txt_history = tk.Text(
            self.tab_history, wrap=tk.WORD, font=("Arial", 10), 
            width=38, bg="#fffdf5", bd=0, yscrollcommand=history_scroll.set
        )
        self.txt_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scroll.config(command=self.txt_history.yview)
        
        self.show_probability_history() # Загружаем полный текст истории

        # --- ПРАВАЯ ПАНЕЛЬ С ГРАФИКАМИ (MATPLOTLIB) ---
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(7, 7))
        self.fig.tight_layout(pad=4.5)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Первичный автоматический запуск симуляции
        self.run_simulation("normal")

    def update_prob_label(self, val):
        p = float(val)
        self.prob_label.config(text=f"Текущее значение: {p * 100:.1f}%")

    def update_flips_label(self, val):
        n = int(float(val))
        self.flips_label.config(text=f"Текущее значение: {n} бросков")

    def set_hint(self, mode):
        self.txt_hint.config(state=tk.NORMAL)
        self.txt_hint.delete("1.0", tk.END)
        
        hints = {
            "normal": "ОБЫЧНЫЙ РЕЖИМ:\nПокажите ученикам, как на малых бросках график штормит, а на больших (ближе к 1000) синяя линия прижимается к красной теории. Это Закон больших чисел Бернулли!",
            "ideal": "ИДЕАЛЬНЫЙ БАЛАНС:\nМонеты выпадают строго по очереди. Объясните классу: 'Так ошибочно представляют случайность люди без знаний. В жизни идеального баланса с первого броска не бывает!'",
            "paradox": "ПАРАДОКС ИГРОКА:\nПервые 7 раз выпал ТОЛЬКО Орёл (взлет графика). Но монета ничего не 'должна' решке! Дальше идут честные броски, и начальный перекос растворяется в массе новых опытов."
        }
        self.txt_hint.insert(tk.END, hints.get(mode, ""))
        self.txt_hint.config(state=tk.DISABLED)

    def show_probability_history(self):
        # Полный, склеенный и исправленный текст истории без разорванных кавычек
        history_text = (
            "📜 ПОЛНАЯ ИСТОРИЯ ТЕОРИИ ВЕРОЯТНОСТЕЙ\n"
            "Эта наука родилась не в тишине библиотек, а из азартных споров, казино и писем великих учёных!\n\n"
            
            "🏛️ ЭПОХА 1: Древний мир и Средневековье\n"
            "• Что происходило:\n"
            "Люди играли в азартные игры тысячи лет. Древние римляне, египтяне и греки обожали кидать "
            "«астрагалы» (кости из суставов овец или отлитые из бронзы). Но никому в голову не приходило считать шансы математически.\n\n"
            "• В чём была причина:\n"
            "В древности господствовало религиозное мышление. Считалось, что исход броска кости — это не случайность, "
            "а прямая воля богов или слепая судьба. Зачем считать формулы, если всё за тебя решают высшие силы?\n\n"
            "• Первая ласточка:\n"
            "Ближе к XVI веку итальянский математик и заядлый игроман Джироламо Кардано написал книгу "
            "«О кубической игре». Он первым попытался посчитать, сколько всего комбинаций выдают два игральных кубика (36 вариантов) "
            "и сколько из них выигрышные. Но его рукопись потерялась и была опубликована только через сто лет, поэтому революции она не совершила.\n\n"
            
            "🎰 ЭПОХА 2: 1654 год — Рождение науки из писем в казино\n"
            "• Главные герои:\n"
            "Французский дворянин Шевалье де Мере (Антуан Гомбо), физик Блез Паскаль и математик Пьер Ферма.\n\n"
            "• Суть конфликта:\n"
            "Шевалье де Мере был профессиональным игроком и зарабатывал ставками. Он заметил закономерность: "
            "если бросать один кубик 4 раза подряд, то шанс, что хотя бы один раз выпадет «шестерка», составляет чуть больше 50% "
            "(это было выгодно). Де Мере решил масштабировать игру и предложил бросать два кубика одновременно 24 раза подряд, "
            "рассчитывая на такой же успех. Но на практике он начал стремительно проигрывать и банкротиться! Де Мере не понимал ошибки "
            "и в 1654 году написал своему другу — ученому Блезу Паскалю.\n\n"
            "• Что они сделали:\n"
            "Паскаль зажёгся этой задачей и связался по переписке с Пьером Ферма. Решая задачу проигравшегося дворянина, они впервые "
            "в истории сформулировали классическое определение вероятности. Они доказали, что случайность подчиняется законам математики. "
            "Год 1654-й официально считается годом рождения теории вероятностей!\n\n"
            
            "🪙 ЭПОХА 3: XVIII век — Порядок рождается из хаоса\n"
            "• Главный герой:\n"
            "Швейцарский математик Якоб Бернулли.\n\n"
            "• Зачем это было нужно:\n"
            "До Бернулли ученые умели считать только простые шансы в играх (например, шанс вытащить туза). "
            "Но Бернулли хотел применить науку к реальной жизни: к демографии, экономике и страхованию. "
            "Ему нужно было понять, как ведет себя случайность на длинной дистанции.\n\n"
            "• В чём суть открытия:\n"
            "В 1713 году вышла его книга «Искусство предположений». В ней он доказал Закон больших чисел. "
            "Бернулли математически подтвердил: если вы бросите монетку 5 раз — это будет непредсказуемый хаос. "
            "Но если вы бросите её 10 000 раз, то хаос самоуничтожится, и доля орлов будет железно равна 50%. "
            "Массовая случайность предсказуема! Это позволило создавать первые страховые компании: "
            "они не знали, кто конкретно заболеет, но точно знали, сколько людей из тысячи заболеет в среднем.\n\n"
            
            "🛡️ ЭПОХА 4: XX век — Из казино в строгую науку\n"
            "• Главный герой:\n"
            "Советский математик Андрей Николаевич Колмогоров.\n\n"
            "• В чём была проблема:\n"
            "Вплоть до XX века многие ученые относились к теории вероятностей с презрением, считая её "
            "прикладным сборником фокусов для азартных игроков. У неё не было строгого математического фундамента.\n\n"
            "• Что он сделал:\n"
            "В 1933 году Колмогоров написал фундаментальный труд «Основные понятия теории вероятностей», "
            "в котором сформулировал строгую аксиоматику этой науки. Он объединил классические подходы с теорией "
            "множеств и мерой Лебега, превратив вероятность в полноценный раздел высшей математики.\n\n"
            "• Зачем это было нужно:\n"
            "После работы Колмогорова теория вероятностей стала абсолютно признанной и фундаментальной дисциплиной. "
            "Именно благодаря его аксиомам сегодня работают прогнозы погоды, алгоритмы космической навигации, "
            "финансовые биржи, квантовая физика и весь современный искусственный интеллект (нейросети!)."
        )
        self.txt_history.insert(tk.END, history_text)
        self.txt_history.config(state=tk.DISABLED)
    def run_simulation(self, mode):
        p_theoretical = round(float(self.prob_slider.get()), 2)
        n_flips = int(self.flips_slider.get())
        
        if mode == "normal":
            self.txt_mode.config(text="Режим: 🎰 Случайный хаос", foreground="black")
            flips = np.random.choice([1, 0], size=n_flips, p=[p_theoretical, 1 - p_theoretical])
            self.set_hint("normal")
            
        elif mode == "ideal":
            self.txt_mode.config(text="Режим: 📐 Идеальный баланс", foreground="green")
            flips = np.zeros(n_flips, dtype=int)
            heads_count = int(round(n_flips * p_theoretical))
            if heads_count > 0:
                indices = np.linspace(0, n_flips - 1, heads_count, dtype=int)
                flips[indices] = 1
            self.set_hint("ideal")
            
        elif mode == "paradox":
            self.txt_mode.config(text="Режим: 💥 Парадокс игрока", foreground="blue")
            fake_start_len = min(7, n_flips)
            fake_start = np.ones(fake_start_len, dtype=int)
            remaining_len = n_flips - fake_start_len
            if remaining_len > 0:
                random_part = np.random.choice([1, 0], size=remaining_len, p=[p_theoretical, 1 - p_theoretical])
                flips = np.concatenate([fake_start, random_part])
            else:
                flips = fake_start
            self.set_hint("paradox")

        # --- Расчёты математики ---
        total_heads = int(np.sum(flips))
        total_tails = n_flips - total_heads
        p_experimental = total_heads / n_flips
        
        self.txt_heads.config(text=f"Выпало Орлов: {total_heads} шт.")
        self.txt_tails.config(text=f"Выпало Решек: {total_tails} шт.")
        self.txt_real_p.config(text=f"Реальная доля Орлов: {p_experimental:.1%}")
        
        cumulative_heads = np.cumsum(flips)
        trials = np.arange(1, n_flips + 1)
        cumulative_proportions = cumulative_heads / trials
        
        # --- ГРАФИК 1 ---
        self.ax1.clear()
        self.ax1.plot(trials, cumulative_proportions, label="Доля Орлов в эксперименте", color="#1f77b4", linewidth=2.5)
        self.ax1.axhline(p_theoretical, color="red", linestyle="--", label=f"Теория ({p_theoretical:.0%})", linewidth=2)
        self.ax1.set_title("График стабилизации частоты (Закон больших чисел)", fontsize=11, fontweight='bold')
        self.ax1.set_xlabel("Номер броска")
        self.ax1.set_ylabel("Текущая доля Орлов")
        self.ax1.set_ylim(-0.05, 1.05)
        self.ax1.grid(True, linestyle=":", alpha=0.6)
        self.ax1.legend(loc="upper right")
        
        # --- ГРАФИК 2 ---
        self.ax2.clear()
        categories = ['Орёл (Heads)', 'Решка (Tails)']
        experimental_data = [p_experimental, 1 - p_experimental]
        theoretical_data = [p_theoretical, 1 - p_theoretical]
        
        x = np.arange(len(categories))
        width = 0.3
        
        self.ax2.bar(x - width/2, experimental_data, width, label='Практика (Факт)', color='#2ca02c')
        self.ax2.bar(x + width/2, theoretical_data, width, label='Теория (План)', color='#ff7f0e', alpha=0.7)
        
        self.ax2.set_title("Итоговое сравнение: Теория vs Практика", fontsize=11, fontweight='bold')
        self.ax2.set_ylabel('Доля выпадений')
        self.ax2.set_xticks(x)
        self.ax2.set_xticklabels(categories)
        self.ax2.set_ylim(0, 1.05)
        self.ax2.grid(axis='y', linestyle=':', alpha=0.6)
        self.ax2.legend(loc="upper right")
        
        self.canvas.draw()

# --- Конец класса и запуск программы ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SuperProbabilityApp(root)
    root.mainloop()

import tkinter as tk
from tkinterweb import HtmlFrame  # Импортируем веб-компонент

def open_help_window():
    help_win = tk.Toplevel(root)
    help_win.title("Большая справка")
    help_win.geometry("550x450")
    
    # Создаем фрейм, который умеет читать HTML и цветные эмодзи
    frame = HtmlFrame(help_win, messages_enabled=False)
    
    # Пишем текст в формате HTML (теперь все смайлики будут цветными!)
    html_content = """
    <div style="font-family: Arial, sans-serif; padding: 15px; font-size: 15px; line-height: 1.6;">
        <h2 style="text-align: center;">📜 ИНСТРУКЦИЯ ПОЛЬЗОВАТЕЛЯ 📜</h2>
        <p>Привет! 👋 Добро пожаловать в нашу программу.</p>
        
        <h3 style="color: #2e7d32;">🚀 Основные фишки:</h3>
        <ol>
            <li>Работает быстро и без багов ✨</li>
            <li>Интерфейс стал красивым 🥰</li>
            <li>Все смайлики теперь <b>цветные</b>! 🎉🎈</li>
        </ol>
        
        <p style="color: #d32f2f; background-color: #ffebee; padding: 10px; border-left: 5px solid #d32f2f;">
            ⚠️ <b>Внимание:</b> Теперь движок поддерживает полноценный веб-рендеринг!
        </p>
        
        <p style="text-align: center; margin-top: 20px; font-weight: bold;">
            Удачи в кодинге! 🐍💻🔥
        </p>
    </div>
    """
    
    # Загружаем наш HTML-текст в окно
    frame.load_html(html_content)
    frame.pack(fill="both", expand=True)
    
    # Кнопка закрытия
    btn_close = tk.Button(help_win, text="Закрыть ❌", command=help_win.destroy, bg="#ff4d4d", fg="white", font=("Arial", 10))
    btn_close.pack(pady=10)

# --- Главное окно программы ---
root = tk.Tk()
root.title("Мое приложение")
root.geometry("350x220")

# Для главного окна тоже используем мини-html, чтобы стрелочка 👇 была цветной
label_frame = HtmlFrame(root, messages_enabled=False)
label_frame.load_html("""
<p style='font-family: Arial; font-size: 13px; text-align: center; margin: 15px 0 0 0;'>
    Нажмите на кнопку ниже, чтобы<br>открыть справку со смайликами 👇
</p>
""")
label_frame.pack(fill="x")

# Главная кнопочка "Открыть"
btn_open = tk.Button(root, text="ℹ️ Открыть справку", font=("Arial", 12, "bold"), command=open_help_window, bg="#4CAF50", fg="white", padx=10, pady=5)
btn_open.pack(pady=20)

root.mainloop()



import tkinter as tk
from tkinter import messagebox

def open_help_window():
    # Создаем новое отдельное окно для большой справки
    help_win = tk.Toplevel(root)
    help_win.title("Большая справка")
    help_win.geometry("500x400")
    
    # Текст справки (здесь вы можете писать любые смайлики)
    help_text = (
        "📜 ИНСТРУКЦИЯ ПОЛЬЗОВАТЕЛЯ 📜\n\n"
        "Привет! 👋 Добро пожаловать в нашу программу.\n\n"
        "🚀 Основные фишки:\n"
        "1. Работает быстро и без багов ✨\n"
        "2. Интерфейс стал красивым 🥰\n"
        "3. Все смайлики теперь отображаются! 🎉🎈\n\n"
        "⚠️ Внимание: Если у вас старая Windows, "
        "некоторые эмодзи могут быть черно-белыми.\n\n"
        "Удачи в кодинге! 🐍💻🔥"
    )
    
    # Используем виджет Text вместо Canvas, он отлично поддерживает эмодзи!
    text_widget = tk.Text(help_win, wrap="word", font=("Arial", 12), padx=15, pady=15)
    text_widget.insert("1.0", help_text)
    
    # Делаем текст доступным только для чтения, чтобы пользователь его не стёр
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True)
    
    # Кнопка закрытия внутри справки
    btn_close = tk.Button(help_win, text="Закрыть ❌", command=help_win.destroy, bg="#ff4d4d", fg="white")
    btn_close.pack(pady=10)

# --- Главное окно программы ---
root = tk.Tk()
root.title("Мое приложение")
root.geometry("300x200")

# Приветственная надпись
label = tk.Text(root, font=("Arial", 11), height=2, bg=root.cget("bg"), bd=0, highlightthickness=0)
label.insert("1.0", "Нажмите на кнопку ниже, чтобы\nоткрыть справку со смайликами 👇")
label.config(state="disabled")
label.pack(pady=20)

# Главная кнопочка "Открыть"
btn_open = tk.Button(root, text="ℹ️ Открыть справку", font=("Arial", 12, "bold"), command=open_help_window, bg="#4CAF50", fg="white", padx=10, pady=5)
btn_open.pack(pady=10)

root.mainloop()


import tkinter as tk
from tkinter import messagebox, ttk

class GraphFinalExam:
    def __init__(self, root):
        self.root = root
        self.root.title("Финальный зачёт: Проверка знаний по теории графов и ИИ")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        # Пул из 10 вопросов на Да/Нет (на основе истории и теории наших 11 уроков)
        self.questions = [
            {
                "text": "1. Леонард Эйлер в 1736 году доказал, что обойти 7 мостов Кёнигсберга без повторов невозможно, потому что у графа было больше двух нечётных вершин?",
                "correct": True
            },
            {
                "text": "2. Алгоритм Дейкстры (1956 г.) ищет кратчайший путь, ориентируясь исключительно на количество рёбер (шагов), полностью игнорируя пробки и веса дорог?",
                "correct": False  # Ложь, он учитывает веса (время/пробки)
            },
            {
                "text": "3. Согласно схеме Бернулли, при меткости стрелка 70%, вероятность сделать 6 попаданий подряд РАВНА исходным 70%?",
                "correct": False  # Ложь, вероятности перемножаются и шанс падает до ~11.7%
            },
            {
                "text": "4. В двудольных графах связи (рёбра) могут существовать только МЕЖДУ вершинами разных долей, а внутри одной группы вершины соединяться не могут?",
                "correct": True
            },
            {
                "text": "5. Венгерский метод Гарольда Куна (1955 г.) создан для того, чтобы найти распределение задач с МАКСИМАЛЬНО возможной переплатой и растратой бюджета?",
                "correct": False  # Ложь, он ищет минимальный бюджет
            },
            {
                "text": "6. Алгоритм Форда-Фалкерсона (1956 г.) для расчёта максимального потока изначально создавался для секретного анализа железнодорожной сети?",
                "correct": True
            },
            {
                "text": "7. Минимальное остовное дерево (MST) Отакара Борувки (1926 г.) обязательно должно содержать замкнутые петли, циклы и кольца?",
                "correct": False  # Ложь, дерево не имеет циклов
            },
            {
                "text": "8. Метрика центральности по посредничеству Фримена ищет 'Серого кардинала' — узел, через который проходит максимум кратчайших путей в сети?",
                "correct": True
            },
            {
                "text": "9. В модели распространения фейков в интернете, скорость заражения всей сети будет ВЫШЕ, если вирус изначально попадёт на хаб (Лидера мнений)?",
                "correct": True
            },
            {
                "text": "10. Для Задача коммивояжёра (TSP) учёные до сих пор нашли точную и быструю математическую формулу, поэтому компьютеры никогда не зависают при её расчёте?",
                "correct": False  # Ложь, это NP-трудная задача, точной быстрой формулы нет
            }
        ]
        
        self.current_q = 0
        self.score = 0
        
        self.setup_ui()
        self.show_question()

    def setup_ui(self):
        # Главный контейнер с отступами
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Индикатор прогресса
        self.lbl_progress = ttk.Label(self.main_frame, text="Вопрос 1 из 10", font=("Arial", 11, "bold"), foreground="blue")
        self.lbl_progress.pack(anchor=tk.W, pady=(0, 10))
        
        # Окно вопроса
        self.question_frame = ttk.LabelFrame(self.main_frame, text=" Вопрос зачёта ", padding=15)
        self.question_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.lbl_question = tk.Label(
            self.question_frame, 
            text="", 
            font=("Arial", 11), 
            wraplength=600, 
            justify=tk.LEFT,
            anchor=tk.NW
        )
        self.lbl_question.pack(fill=tk.BOTH, expand=True)
        
        # Панель кнопок Да / Нет
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.pack(fill=tk.X, pady=15)
        
        self.btn_yes = tk.Button(
            self.btn_frame, text="🟢 ДА (Правда)", font=("Arial", 11, "bold"), 
            bg="#ccffcc", fg="green", height=2, width=15, command=lambda: self.check_answer(True)
        )
        self.btn_yes.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
        
        self.btn_no = tk.Button(
            self.btn_frame, text="🔴 НЕТ (Ложь)", font=("Arial", 11, "bold"), 
            bg="#ffcccc", fg="red", height=2, width=15, command=lambda: self.check_answer(False)
        )
        self.btn_no.pack(side=tk.RIGHT, padx=20, expand=True, fill=tk.X)

    def show_question(self):
        if self.current_q < len(self.questions):
            self.lbl_progress.config(text=f"Вопрос {self.current_q + 1} из {len(self.questions)}")
            self.lbl_question.config(text=self.questions[self.current_q]["text"])
        else:
            self.show_final_results()

    def check_answer(self, user_choice):
        correct_ans = self.questions[self.current_q]["correct"]
        if user_choice == correct_ans:
            self.score += 1
            
        self.current_q += 1
        self.show_question()

    def show_final_results(self):
        # Очищаем холст вопросов
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Считаем итог
        half_score = len(self.questions) / 2
        is_passed = self.score >= half_score
        
        color = "darkgreen" if is_passed else "darkred"
        verdict = "🎉 ЗАЧЁТ ПОСТАВЛЕН! 🎉" if is_passed else "❌ НЕЗАЧЁТ (Попробуй ещё раз) ❌"
        bg_card = "#e6ffe6" if is_passed else "#ffe6e6"
        
        # Карточка итогов
        res_frame = tk.LabelFrame(self.main_frame, text=" Официальный протокол зачёта ", padx=10, pady=10)
        res_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            res_frame, text=verdict, font=("Arial", 16, "bold"), 
            foreground=color, bg=bg_card, pady=10
        ).pack(fill=tk.X, pady=10)
        
        report = (
            f"• Правильных ответов: {self.score} из {len(self.questions)}\n\n"
            f"• Процент успешности: {int(self.score / len(self.questions) * 100)}%\n\n"
            f"• Статус: {'Курс успешно пройден! Ты настоящий инженер! 👍' if is_passed else 'Не хватило баллов. Прочитай исторические справки в лабах! 📚'}"
        )
        
        ttk.Label(res_frame, text=report, font=("Courier", 11, "bold"), justify=tk.LEFT).pack(anchor=tk.W, pady=10)
        ttk.Button(self.main_frame, text="🔄 Сдать зачёт заново", command=self.restart_exam).pack(fill=tk.X, pady=10)

    def restart_exam(self):
        self.current_q = 0
        self.score = 0
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.setup_ui()
        self.show_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphFinalExam(root)
    root.mainloop()


import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random
import numpy as np

class PowerNetworkOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Урок 11: Экономный Электрик — Минимальное остовное дерево (MST)")
        self.root.geometry("1400x850")
        
        # Обычный ненаправленный граф для карты посёлка
        self.G = nx.Graph()
        self.pos = {}
        self.mst_edges = []
        self.mst_cost = 0
        
        self.setup_ui()
        self.generate_village_map()

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=400)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для графа
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Управление картой
        ttk.Label(self.left_panel, text="🏡 Карта дачного посёлка", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Button(self.left_panel, text="🎲 Разбросать дома по-новому", command=self.generate_village_map).pack(fill=tk.X, pady=5)
        
        # Оптимизация сети
        ttk.Label(self.left_panel, text="⚡ Оптимизация кабелей", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        ttk.Button(self.left_panel, text="✂️ Стереть лишнее и сэкономить бюджет", command=self.solve_mst_kruskal).pack(fill=tk.X, pady=5)
        
        # Финансовый отчёт
        ttk.Label(self.left_panel, text="📊 Финансовая смета инженера:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.lbl_results = ttk.Label(self.left_panel, text="Кабели не проведены.\nВ посёлке темно.", font=("Courier", 10), justify=tk.LEFT, foreground="darkblue")
        self.lbl_results.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # Историческая справка и подсказки
        ttk.Label(self.left_panel, text="📜 Исторический кризис света:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=18, wrap=tk.WORD, font=("Arial", 10), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Настройка Matplotlib Canvas
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "📜 ИСТОРИЯ И СМЫСЛ ЗАДАЧИ:\n"
            "В 1926 году чешский инженер Отакар Борувка решал важнейшую государственную задачу: "
            "как провести электрические кабели ко всем городам и сёлам Западной Моравии. Требовалось, "
            "чтобы все населённые пункты гарантированно получили свет, но при этом длина дорогущего "
            "высоковольтного кабеля была минимально возможной. Борувка создал первый алгоритм поиска "
            "Минимального остовного дерева (MST). Позже, в 1930 и 1956 годах, математики Прим и Краскал "
            "сделали этот расчёт ещё быстрее.\n\n"
            "Суть алгоритма: компьютер изучает граф всех возможных дорог между точками и безжалостно "
            "стирает лишние циклы и петли. Остаётся чистый древовидный каркас — 'скелет' графа, "
            "который связывает абсолютно всех участников, но стоит копейки по протяжённости.\n\n"
            "💼 ГДЕ ПРИМЕНЯЕТСЯ СЕГОДНЯ:\n"
            "• Интернет-провайдерами при прокладке оптоволокна в новые жилые районы.\n"
            "• Инженерами микросхем при проектировании дорожек на процессорах смартфонов (чтобы сигнал "
            "доходил до транзисторов мгновенно, затрачивая минимум кремния)."
        )
        self.txt_hint.config(state=tk.DISABLED)

    def generate_village_map(self):
        self.G.clear()
        self.mst_edges = []
        self.mst_cost = 0
        self.lbl_results.config(text="Дома построены.\nКабели пока не проложены.", foreground="black")
        
        # 9 домов-вершин посёлка
        num_houses = 9
        self.G.add_nodes_from(range(num_houses))
        
        # Фиксируем координаты, чтобы посёлок выглядел аккуратным прямоугольником
        self.pos = {
            0: (0, 2), 1: (1, 4), 2: (1, 0),
            3: (2, 4), 4: (2, 2), 5: (2, 0),
            6: (3, 4), 7: (3, 0), 8: (4, 2)
        }
        
        # Все возможные варианты прокладки кабелей между соседними домами
        connections = [
            (0, 1), (0, 4), (0, 2), (1, 3), (1, 4), (2, 4), (2, 5),
            (3, 6), (3, 4), (5, 4), (5, 7), (6, 8), (4, 8), (7, 8),
            (6, 4), (7, 4)
        ]
        
        # Раздаем случайную стоимость кабеля (от 2 до 15 млн рублей)
        for u, v in connections:
            cost = random.randint(2, 15)
            self.G.add_edge(u, v, weight=cost)
            
        self.draw_village()

    def solve_mst_kruskal(self):
        # САМАЯ ВАЖНАЯ СТРОКА: Запускаем алгоритм Крускала для поиска Минимального остовного дерева
        # Алгоритм за миллисекунду выбирает рёбра с наименьшим весом, которые не создают замкнутых колец
        try:
            mst_subgraph = nx.minimum_spanning_tree(self.G, weight='weight')
            self.mst_edges = list(mst_subgraph.edges())
            
            # Считаем полную стоимость экономичной сети
            self.mst_cost = sum(self.G[u][v]['weight'] for u, v in self.mst_edges)
            
            # Считаем, сколько бы мы потратили, если бы бездумно проложили абсолютно все кабели
            total_possible_cost = sum(self.G[u][v]['weight'] for u, v in self.G.edges())
            money_saved = total_possible_cost - self.mst_cost
            
            # Формируем красивый экономический отчёт
            report = (
                f"⚡ Электросеть посёлка построена!\n\n"
                f"• Финальная смета (MST):\n  {self.mst_cost} млн рублей\n\n"
                f"• Проложено кабелей:\n  {len(self.mst_edges)} шт. (для 9 домов)\n\n"
                f"💰 Выгода оптимизации:\n"
                f"  Сэкономлено: {money_saved} млн руб.!\n"
                f"  Алгоритм убрал все лишние\n"
                f"  замкнутые петли и кольца."
            )
            self.lbl_results.config(text=report, foreground="darkgreen")
            self.draw_village(show_mst=True)
        except Exception as e:
            messagebox.showerror("Ошибка оптимизации", str(e))

    def draw_village(self, show_mst=False):
        self.ax.clear()
        
        # Базовая карта: все возможные дороги (серые тонкие пунктирные линии)
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color="#d0d0d0", width=1.5, style="dashed")
        
        # Если нажали кнопку оптимизации, зажигаем остовное дерево жирным золотисто-оранжевым цветом
        if show_mst and self.mst_edges:
            nx.draw_networkx_edges(
                self.G, self.pos, ax=self.ax, 
                edgelist=self.mst_edges, 
                edge_color="#ff9900", width=5.0, alpha=0.9
            )
            
            # Накладываем маленькие маркеры направления тока по центру (для красоты)
            for u, v in self.mst_edges:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = (x2 - x1) * 0.005, (y2 - y1) * 0.005
                self.ax.annotate("", xy=(cx+dx, cy+dy), xytext=(cx, cy),
                                 arrowprops=dict(arrowstyle="-", color="white", lw=1.5))
                
        # Текстовые подписи стоимости кабелей на линиях (в миллионах)
        edge_labels = { (u, v): f"{self.G[u][v]['weight']} млн" for u, v in self.G.edges() }
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax, font_size=8, font_weight="bold")

        # Рисуем сами домики посёлка (сделаем их уютными светло-зелёными кружками)
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color="#e6ffed", node_size=600, edgecolors="#009933", linewidths=1.5)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=11, font_weight="bold")
        
        self.ax.set_title("--- Карта посёлка | Оранжевые линии — Минимальное остовное дерево кабелей", fontsize=11, fontweight='bold', pad=15)
        self.ax.axis("off")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PowerNetworkOptimizer(root)
    root.mainloop()







import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random
import numpy as np

class WaterFlowSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Урок 10: Симулятор Водоканала — Максимальный поток Форда-Фалкерсона")
        self.root.geometry("1400x850")
        
        # Направленный граф (DiGraph), так как вода течёт строго в одну сторону по трубам
        self.G = nx.DiGraph()
        self.pos = {}
        self.flow_value = 0
        self.flow_dict = {}
        
        self.setup_ui()
        self.generate_pipe_network()

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=400)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для графа
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Управление картой труб
        ttk.Label(self.left_panel, text="🚰 Управление водопроводной сетью", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Button(self.left_panel, text="🎲 Перестроить трубы и лимиты", command=self.generate_pipe_network).pack(fill=tk.X, pady=5)
        
        # Запуск гидро-расчёта
        ttk.Label(self.left_panel, text="⚙️ Инженерный расчёт потока", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        ttk.Button(self.left_panel, text="🌊 Включить насосы и рассчитать поток", command=self.calculate_max_flow).pack(fill=tk.X, pady=5)
        # Кнопка для плавного, анимированного пуска воды
        ttk.Button(self.left_panel, text=" Плавный запуск насосов (Анимация)", command=self.start_animated_flow).pack(fill=tk.X, pady=5)
        
        # Отчёт инженера
        ttk.Label(self.left_panel, text="📊 Сводка главного инженера:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.lbl_results = ttk.Label(self.left_panel, text="Насосы выключены.\nДавление в норме.", font=("Courier", 10), justify=tk.LEFT, foreground="darkblue")
        self.lbl_results.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # Историческая справка и подсказки
        ttk.Label(self.left_panel, text="📜 Секретная история Холодной войны:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=18, wrap=tk.WORD, font=("Arial", 10), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Настройка Matplotlib Canvas
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "📜 ИСТОРИЯ И СМЫСЛ ЗАДАЧИ:\n"
            "In 1954 году, в разгар Холодной войны, американские военные математики Лестер Форд и Делберт Фалкерсон "
            "получили секретное задание от военной корпорации RAND: оценить пропускную способность железнодорожной "
            "сети СССР. Требовалось понять, какое максимальное количество эшелонов с грузом может проехать "
            "из глубины страны к границам Европы за сутки, учитывая ограничения станций и путей.\n\n"
            "В 1956 году они опубликовали знаменитый Алгоритм Форда-Фалкерсона. Этот алгоритм решает "
            "задачу 'узкого горлышка'. Представьте граф как систему водопроводных труб, где у каждого ребра "
            "есть лимит литров в минуту. Задача — пустить из башни в жилые дома максимум воды так, чтобы "
            "ни одна труба не лопнула от перегрузки.\n\n"
            "💼 ГДЕ ПРИМЕНЯЕТСЯ СЕГОДНЯ:\n"
            "• Менеджерами городских водоканалов и нефтепроводов для управления давлением.\n"
            "• Сетевыми инженерами интернета для распределения трафика (чтобы видеохостинги вроде YouTube "
            "не зависали при пиковых нагрузках миллионами пользователей)."
        )
        self.txt_hint.config(state=tk.DISABLED)

    def generate_pipe_network(self):
        self.G.clear()
        self.flow_dict = {}
        self.flow_value = 0
        self.lbl_results.config(text="Новая система труб проложена.\nЖду запуска насосов.", foreground="black")
        
        # 8 узлов: 0 - Водонапорная башня (Исток), 7 - Жилой сектор (Сток)
        nodes = range(8)
        self.G.add_nodes_from(nodes)
        
        # Фиксированные координаты, чтобы граф всегда выглядел аккуратно слоями
        self.pos = {
            0: (0, 2), # Исток
            1: (1, 3), 2: (1, 1),
            3: (2, 4), 4: (2, 2), 5: (2, 0),
            6: (3, 2),
            7: (4, 2)  # Сток
        }
        
        # Набор труб (откуда, куда)
        pipes = [
            (0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (2, 5),
            (3, 6), (4, 6), (5, 6), (6, 7), (1, 2), (4, 5)
        ]
        
        # Раздаем случайную пропускную способность трубам (лимит от 10 до 40 литров)
        for u, v in pipes:
            capacity = random.randint(10, 40)
            # Для главной финишной трубы (6, 7) дадим лимит побольше, чтобы она не была всегда единственным затором
            if (u, v) == (6, 7):
                capacity = random.randint(40, 80)
            self.G.add_edge(u, v, capacity=capacity)
            
        self.draw_network()

    def calculate_max_flow(self):
        # САМАЯ ВАЖНАЯ СТРОКА: Запускаем алгоритм Форда-Фалкерсона встроенными средствами NetworkX
        # Параметры: Исток = 0, Сток = 7, лимитирующий фактор = 'capacity'
        try:
            self.flow_value, self.flow_dict = nx.maximum_flow(self.G, 0, 7, capacity='capacity')
            
            # Строим красивый инженерный отчет
            report = (
                f"🌊 Насосы запущены на максимум!\n\n"
                f"• Мощность на входе (узел 0):\n  {self.flow_value} л/сек\n\n"
                f"• Дошло до жилых домов (узел 7):\n  {self.flow_value} л/сек\n\n"
                f"💡 Обратите внимание:\n"
                f"Некоторые трубы заполнены\n"
                f"полностью (до лимита) —\n"
                f"это 'узкие горлышки' системы.\n"
                f"Они подсвечены жирным синим!"
            )
            self.lbl_results.config(text=report, foreground="darkgreen")
            self.draw_network(show_flow=True)
        except Exception as e:
            messagebox.showerror("Ошибка гидро-расчета", str(e))

    def draw_network(self, show_flow=False):
        self.ax.clear()
        
        # Базовые серые стрелки труб
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color="#d0d0d0", width=1.5, arrowstyle="-|>", arrowsize=15, node_size=600)
        
        # Если включили насосы, поверх пускаем воду (жирные синие линии разной толщины в зависимости от потока)
        if show_flow and self.flow_dict:
            flow_edges = []
            edge_widths = []
            
            for u in self.flow_dict:
                for v, flow_amount in self.flow_dict[u].items():
                    if flow_amount > 0:
                        flow_edges.append((u, v))
                        # Толщина синей линии зависит от реального количества проходящей воды
                        width = 2.0 + (flow_amount / max(1, self.flow_value)) * 6.0
                        edge_widths.append(width)
                        
            if flow_edges:
                nx.draw_networkx_edges(
                    self.G, self.pos, ax=self.ax, 
                    edgelist=flow_edges, 
                    edge_color="#0066ff", width=edge_widths,
                    arrowstyle="-|>", arrowsize=18, node_size=600
                )
                
        # Настраиваем текстовые подписи над трубами в формате: "Текущий Поток / Макс Лимит"
        edge_labels = {}
        for u, v, data in self.G.edges(data=True):
            capacity = data['capacity']
            if show_flow and self.flow_dict and v in self.flow_dict[u]:
                actual_flow = self.flow_dict[u][v]
                edge_labels[(u, v)] = f"{actual_flow}/{capacity}"
            else:
                edge_labels[(u, v)] = f"0/{capacity}"
                
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax, font_size=8, font_weight="bold")

        # Рисуем узлы-резервуары
        node_colors = []
        for node in self.G.nodes():
            if node == 0:
                node_colors.append("#99ff99")  # Исток — зелёная водокачка
            elif node == 7:
                node_colors.append("#ff9999")  # Сток — красный жилой массив
            else:
                node_colors.append("#e6f2ff")  # Промежуточные задвижки
                
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color=node_colors, node_size=600, edgecolors="black", linewidths=1.5)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=11, font_weight="bold")
        
        # Добавляем текстовые маркеры Исток/Сток прямо на холст
        self.ax.text(0, 2.4, "💧 ИСТОК\n(Башня)", ha="center", va="center", fontsize=9, fontweight="bold", color="darkgreen")
        self.ax.text(4, 2.4, "🏠 СТОК\n(Дома)", ha="center", va="center", fontsize=9, fontweight="bold", color="darkred")

        self.ax.set_title("--- Инженерная схема труб | Числа: Реальный Поток / Лимит трубы в л/с", fontsize=11, fontweight='bold', pad=15)
        self.ax.axis("off")
        self.canvas.draw()

    def start_animated_flow(self):
        """Готовит данные для анимации и запускает её с первого шага"""
        try:
            # Сначала рассчитываем финальный максимальный поток
            self.flow_value, self.flow_dict = nx.maximum_flow(self.G, 0, 7, capacity='capacity')
            
            if self.flow_value == 0:
                messagebox.showinfo("Внимание", "Поток равен 0. Вода не может течь!")
                return
                
            # Блокируем кнопку, чтобы ученик не нажал её дважды во время анимации
            self.lbl_results.config(text="🌊 Запуск насосов...\nТрубы заполняются водой!", foreground="blue")
            
            # Запускаем пошаговую анимацию с коэффициента 0.1 (10% от финального потока)
            self.animate_step(current_ratio=0.1)
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def animate_step(self, current_ratio):
        """Отрисовывает промежуточное состояние потока и планирует следующий шаг"""
        if current_ratio > 1.0:
            # Конец анимации — выводим финальный отчёт инженера
            report = (
                f"🌊 Насосы запущены на максимум!\n\n"
                f"• Мощность на входе (узел 0):\n  {self.flow_value} л/сек\n\n"
                f"• Дошло до жилых домов (узел 7):\n  {self.flow_value} л/сек\n\n"
                f"💡 Обратите внимание:\n"
                f"Трубы, заполненные до упора,\n"
                f"подсвечены самым жирным синим!"
            )
            self.lbl_results.config(text=report, foreground="darkgreen")
            self.draw_network(show_flow=True)
            return

        # Очищаем холст для нового кадра анимации
        self.ax.clear()
        
        # Рисуем базовые серые стрелки труб
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color="#d0d0d0", width=1.5, arrowstyle="-|>", arrowsize=15, node_size=600)
        
        flow_edges = []
        edge_widths = []
        edge_labels = {}
        
        # Просчитываем текущий частичный поток для этого кадра
        for u in self.flow_dict:
            for v, final_flow in self.flow_dict[u].items():
                capacity = self.G[u][v]['capacity']
                
                # Поток на текущем шаге анимации
                current_flow = int(final_flow * current_ratio)
                
                if final_flow > 0:
                    flow_edges.append((u, v))
                    # Толщина растёт вместе с набором мощности
                    width = 2.0 + (current_flow / max(1, self.flow_value)) * 6.0
                    edge_widths.append(width)
                    edge_labels[(u, v)] = f"{current_flow}/{capacity}"
                else:
                    edge_labels[(u, v)] = f"0/{capacity}"

        # Рисуем синие линии текущего потока
        if flow_edges:
            nx.draw_networkx_edges(
                self.G, self.pos, ax=self.ax, 
                edgelist=flow_edges, 
                edge_color="#0066ff", width=edge_widths,
                arrowstyle="-|>", arrowsize=18, node_size=600
            )
            
            # Стрелочки направления по центру
            for u, v in flow_edges:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = (x2 - x1) * 0.01, (y2 - y1) * 0.01
                self.ax.annotate("", xy=(cx+dx, cy+dy), xytext=(cx, cy),
                                 arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5, mutation_scale=15))

        # Текстовые метки
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax, font_size=8, font_weight="bold")

        # Рисуем узлы-резервуары
        node_colors = ["#99ff99" if n == 0 else ("#ff9999" if n == 7 else "#e6f2ff") for n in self.G.nodes()]
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color=node_colors, node_size=600, edgecolors="black", linewidths=1.5)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=11, font_weight="bold")
        
        # Легенда
        self.ax.text(0, 2.4, "💧 ИСТОК\n(Башня)", ha="center", va="center", fontsize=9, fontweight="bold", color="darkgreen")
        self.ax.text(4, 2.4, "🏠 СТОК\n(Дома)", ha="center", va="center", fontsize=9, fontweight="bold", color="darkred")
        self.ax.set_title(f"--- НАПОР НАСОСОВ: {int(current_ratio*100)}% ---", fontsize=11, fontweight='bold', pad=15)
        self.ax.axis("off")
        self.canvas.draw()
        
        # Планируем следующий кадр через 150 миллисекунд (увеличиваем напор на 15%)
        # Изменяй 150 (скорость) и 0.15 (шаг напора), чтобы настроить идеальную плавность под свой ПК
        self.root.after(150, lambda: self.animate_step(current_ratio + 0.15))


if __name__ == "__main__":
    root = tk.Tk()
    app = WaterFlowSimulator(root)
    root.mainloop()







import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random
import numpy as np

# Пытаемся импортировать Венгерский алгоритм из scipy, если его нет — используем встроенную альтернативу NetworkX
try:
    from scipy.optimize import linear_sum_assignment
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

class HRAssignmentGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Урок 9: ИИ-Отдел Кадров — Двудольные графы и Задача о назначениях")
        self.root.geometry("1450x880")
        
        # Двудольный граф
        self.G = nx.Graph()
        self.pos = {}
        self.matrix_costs = {} # Матрица ценностей: (программист, задача) -> цена
        self.user_assignments = {} # Выбор ученика: программист -> задача
        
        # Списки объектов
        self.programmers = ["Анна (№0)", "Борис (№1)", "Влад (№2)", "Дарья (№3)", "Егор (№4)"]
        self.tasks = ["Нейросеть (№5)", "Киберщит (№6)", "База Данных (№7)", "Мобилка (№8)", "Блокчейн (№9)"]
        
        self.setup_ui()
        self.generate_new_hr_case()

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=420)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для графа
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Управление кейсом
        ttk.Label(self.left_panel, text="💼 Управление отделом кадров", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Button(self.left_panel, text="🎲 Сгенерировать новые резюме и цены", command=self.generate_new_hr_case).pack(fill=tk.X, pady=5)
        
        # Блок ручного назначения должностей
        ttk.Label(self.left_panel, text="🛠️ Назначить сотрудников вручную:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        
        manual_frame = ttk.Frame(self.left_panel)
        manual_frame.pack(fill=tk.X, pady=5)
        ttk.Label(manual_frame, text="Сотрудник (0-4):").pack(side=tk.LEFT)
        self.ent_worker = ttk.Entry(manual_frame, width=4)
        self.ent_worker.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(manual_frame, text="Задача (5-9):").pack(side=tk.LEFT, padx=(5,0))
        self.ent_task = ttk.Entry(manual_frame, width=4)
        self.ent_task.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(manual_frame, text="🔗 Связать", command=self.assign_worker_manual).pack(side=tk.LEFT, padx=5)
        
        # Кнопки проверок и ИИ
        ttk.Button(self.left_panel, text="🧐 Проверить бюджет моего назначения", command=self.check_user_budget).pack(fill=tk.X, pady=(10,5))
        ttk.Button(self.left_panel, text="🤖 Запустить Венгерский Алгоритм ИИ", command=self.solve_hungarian_ai).pack(fill=tk.X, pady=5)
        
        # Результаты вычислений
        ttk.Label(self.left_panel, text="📊 Финансовый отчёт компании:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.lbl_results = ttk.Label(self.left_panel, text="Назначьте людей на задачи...", font=("Courier", 10), justify=tk.LEFT, foreground="darkblue")
        self.lbl_results.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # Шпаргалка и история
        ttk.Label(self.left_panel, text="📜 Исторический детектив:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=18, wrap=tk.WORD, font=("Arial", 10), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Поле Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Память для кликов: хранит первую выбранную вершину
        self.clicked_node = None
        
        # Подключаем интерактивный клик мышкой по кружкам графа!
        self.fig.canvas.mpl_connect('button_press_event', self.on_graph_click)


    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "📜 ИСТОРИЯ И СМЫСЛ ЗАДАЧИ:\n"
            "В 1955 году американский математик Гарольд Кун опубликовал алгоритм, который совершил "
            "революцию в управлении персоналом. Он назвал его 'Венгерским методом' в честь двух "
            "венгерских учёных — Денеша Кёнига и Йенё Эгервари, чьи идеи начала XX века он развил.\n\n"
            "Эта задача решает глобальную проблему распределения ресурсов: например, у вас есть 5 сложных "
            "задач ИИ и 5 программистов, каждый из которых требует за разные задачи разную оплату. "
            "Как распределить людей по рабочим местам так, чтобы вся работа была выполнена идеально, "
            "а суммарные затраты компании оказались минимальными? Программа использует специальный "
            "двудольный граф (где вершины разделены на два независимых лагеря) и за сотые доли секунды "
            "вычисляет золотой баланс.\n\n"
            "💼 ГДЕ ПРИМЕНЯЕТСЯ СЕГОДНЯ:\n"
            "• В сервисах распределения заказов такси (какого водителя направить к какому клиенту, чтобы "
            "время подачи машины по всему городу было минимальным).\n"
            "• В HR-службах крупных корпораций при распределении вакансий."
        )
        self.txt_hint.config(state=tk.DISABLED)

    def on_graph_click(self, event):
        if event.xdata is None or event.ydata is None or not self.pos:
            return
            
        # Находим ближайшую к клику вершину графа
        click_coord = (event.xdata, event.ydata)
        closest_node = None
        min_dist = float('inf')
        
        for node, coord in self.pos.items():
            dist = (coord[0] - click_coord[0])**2 + (coord[1] - click_coord[1])**2
            if dist < min_dist:
                min_dist = dist
                closest_node = node
                
        # Если кликнули достаточно близко к узлу (радиус попадания)
        if min_dist < 0.15 and closest_node is not None:
            # Если это первый клик и выбрана левая доля (Сотрудник 0-4)
            if self.clicked_node is None:
                if closest_node in range(5):
                    self.clicked_node = closest_node
                    # Подсвечиваем текстовое поле, чтобы ученик видел прогресс
                    self.ent_worker.delete(0, tk.END)
                    self.ent_worker.insert(0, str(closest_node))
                else:
                    messagebox.showinfo("Подсказка", "Сначала выберите сотрудника из левой колонки (№ 0-4)!")
            else:
                # Это второй клик. Проверяем, что выбрана правая доля (Задача 5-9)
                if closest_node in range(5, 10):
                    worker = self.clicked_node
                    task = closest_node
                    
                    # Заполняем поля ввода для наглядности
                    self.ent_task.delete(0, tk.END)
                    self.ent_task.insert(0, str(task))
                    
                    # Вызываем старую рабочую логику связывания
                    if task in self.user_assignments.values():
                        old_worker = [w for w, t in self.user_assignments.items() if t == task]
                        if old_worker:
                            del self.user_assignments[old_worker[0]]
                            
                    self.user_assignments[worker] = task
                    self.draw_hr_graph(highlighted_dict=self.user_assignments, color="orange")
                    
                    current_sum = sum(self.matrix_costs[(w, t)] for w, t in self.user_assignments.items())
                    self.lbl_results.config(text=f"Выбор кадров обновлен:\n• Назначено: {len(self.user_assignments)} из 5 чел.\n• Текущий бюджет: {current_sum} тыс. руб.", foreground="black")
                    
                    # Сбрасываем память клика для следующей пары
                    self.clicked_node = None
                else:
                    # Если кликнули опять по левой доле, просто переключаем текущего рабочего
                    if closest_node in range(5):
                        self.clicked_node = closest_node
                        self.ent_worker.delete(0, tk.END)
                        self.ent_worker.insert(0, str(closest_node))
                    else:
                        self.clicked_node = None


    def generate_new_hr_case(self):
        self.G.clear()
        self.matrix_costs = {}
        self.user_assignments = {}
        self.lbl_results.config(text="Сгенерирован новый контракт.\nРаспределите сотрудников!", foreground="black")
        
        # Двудольный граф: 0-4 левая доля (программисты), 5-9 правая доля (задачи)
        workers = list(range(5))
        tasks_nodes = list(range(5, 10))
        
        self.G.add_nodes_from(workers, bipartite=0)
        self.G.add_nodes_from(tasks_nodes, bipartite=1)
        
        # Координаты для двух ровных параллельных колонн (долей графа)
        for i in workers:
            self.pos[i] = (1, 4 - i) # Колонна сотрудников слева
        for idx, j in enumerate(tasks_nodes):
            self.pos[j] = (3, 4 - idx) # Колонна задач справа
            
        # Заполняем веса рёбер (стоимость работы в тыс. рублей от 30 до 95)
        for w in workers:
            for t in tasks_nodes:
                cost = random.randint(30, 95)
                self.matrix_costs[(w, t)] = cost
                self.G.add_edge(w, t, weight=cost)
                
        self.draw_hr_graph()

    def assign_worker_manual(self):
        try:
            worker = int(self.ent_worker.get())
            task = int(self.ent_task.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые номера!")
            return
            
        if worker < 0 or worker > 4 or task < 5 or task > 9:
            messagebox.showerror("Ошибка", "Номера сотрудников должны быть от 0 до 4, а задач — от 5 до 9!")
            return
            
        # Проверяем, не занята ли уже эта задача другим сотрудником
        if task in self.user_assignments.values():
            # Находим, кто был назначен ранее, и удаляем старую связь
            old_worker = [w for w, t in self.user_assignments.items() if t == task][0]
            del self.user_assignments[old_worker]
            
        # Записываем новое назначение
        self.user_assignments[worker] = task
        self.draw_hr_graph(highlighted_dict=self.user_assignments, color="orange")
        
        # Считаем текущие промежуточные траты
        current_sum = sum(self.matrix_costs[(w, t)] for w, t in self.user_assignments.items())
        self.lbl_results.config(text=f"Текущий выбор кадров:\n• Назначено: {len(self.user_assignments)} из 5 чел.\n• Текущий бюджет: {current_sum} тыс. руб.", foreground="black")

    def check_user_budget(self):
        if len(self.user_assignments) < 5:
            messagebox.showwarning("Внимание", f"Вы распределили только {len(self.user_assignments)} сотрудников из 5. Назначьте всех!")
            return
            
        total_user_cost = sum(self.matrix_costs[(w, t)] for w, t in self.user_assignments.items())
        
        # Вычисляем эталонное ИИ решение для сравнения стоимости
        if HAS_SCIPY:
            cost_matrix = np.zeros((5, 5))
            for w in range(5):
                for t in range(5):
                    cost_matrix[w][t] = self.matrix_costs[(w, t + 5)]
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            ai_cost = cost_matrix[row_ind, col_ind].sum()
        else:
            # Альтернативный поиск идеала средствами networkx
            ai_sol = nx.bipartite.minimum_weight_full_matching(self.G, weight='weight')
            ai_cost = sum(self.matrix_costs[(w, t)] if w < 5 else 0 for w, t in ai_sol.items())
            
        diff = total_user_cost - ai_cost
        if diff == 0:
            messagebox.showinfo("Идеально! 🎉", f"Поздравляем! Вы сработали как гениальный директор компании!\nВаш бюджет: {int(total_user_cost)} тыс. руб. — это абсолютный минимум!")
        else:
            messagebox.showinfo("Анализ расходов", f"Все сотрудники устроены.\n• Ваш бюджет: {int(total_user_cost)} тыс. руб.\n• Математический минимум: {int(ai_cost)} тыс. руб.\n\nВы переплатили лишние {int(diff)} тыс. рублей. Попробуйте улучшить результат или запустите ИИ!")

    def solve_hungarian_ai(self):
        ai_assignments = {}
        
        if HAS_SCIPY:
            cost_matrix = np.zeros((5, 5))
            for w in range(5):
                for t in range(5):
                    cost_matrix[w][t] = self.matrix_costs[(w, t + 5)]
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            for r, c in zip(row_ind, col_ind):
                ai_assignments[r] = c + 5
            total_ai_cost = cost_matrix[row_ind, col_ind].sum()
        else:
            # Если scipy недоступен, рассчитываем через встроенные алгоритмы графов networkx
            matching = nx.bipartite.minimum_weight_full_matching(self.G, weight='weight')
            for w in range(5):
                ai_assignments[w] = matching[w]
            total_ai_cost = sum(self.matrix_costs[(w, ai_assignments[w])] for w in range(5))
            
        # Обновляем отчёт на экране
        report = f"🤖 Венгерский алгоритм ИИ сработал:\n\n"
        for w, t in ai_assignments.items():
            report += f"• {self.programmers[w]} -> {self.tasks[t-5]} ({self.matrix_costs[(w,t)]}к)\n"
        report += f"\n🏆 Идеальный минимальный бюджет:\n {int(total_ai_cost)} тыс. рублей!"
        
        self.lbl_results.config(text=report, foreground="darkgreen")
        # Рисуем идеальные связи жирным зелёным цветом
        self.draw_hr_graph(highlighted_dict=ai_assignments, color="#00cc66")

    def draw_hr_graph(self, highlighted_dict=None, color="orange"):
        self.ax.clear()
        
        # Рисуем фоновые тонкие линии (все возможные предложения зарплат)
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color="#e0e0e0", width=1.0)
        
        # Подсвечиваем выбранные контракты жирными линиями со стрелочками
        if highlighted_dict:
            edges_to_show = [(w, t) for w, t in highlighted_dict.items()]
            nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edgelist=edges_to_show, edge_color=color, width=4.5)
            
            # Векторы направления
            for u, v in edges_to_show:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = (x2 - x1) * 0.01, (y2 - y1) * 0.01
                self.ax.annotate("", xy=(cx+dx, cy+dy), xytext=(cx, cy),
                                 arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5, mutation_scale=15))

        # Настраиваем текстовые метки цен над рёбрами
        edge_labels = {}
        for (w, t), cost in self.matrix_costs.items():
            if highlighted_dict and w in highlighted_dict and highlighted_dict[w] == t:
                edge_labels[(w, t)] = f"{cost}к"
            elif cost < 40 or cost > 85:
                edge_labels[(w, t)] = f"{cost}к"
                
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax, font_size=8, font_color="#555555")

        # Отрисовка вершин долей
        workers_nodes = list(range(5))
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, nodelist=workers_nodes, node_color="#99ccff", node_size=650, edgecolors="black")
        
        tasks_nodes = list(range(5, 10))
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, nodelist=tasks_nodes, node_color="#ffdb4d", node_size=650, edgecolors="black")
        
        # Подписи названий узлов по бокам
        labels_dict = {i: str(i) for i in range(10)}
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, labels=labels_dict, font_size=10, font_weight="bold")
        
        # Красивые текстовые легенды-колонки на самом графике
        for i, name in enumerate(self.programmers):
            self.ax.text(0.3, 4 - i, name, ha="right", va="center", fontname="Arial", fontsize=10, fontweight="bold", bbox=dict(facecolor='#e6f2ff', alpha=0.8, boxstyle='round,pad=0.3'))
        for i, name in enumerate(self.tasks):
            self.ax.text(3.7, 4 - i, name, ha="left", va="center", fontname="Arial", fontsize=10, fontweight="bold", bbox=dict(facecolor='#fff7d9', alpha=0.8, boxstyle='round,pad=0.3'))

        self.ax.set_title("--- Левая доля — Сотрудники | Направления задач ИИ", fontsize=11, fontweight='bold', pad=15)
        self.ax.set_xlim(0, 4.5)
        self.ax.set_ylim(-0.8, 4.8)
        self.ax.axis("off")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = HRAssignmentGame(root)
    root.mainloop()