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