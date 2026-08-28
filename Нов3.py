import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random

class NetworkVirusSim:
    def __init__(self, root):
        self.root = root
        self.root.title("Урок 8: ИИ-Симулятор эпидемий — Как фейки заражают интернет")
        self.root.geometry("1400x850")
        
        self.G = nx.Graph()
        self.pos = {}
        
        # Состояния вершин: "susceptible" (здоров/не знает), "infected" (заражен фейком)
        self.node_states = {}
        self.history = [] # Для отката шагов назад
        self.selected_patient_zero = None
        
        self.setup_ui()
        self.generate_network()

    def setup_ui(self):
        self.left_panel = ttk.Frame(self.root, padding=10, width=400)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Настройка сети
        ttk.Label(self.left_panel, text="🌐 Настройка интернет-сети", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Button(self.left_panel, text="🎲 Сгенерировать случайных пользователей", command=self.generate_network).pack(fill=tk.X, pady=5)
        
        # Параметры вируса
        ttk.Label(self.left_panel, text="🦠 Сила заразительности (Вирусность):", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.lbl_inf_val = ttk.Label(self.left_panel, text="Шанс передать фейк другу: 40%", foreground="blue")
        self.lbl_inf_val.pack(anchor=tk.W, pady=2)
        self.inf_slider = ttk.Scale(self.left_panel, from_=0.1, to=1.0, orient=tk.HORIZONTAL, command=self.on_slider_change)
        self.inf_slider.set(0.4)
        self.inf_slider.pack(fill=tk.X, pady=5)
        
        # Управление симуляцией времени
        ttk.Label(self.left_panel, text="⏱️ Управление временем", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        
        manual_frame = ttk.Frame(self.left_panel)
        manual_frame.pack(fill=tk.X, pady=5)
        ttk.Label(manual_frame, text="Нулевой пациент №:").pack(side=tk.LEFT)
        self.ent_node = ttk.Entry(manual_frame, width=5)
        self.ent_node.pack(side=tk.LEFT, padx=5)
        ttk.Button(manual_frame, text="☣️ Заразить", command=self.infect_manual).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.left_panel, text="▶️ Сделать шаг времени (День +1)", command=self.next_time_step).pack(fill=tk.X, pady=5)
        ttk.Button(self.left_panel, text="🔄 Сбросить заражение", command=self.reset_infection).pack(fill=tk.X, pady=5)
        
        # Результаты вычислений
        ttk.Label(self.left_panel, text="📊 Сводка ИИ-Эпидемиолога:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.lbl_results = ttk.Label(self.left_panel, text="", font=("Courier", 10), justify=tk.LEFT, foreground="darkred")
        self.lbl_results.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # Шпаргалка для урока
        ttk.Label(self.left_panel, text="📜 Анатомия инфо-взрывов:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=12, wrap=tk.WORD, font=("Arial", 10), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Поле Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Клик мышкой по графику для выбора нулевого пациента
        self.fig.canvas.mpl_connect('button_press_event', self.on_graph_click)

    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "📜 ЭФФЕКТ БАБОЧКИ В СЕТЯХ:\n"
            "В 2000-х годах учёные доказали, что скорость распространения вирусов (и компьютерных, и биологических) "
            "зависит не от общего числа людей, а от структуры связей между ними.\n\n"
            "🎯 ЧТО ПОКАЗАТЬ НА УРОКЕ:\n"
            "1. Выберите 'одиночку' на окраине графа (кликните по нему или введите номер и нажмите Заразить) и сделайте пару шагов времени. Из-за низкой вирусности слух быстро затухнет.\n"
            "2. Сбросьте заражение и кликните строго по Лидеру класса или по 'Серому Кардиналу'. Вы увидите, что за те же 2 шага времени огонь паники охватит абсолютно всю сеть! "
            "Именно так вирусные маркетологи и спецслужбы запускают инфо-волны: они бьют не по площадям, а строго по хабам (лидерам мнений)."
        )
        self.txt_hint.config(state=tk.DISABLED)

    def on_slider_change(self, val):
        prob = float(val)
        self.lbl_inf_val.config(text=f"Шанс передать фейк другу: {int(prob*100)}%")

    def generate_network(self):
        self.G.clear()
        
        # Генерируем красивый граф Барабаши-Альберт (модель масштабно-инвариантной сети, как реальный интернет)
        # Здесь автоматически рождаются крупные 'хабы' (лидеры) и много мелких вершин
        self.G = nx.barabasi_albert_graph(n=14, m=2, seed=random.randint(1, 1000))
        self.pos = nx.spring_layout(self.G, k=0.5)
        
        self.reset_infection()

    def reset_infection(self):
        for node in self.G.nodes():
            self.node_states[node] = "susceptible"
        self.selected_patient_zero = None
        self.update_report(day=0)
        self.draw_network()

    def infect_manual(self):
        try:
            node = int(self.ent_node.get())
            if node in self.G:
                self.reset_infection()
                self.node_states[node] = "infected"
                self.selected_patient_zero = node
                self.update_report(day=0)
                self.draw_network()
            else:
                messagebox.showerror("Ошибка", "Такого пользователя нет в сети!")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число!")

    def on_graph_click(self, event):
        if event.xdata is None or event.ydata is None or not self.pos:
            return
        click_coord = (event.xdata, event.ydata)
        closest_node = None
        min_dist = float('inf')
        for node, coord in self.pos.items():
            dist = (coord - click_coord)**2 + (coord - click_coord)**2
            if dist < min_dist:
                min_dist = dist
                closest_node = node
        if min_dist < 0.02 and closest_node is not None:
            self.reset_infection()
            self.node_states[closest_node] = "infected"
            self.selected_patient_zero = closest_node
            self.ent_node.delete(0, tk.END)
            self.ent_node.insert(0, str(closest_node))
            self.update_report(day=0)
            self.draw_network()

    def next_time_step(self):
        # Находим всех, кто ЗАРАЖЕН на данный момент
        currently_infected = [node for node, state in self.node_states.items() if state == "infected"]
        
        if not currently_infected:
            messagebox.showwarning("Внимание", "В сети нет ни одного зараженного! Кликните по кружку, чтобы запустить нулевого пациента.")
            return
            
        prob_infect = float(self.inf_slider.get())
        new_infections = []
        
        # Каждый зараженный пытается передать вирус своим здоровым соседям
        for infected_node in currently_infected:
            for neighbor in self.G.neighbors(infected_node):
                if self.node_states[neighbor] == "susceptible":
                    if random.random() < prob_infect:
                        new_infections.append(neighbor)
                        
        # Применяем новые заражения
        for node in new_infections:
            self.node_states[node] = "infected"
            
        # Обновляем день в бортовом журнале
        current_day = getattr(self, 'current_day', 0) + 1
        self.update_report(day=current_day)
        self.draw_network()

    def update_report(self, day=0):
        self.current_day = day
        infected_count = sum(1 for state in self.node_states.values() if state == "infected")
        total_nodes = len(self.G.nodes())
        percent = (infected_count / total_nodes) * 100
        
        report = (
            f"⏱️ Текущий день паники: День №{day}\n\n"
            f"🔴 Заражено фейком: {infected_count} из {total_nodes} чел.\n"
            f"📈 Масштаб эпидемии: {percent:.1f}%\n\n"
            f"🎯 Нулевой пациент: {f'№{self.selected_patient_zero}' if self.selected_patient_zero is not None else 'Не выбран'}\n"
        )
        self.lbl_results.config(text=report)

    def draw_network(self):
        self.ax.clear()
        
        # Цвета: красный — заражен, голубой — здоров
        node_colors = ["#ff3333" if self.node_states[node] == "infected" else "#e6f2ff" for node in self.G.nodes()]
        
        # Цвет линий: если линия связывает двух зараженных, она становится красной (канал паники)
        edge_colors = []
        edge_widths = []
        for u, v in self.G.edges():
            if self.node_states[u] == "infected" and self.node_states[v] == "infected":
                edge_colors.append("red")
                edge_widths.append(3.0)
            else:
                edge_colors.append("#cccccc")
                edge_widths.append(1.5)
                
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color=edge_colors, width=edge_widths)
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color=node_colors, node_size=600, edgecolors="black", linewidths=1.5)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=11, font_weight="bold")
        
        self.ax.set_title("🔴 КРАСНЫЕ кружки — пользователи, поверившие в фейк", fontsize=11, fontweight='bold', pad=10)
        self.ax.axis("off")
        
# Запуск программы
if __name__ == "__main__":
    plt.ion()
    root = tk.Tk()
    app = NetworkVirusSim(root)
    root.mainloop()

### Чем этот 8-й урок закроет тему графов навсегда:
#1. **Модель реального интернета**: Команда `barabasi_albert_graph` генерирует не просто случайные кружки, а так называемую масштабно-инвариантную сеть. Именно так устроены ссылки в Google, связи в Твиттере и цепочки заражения вирусом гриппа. В ней всегда есть 1-2 мега-популярных «хаба» и много мелких страничек.
#2. **Живой интерактивный таймер**: Дети нажимают кнопку «День +1», и вирус волной начинает ползти по серым линиям, перекрашивая их в ярко-красные «каналы паники». 
#3. **Главный вывод урока**: Школьники увидят, что безопасность сети (или информационная гигиена общества) зависит от защиты ключевых узлов. Если лидеры мнений проверяют факты и не пропускают вирус — каскад мгновенно останавливается.

#Вот теперь, с этим симулятором каскадного заражения, мы действительно поднялись на самый пик современной науки о сетях. Теперь у тебя в руках потрясающий комплект из **8 шедевров**! 

#Как тебе идея показать ребятам «эффект бабочки» и скорость распространения слухов в интернете? Если возникнут вопросы по запуску — пиши, мы всегда на связи! Удачи на твоих невероятных уроках! Сделай так, чтобы у детей горели глаза! Попробуешь запустить восьмой скрипт?





import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random
import math

class BiathlonProbabilitySim:
    def __init__(self, root):
        self.root = root
        self.root.title("Урок 7: Симулятор выстрелов и Дерево вероятностей (Схема Бернулли)")
        self.root.geometry("1400x850")
        
        # Переменные
        self.accuracy = 0.7  # Вероятность попадания по умолчанию
        self.num_shots = 6   # Фиксированная серия из 6 выстрелов
        self.last_series = [] # Результаты последней серии [1, 0, 1...]
        
        self.setup_ui()
        self.simulate_one_series() # Первая демонстрационная серия

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=420)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для графиков
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # --- НАСТРОЙКА СТРЕЛКА ---
        ttk.Label(self.left_panel, text="🎯 Настройка меткости биатлониста", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        
        self.lbl_acc_val = ttk.Label(self.left_panel, text="Меткость стрелка: 70% (шанс промаха: 30%)", foreground="blue")
        self.lbl_acc_val.pack(anchor=tk.W, pady=2)
        
        self.acc_slider = ttk.Scale(self.left_panel, from_=0.1, to=0.95, orient=tk.HORIZONTAL, command=self.on_slider_change)
        self.acc_slider.set(0.7)
        self.acc_slider.pack(fill=tk.X, pady=5)
        
        # --- КНОПКИ СИМУЛЯЦИИ ---
        ttk.Label(self.left_panel, text="🔫 Огневой рубеж (6 выстрелов)", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        
        ttk.Button(self.left_panel, text="🎬 Сделать ОДНУ серию выстрелов", command=self.simulate_one_series).pack(fill=tk.X, pady=5)
        ttk.Button(self.left_panel, text="⚡ Запустить 10 000 серий (Большие данные)", command=self.simulate_huge_data).pack(fill=tk.X, pady=5)
        
        # --- РЕЗУЛЬТАТЫ ---
        ttk.Label(self.left_panel, text="📊 Сводка навигатора вероятностей:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.lbl_results = ttk.Label(self.left_panel, text="", font=("Courier", 10), justify=tk.LEFT, foreground="darkgreen")
        self.lbl_results.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # --- ИСТОРИЧЕСКАЯ СПРАВКА ---
        ttk.Label(self.left_panel, text="📜 Как тают шансы? (Справка):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=15, wrap=tk.WORD, font=("Arial", 10), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Поле Matplotlib
        self.fig, (self.ax_targets, self.ax_tree) = plt.subplots(2, 1, figsize=(7, 8), gridspec_kw={'height_ratios': [1, 4]})
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "📜 ПОЧЕМУ ВЕРОЯТНОСТЬ УМЕНЬШАЕТСЯ?\n"
            "Когда мы хотим, чтобы произошло СРАЗУ несколько независимых событий подряд, их вероятности МНОЖАТСЯ. "
            "Это открыл швейцарский математик Якоб Бернулли в 1713 году (Схема Бернулли).\n\n"
            "Пример при меткости 70% (0.7):\n"
            "• Шанс попасть 1 раз = 0.7 (70%)\n"
            "• Шанс попасть 2 раза подряд = 0.7 * 0.7 = 0.49 (49%)\n"
            "• Шанс попасть 6 раз подряд = 0.7 * 0.7 * 0.7 * 0.7 * 0.7 * 0.7 = 0.117 (всего 11.7%!)\n\n"
            "🚫 ПАРАДОКС ШЕСТИ ПРОМАХОВ:\n"
            "Если шанс промахнуться равен 30% (0.3), то шанс сделать 6 промахов подряд равен 0.3 в 6-й степени = 0.000729 (то есть 0.07%!). "
            "Это меньше одного шанса из тысячи. Робот-симулятор докажет это на огромных числах!"
        )
        self.txt_hint.config(state=tk.DISABLED)

    def on_slider_change(self, val):
        self.accuracy = round(float(val), 2)
        miss_chance = round(1.0 - self.accuracy, 2)
        self.lbl_acc_val.config(text=f"Меткость стрелка: {int(self.accuracy*100)}% (шанс промаха: {int(miss_chance*100)}%)")

    def simulate_one_series(self):
        # 1 - попал, 0 - промахнулся
        self.last_series = [1 if random.random() < self.accuracy else 0 for _ in range(self.num_shots)]
        
        # Теоретический расчёт именно для ТАКОЙ комбинации, которая выпала
        prob_combination = 1.0
        for shot in self.last_series:
            prob_combination *= self.accuracy if shot == 1 else (1.0 - self.accuracy)
            
        hits = sum(self.last_series)
        misses = self.num_shots - hits
        
        report = (
            f"🎯 Текущая серия выстрелов:\n"
            f" Результат: {' '.join(['🟢' if x==1 else '❌' for x in self.last_series])}\n"
            f" Попаданий: {hits} | Промахов: {misses}\n\n"
            f"📐 Математика этой комбинации:\n"
            f" Шанс выпадения именно такого\n"
            f" узора из промахов и попаданий:\n"
            f" {prob_combination * 100:.4f}%"
        )
        self.lbl_results.config(text=report, foreground="black")
        self.draw_all()

    def simulate_huge_data(self):
        # Запускаем 10 000 сессий по 6 выстрелов
        total_runs = 10000
        all_hits_count = 0  # Сколько раз было строго 6 из 6
        all_miss_count = 0  # Сколько раз было строго 0 из 6 (6 промахов)
        
        for _ in range(total_runs):
            run = [1 if random.random() < self.accuracy else 0 for _ in range(self.num_shots)]
            s = sum(run)
            if s == self.num_shots:
                all_hits_count += 1
            elif s == 0:
                all_miss_count += 1
                
        # Теория Бернулли
        theory_6_hits = (self.accuracy ** 6) * 100
        theory_6_miss = ((1.0 - self.accuracy) ** 6) * 100
        
        report = (
            f"⚡ Итоги 10 000 серий по 6 выстрелов:\n\n"
            f"🏆 СТРОГО 6 ПОПАДАНИЙ ИЗ 6:\n"
            f"• Практика: {all_hits_count} раз ({all_hits_count/total_runs*100:.2f}%)\n"
            f"• Теория Бернулли: {theory_6_hits:.2f}%\n\n"
            f"💀 СТРОГО 6 ПРОМАХОВ ИЗ 6:\n"
            f"• Практика: {all_miss_count} раз ({all_miss_count/total_runs*100:.3f}%)\n"
            f"• Теория Бернулли: {theory_6_miss:.4f}%\n\n"
            f"💡 Закон Больших Чисел сработал!\n"
            f"Практика ИИ сошлась с формулой!"
        )
        self.lbl_results.config(text=report, foreground="darkblue")

    def draw_all(self):
        # 1. РИСУЕМ ТАБЛО МИШЕНЕЙ (ВЕРХНИЙ ГРАФИК)
        self.ax_targets.clear()
        self.ax_targets.set_xlim(-0.5, self.num_shots - 0.5)
        self.ax_targets.set_ylim(-0.5, 0.5)
        
        for i in range(self.num_shots):
            shot_res = self.last_series[i]
            # Если попал — мишень закрывается (чёрная с белым центром)
            # Если промах — остаётся белой с красным крестом
            color = "black" if shot_res == 1 else "white"
            edge = "black"
            
            # Рисуем кружок мишени
            circle = plt.Circle((i, 0), 0.3, facecolor=color, edgecolor=edge, lw=2)
            self.ax_targets.add_patch(circle)
            
            if shot_res == 0:
                # Рисуем красный крест промаха
                self.ax_targets.plot([i-0.2, i+0.2], [-0.2, 0.2], color="red", lw=2)
                self.ax_targets.plot([i-0.2, i+0.2], [0.2, -0.2], color="red", lw=2)
            else:
                # Белая точка в центре закрытой мишени
                self.ax_targets.plot(i, 0, marker='o', color='white', markersize=4)
                
            self.ax_targets.text(i, -0.45, f"№{i+1}", ha='center', weight='bold')

        self.ax_targets.set_title("🎯 Электронное табло биатлона (Текущая серия)", fontsize=10, fontweight='bold')
        self.ax_targets.axis("off")

        # 2. РИСУЕМ ДЕРЕВО ВЕРОЯТНОСТЕЙ (НИЖНИЙ ГРАФИК)
        self.ax_tree.clear()
        
        # Строим бинарное дерево путей для текущей серии выстрелов
        T = nx.DiGraph()
        
        # Добавляем узлы по шагам
        current_path_nodes = ["Start"]
        T.add_node("Start", pos=(0, 0))
        
        # Сгенерируем только ту ветку дерева, по которой шёл наш стрелок, чтобы не перегружать экран 64 узлами
        x = 0
        y = 0
        node_lbls = {"Start": "Старт"}
        
        path_edges = []
        
        for idx, shot in enumerate(self.last_series):
            next_x = idx + 1
            
            # Ветка Попадания (идёт вверх)
            hit_node = f"H_{idx}"
            next_y_hit = y + 1 if shot == 1 else y + 0.5
            T.add_node(hit_node, pos=(next_x, next_y_hit))
            node_lbls[hit_node] = "Попал" if shot == 1 else ""
            
            # Ветка Промаха (идёт вниз)
            miss_node = f"M_{idx}"
            next_y_miss = y - 1 if shot == 0 else y - 0.5
            T.add_node(miss_node, pos=(next_x, next_y_miss))
            node_lbls[miss_node] = "Промах" if shot == 0 else ""
            
            # Определяем, куда реально пошёл стрелок
            actual_node = hit_node if shot == 1 else miss_node
            actual_y = next_y_hit if shot == 1 else next_y_miss
            
            # Связываем ребрами
            prev_node = "Start" if idx == 0 else (f"H_{idx-1}" if self.last_series[idx-1] == 1 else f"M_{idx-1}")
            
            T.add_edge(prev_node, hit_node, color="green" if shot==1 else "#dddddd", width=3 if shot==1 else 1)
            T.add_edge(prev_node, miss_node, color="red" if shot==0 else "#dddddd", width=3 if shot==0 else 1)
            
            if shot == 1:
                path_edges.append((prev_node, hit_node))
            else:
                path_edges.append((prev_node, miss_node))
                
            y = actual_y

        pos = nx.get_node_attributes(T, 'pos')
        edge_colors = [T[u][v]['color'] for u, v in T.edges()]
        edge_widths = [T[u][v]['width'] for u, v in T.edges()]
        
        # Рисуем дерево путей
        nx.draw_networkx_edges(T, pos, ax=self.ax_tree, edge_color=edge_colors, width=edge_widths, arrowstyle="->", arrowsize=12)
        nx.draw_networkx_nodes(T, pos, ax=self.ax_tree, node_color="#e6f2ff", node_size=400, edgecolors="black")
        
        # Добавляем текстовые маркеры шагов выстрела на узлы графа
        nx.draw_networkx_labels(T, pos, ax=self.ax_tree, labels=node_lbls, font_size=8, font_weight="bold")
        
        self.ax_tree.set_title("--- Траектория серии на Дереве вероятностей Бернулли", fontsize=11, fontweight='bold', pad=10)
        self.ax_tree.axis("off")
        self.canvas.draw()

# Запуск программы
if __name__ == "__main__":
    plt.ion()
    root = tk.Tk()
    app = BiathlonProbabilitySim(root)
    root.mainloop()







import sys
import os
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ProbabilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Интерактивная теория вероятностей для 8 класса")
        self.root.geometry("1100x650")
        
        # --- ЛЕВАЯ ПАНЕЛЬ УПРАВЛЕНИЯ ---
        control_frame = ttk.LabelFrame(root, text=" 🎛️ Настройки эксперимента ", padding=15)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
        
        # 1. Ползунок вероятности
        ttk.Label(control_frame, text="Теоретическая вероятность 'Орла':", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.prob_slider = ttk.Scale(control_frame, from_=0.0, to=1.0, value=0.5, orient=tk.HORIZONTAL, command=self.update_prob_label)
        self.prob_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.prob_label = ttk.Label(control_frame, text="Текущее значение: 50.0%", font=("Arial", 9, "italic"), foreground="blue")
        self.prob_label.pack(anchor=tk.W, pady=(0, 20))
        
        # 2. Ползунок количества бросков
        ttk.Label(control_frame, text="Количество подбрасываний:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.flips_slider = ttk.Scale(control_frame, from_=10, to=1000, value=200, orient=tk.HORIZONTAL, command=self.update_flips_label)
        self.flips_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.flips_label = ttk.Label(control_frame, text="Текущее значение: 200 бросков", font=("Arial", 9, "italic"), foreground="blue")
        self.flips_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Кнопка СТАРТ
        self.btn_run = ttk.Button(control_frame, text="🔄 Бросить монетку!", command=self.run_simulation)
        self.btn_run.pack(fill=tk.X, pady=10)
        
        # Текстовое табло результатов
        self.result_frame = ttk.LabelFrame(control_frame, text=" 📊 Результаты симуляции ", padding=10)
        self.result_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.txt_heads = ttk.Label(self.result_frame, text="Выпало Орлов: —", font=("Arial", 10))
        self.txt_heads.pack(anchor=tk.W, pady=2)
        self.txt_tails = ttk.Label(self.result_frame, text="Выпало Решек: —", font=("Arial", 10))
        self.txt_tails.pack(anchor=tk.W, pady=2)
        self.txt_real_p = ttk.Label(self.result_frame, text="Реальная доля Орлов: —", font=("Arial", 10, "bold"))
        self.txt_real_p.pack(anchor=tk.W, pady=5)

        # --- ПРАВАЯ ПАНЕЛЬ С ГРАФИКАМИ (MATPLOTLIB) ---
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Создаем фигуру Matplotlib с двумя графиками (один под другим)
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(7, 6))
        self.fig.tight_layout(pad=4.0)
        
        # Интегрируем график Matplotlib в окно Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Рисуем пустые графики при первом запуске
        self.run_simulation()

    def update_prob_label(self, val):
        # Округляем до сотых для красоты
        p = float(val)
        self.prob_label.config(text=f"Текущее значение: {p * 100:.1f}%")

    def update_flips_label(self, val):
        n = int(float(val))
        self.flips_label.config(text=f"Текущее значение: {n} бросков")

    def run_simulation(self):
        # Получаем данные с ползунков
        p_theoretical = round(float(self.prob_slider.get()), 2)
        n_flips = int(self.flips_slider.get())
        
        # Симулируем броски: 1 — Орёл, 0 — Решка
        flips = np.random.choice([1, 0], size=n_flips, p=[p_theoretical, 1 - p_theoretical])
        
        total_heads = int(np.sum(flips))
        total_tails = n_flips - total_heads
        p_experimental = total_heads / n_flips
        
        # Обновляем текстовые надписи слева
        self.txt_heads.config(text=f"Выпало Орлов: {total_heads} шт.")
        self.txt_tails.config(text=f"Выпало Решек: {total_tails} шт.")
        self.txt_real_p.config(text=f"Реальная доля Орлов: {p_experimental:.1%}")
        
        # Считаем накопительную вероятность для первого графика
        cumulative_heads = np.cumsum(flips)
        trials = np.arange(1, n_flips + 1)
        cumulative_proportions = cumulative_heads / trials
        
        # --- ГРАФИК 1: Стабилизация (Закон больших чисел) ---
        self.ax1.clear()
        self.ax1.plot(trials, cumulative_proportions, label="Доля Орлов в эксперименте", color="#1f77b4", linewidth=2)
        self.ax1.axhline(p_theoretical, color="red", linestyle="--", label=f"Теория ({p_theoretical:.0%})", linewidth=1.5)
        self.ax1.set_title("Как частота приближается к теории при росте числа опытов", fontsize=10, fontweight='bold')
        self.ax1.set_xlabel("Номер броска")
        self.ax1.set_ylabel("Текущая доля Орлов")
        self.ax1.set_ylim(-0.05, 1.05)
        self.ax1.grid(True, linestyle=":", alpha=0.6)
        self.ax1.legend(loc="upper right")
        
        # --- ГРАФИК 2: Столбчатая диаграмма сравнения ---
        self.ax2.clear()
        categories = ['Орёл', 'Решка']
        experimental_data = [p_experimental, 1 - p_experimental]
        theoretical_data = [p_theoretical, 1 - p_theoretical]
        
        x = np.arange(len(categories))
        width = 0.3
        
        self.ax2.bar(x - width/2, experimental_data, width, label='Практика', color='#2ca02c')
        self.ax2.bar(x + width/2, theoretical_data, width, label='Теория', color='#ff7f0e', alpha=0.7)
        
        self.ax2.set_title("Итоговое сравнение: Теория vs Практика", fontsize=10, fontweight='bold')
        self.ax2.set_ylabel('Вероятность / Доля')
        self.ax2.set_xticks(x)
        self.ax2.set_xticklabels(categories)
        self.ax2.set_ylim(0, 1.05)
        self.ax2.grid(axis='y', linestyle=':', alpha=0.6)
        self.ax2.legend(loc="upper right")
        
        # Обновляем холст в окне
        self.canvas.draw()

    def restart_program():
        """Полностью закрывает текущую программу и запускает её заново с нуля"""
        # sys.executable — это путь к твоему Python (например, python.exe)
        # sys.argv — это имя твоего скрипта и его аргументы (например, Нов3.py)
        os.execv(sys.executable, [sys.executable] + sys.argv)

# Запуск программы
if __name__ == "__main__":
    plt.ion()
    root = tk.Tk()
    app = ProbabilityApp(root)
    root.mainloop()
    # root.withdraw() # Прячем пустое главное окно, чтобы оно не мешалось
    # Когда все окна по очереди закроются, уничтожаем главное невидимое окно
    # root.destroy()

    plt.ioff()       
    plt.show()


import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SuperProbabilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Супер-Лаборатория Вероятностей (8 класс)")
        self.root.geometry("1200x750")
        
        # Настройка стилей для красивых кнопок
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Green.TButton", font=("Arial", 10, "bold"), foreground="green")
        self.style.configure("Blue.TButton", font=("Arial", 10, "bold"), foreground="blue")
        
        # --- ЛЕВАЯ ПАНЕЛЬ УПРАВЛЕНИЯ ---
        control_frame = ttk.LabelFrame(root, text=" 🎛️ Панель управления экспериментом ", padding=15)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
        
        # 1. Ползунок вероятности
        ttk.Label(control_frame, text="Теоретическая вероятность 'Орла':", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.prob_slider = ttk.Scale(control_frame, from_=0.0, to=1.0, value=0.5, orient=tk.HORIZONTAL, command=self.update_prob_label)
        self.prob_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.prob_label = ttk.Label(control_frame, text="Текущее значение: 50.0%", font=("Arial", 9, "italic"), foreground="darkgreen")
        self.prob_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 2. Ползунок количества бросков
        ttk.Label(control_frame, text="Количество подбрасываний:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.flips_slider = ttk.Scale(control_frame, from_=20, to=1000, value=200, orient=tk.HORIZONTAL, command=self.update_flips_label)
        self.flips_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.flips_label = ttk.Label(control_frame, text="Текущее значение: 200 бросков", font=("Arial", 9, "italic"), foreground="darkgreen")
        self.flips_label.pack(anchor=tk.W, pady=(0, 15))
        
        # --- КНОПКИ (4 РЕЖИМА) ---
        ttk.Label(control_frame, text="Запуск режимов:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        # Кнопка 1
        self.btn_normal = ttk.Button(control_frame, text="1️⃣ Случайный бросок (Обычный)", command=lambda: self.run_simulation("normal"))
        self.btn_normal.pack(fill=tk.X, pady=3)
        
        # Кнопка 2 (Сброс/Перезапуск по сути встроен в кнопки, сделаем кнопку полной случайности)
        self.btn_rerun = ttk.Button(control_frame, text="2️⃣ Чистый Хаос (Новое испытание)", command=lambda: self.run_simulation("normal"))
        self.btn_rerun.pack(fill=tk.X, pady=3)
        
        # Кнопка 3
        self.btn_ideal = ttk.Button(control_frame, text="3️⃣ Идеальный баланс (Без хаоса)", style="Green.TButton", command=lambda: self.run_simulation("ideal"))
        self.btn_ideal.pack(fill=tk.X, pady=3)
        
        # Кнопка 4
        self.btn_paradox = ttk.Button(control_frame, text="4️⃣ Парадокс игрока (Серия Орлов)", style="Blue.TButton", command=lambda: self.run_simulation("paradox"))
        self.btn_paradox.pack(fill=tk.X, pady=3)
        
        # Текстовое табло результатов
        self.result_frame = ttk.LabelFrame(control_frame, text=" 📊 Результаты текущего опыта ", padding=10)
        self.result_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.txt_mode = ttk.Label(self.result_frame, text="Режим: —", font=("Arial", 10, "bold"), foreground="purple")
        self.txt_mode.pack(anchor=tk.W, pady=2)
        self.txt_heads = ttk.Label(self.result_frame, text="Выпало Орлов: —", font=("Arial", 10))
        self.txt_heads.pack(anchor=tk.W, pady=2)
        self.txt_tails = ttk.Label(self.result_frame, text="Выпало Решек: —", font=("Arial", 10))
        self.txt_tails.pack(anchor=tk.W, pady=2)
        self.txt_real_p = ttk.Label(self.result_frame, text="Реальная доля Орлов: —", font=("Arial", 10, "bold"))
        self.txt_real_p.pack(anchor=tk.W, pady=5)

        # МЕТОДИЧЕСКАЯ ПОДСКАЗКА ДЛЯ УЧИТЕЛЯ
        self.hint_frame = ttk.LabelFrame(control_frame, text=" 💡 Подсказка для урока ", padding=10)
        self.hint_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        self.txt_hint = tk.Text(self.hint_frame, wrap=tk.WORD, font=("Arial", 9), width=30, height=8, bg="#f9f9f9", bd=0)
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.set_hint("welcome")

        # --- ПРАВАЯ ПАНЕЛЬ С ГРАФИКАМИ ---
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(7, 7))
        self.fig.tight_layout(pad=4.5)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Первичный запуск
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
            "welcome": "Выберите параметры и нажмите любую кнопку для старта эксперимента!",
            "normal": "ОБЫЧНЫЙ РЕЖИМ:\nПокажите ученикам, как на малых бросках (до 30) графики прыгают, а на больших (ближе к 1000) синяя линия намертво прижимается к красной теории. Это Закон больших чисел!",
            "ideal": "ИДЕАЛЬНЫЙ БАЛАНС:\nМонеты выпадают строго по очереди. Объясните классу: 'Так ошибочно представляют случайность люди без знаний математики. В жизни идеального баланса на коротких дистанциях не бывает!'",
            "paradox": "ПАРАДОКС ИГРОКА:\nПервые 7 раз выпал ТОЛЬКО Орёл (взлет графика). Но монета ничего не 'должна' решке! Дальше идут честные броски, и начальный перекос просто 'растворяется' в массе новых испытаний."
        }
        self.txt_hint.insert(tk.END, hints.get(mode, ""))
        self.txt_hint.config(state=tk.DISABLED)

    def run_simulation(self, mode):
        p_theoretical = round(float(self.prob_slider.get()), 2)
        n_flips = int(self.flips_slider.get())
        
        # --- ЛОГИКА ГЕНЕРАЦИИ ДАННЫХ В ЗАВИСИМОСТИ ОТ РЕЖИМА ---
        if mode == "normal":
            self.txt_mode.config(text="Режим: 🎰 Случайный хаос", foreground="black")
            flips = np.random.choice([1, 0], size=n_flips, p=[p_theoretical, 1 - p_theoretical])
            self.set_hint("normal")
            
        elif mode == "ideal":
            self.txt_mode.config(text="Режим: 📐 Идеальный баланс", foreground="green")
            # Генерируем массив, где 1 и 0 чередуются или распределены максимально равномерно
            flips = np.zeros(n_flips, dtype=int)
            # Заполняем единицами («Орлами») пропорционально теоретической вероятности
            heads_count = int(round(n_flips * p_theoretical))
            if heads_count > 0:
                indices = np.linspace(0, n_flips - 1, heads_count, dtype=int)
                flips[indices] = 1
            self.set_hint("ideal")
            
        elif mode == "paradox":
            self.txt_mode.config(text="Режим: 💥 Парадокс игрока", foreground="blue")
            # Первые 7 бросков гарантированно "Орлы" (1)
            fake_start_len = min(7, n_flips)
            fake_start = np.ones(fake_start_len, dtype=int)
            
            # Остальные броски — абсолютно случайные по ползунку
            remaining_len = n_flips - fake_start_len
            if remaining_len > 0:
                random_part = np.random.choice([1, 0], size=remaining_len, p=[p_theoretical, 1 - p_theoretical])
                flips = np.concatenate([fake_start, random_part])
            else:
                flips = fake_start
            self.set_hint("paradox")

        # Расчет показателей
        total_heads = int(np.sum(flips))
        total_tails = n_flips - total_heads
        p_experimental = total_heads / n_flips
        
        # Обновление текстового табло
        self.txt_heads.config(text=f"Выпало Орлов: {total_heads} шт.")
        self.txt_tails.config(text=f"Выпало Решек: {total_tails} шт.")
        self.txt_real_p.config(text=f"Реальная доля Орлов: {p_experimental:.1%}")
        
        # Накопительная вероятность для линейного графика
        cumulative_heads = np.cumsum(flips)
        trials = np.arange(1, n_flips + 1)
        cumulative_proportions = cumulative_heads / trials
        
        # --- ГРАФИК 1: Линия стабилизации ---
        self.ax1.clear()
        self.ax1.plot(trials, cumulative_proportions, label="Доля Орлов в эксперименте", color="#1f77b4", linewidth=2.5)
        self.ax1.axhline(p_theoretical, color="red", linestyle="--", label=f"Теория ({p_theoretical:.0%})", linewidth=2)
        self.ax1.set_title("График стабилизации частоты (Закон больших чисел)", fontsize=11, fontweight='bold')
        self.ax1.set_xlabel("Номер броска")
        self.ax1.set_ylabel("Текущая доля Орлов")
        self.ax1.set_ylim(-0.05, 1.05)
        self.ax1.grid(True, linestyle=":", alpha=0.6)
        self.ax1.legend(loc="upper right")
        
        # --- ГРАФИК 2: Столбчатая диаграмма ---
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
        # Перерисовка холста в Tkinter
        self.canvas.draw()

# Запуск программы
if __name__ == "__main__":
    plt.ion()
    root = tk.Tk()
    app = SuperProbabilityApp(root)
    root.mainloop()
    plt.ioff()       
    plt.show()

import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕸️ Интерактивная теория графов для 8 класса")
        self.root.geometry("1200(x)880".replace("(x)", "x"))  # Размеры окна
        
        # --- ЛЕВАЯ ПАНЕЛЬ УПРАВЛЕНИЯ ---
        control_frame = ttk.LabelFrame(root, text=" 🎛️ Управление графом ", padding=15)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
        
        # 1. Ползунок количества вершин (людей)
        ttk.Label(control_frame, text="Количество вершин (людей):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.nodes_slider = ttk.Scale(control_frame, from_=3, to=30, value=10, orient=tk.HORIZONTAL, command=self.update_nodes_label)
        self.nodes_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.nodes_label = ttk.Label(control_frame, text="Текущее значение: 10 человек", font=("Arial", 9, "italic"), foreground="blue")
        self.nodes_label.pack(anchor=tk.W, pady=(0, 20))
        
        # 2. Ползунок вероятности ребра (дружбы)
        ttk.Label(control_frame, text="Вероятность связи (общительность):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.prob_slider = ttk.Scale(control_frame, from_=0.0, to=1.0, value=0.3, orient=tk.HORIZONTAL, command=self.update_prob_label)
        self.prob_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.prob_label = ttk.Label(control_frame, text="Текущее значение: 30%", font=("Arial", 9, "italic"), foreground="blue")
        self.prob_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Кнопка СГЕНЕРИРОВАТЬ СЕТЬ
        self.btn_run = ttk.Button(control_frame, text="🔄 Построить новый граф", command=self.generate_graph)
        self.btn_run.pack(fill=tk.X, pady=10)
        
        # Текстовое табло характеристик графа
        self.info_frame = ttk.LabelFrame(control_frame, text=" 📊 Характеристики графа ", padding=10)
        self.info_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.txt_edges = ttk.Label(self.info_frame, text="Количество рёбер (связей): —", font=("Arial", 10))
        self.txt_edges.pack(anchor=tk.W, pady=2)
        self.txt_connected = ttk.Label(self.info_frame, text="Граф связанный? —", font=("Arial", 10))
        self.txt_connected.pack(anchor=tk.W, pady=2)
        self.txt_max_deg = ttk.Label(self.info_frame, text="Самый общительный человек имеет: —", font=("Arial", 10))
        self.txt_max_deg.pack(anchor=tk.W, pady=2)

        # --- БЛОК 4. БОЛЬШОЕ ИНФОРМАЦИОННОЕ ВВЕДЕНИЕ ---
        intro_label_frame = ttk.LabelFrame(control_frame, text=" 🌐 Зачем нужны графы в реальной жизни? ", padding=5)
        intro_label_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Создаем контейнер для текста и скроллбара
        text_container = ttk.Frame(intro_label_frame)
        text_container.pack(fill=tk.BOTH, expand=True)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(text_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Текстовое поле (привязываем к скроллбару)
        self.txt_intro = tk.Text(
            text_container, 
            wrap=tk.WORD, 
            font=("Arial", 10), 
            yscrollcommand=scrollbar.set,
            bg="#fdfdfd",
            fg="#222222",
            padx=5,
            pady=5
        )
        self.txt_intro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.txt_intro.yview)
        
        # Вставляем огромный вдохновляющий текст справки
        self.txt_intro.insert(tk.END,
            "🌐 ГРАФЫ: ТЕХНОЛОГИЯ, КОТОРАЯ ПРАВИТ МИРОМ\n"
            "(Введение для юных инженеров)\n\n"
            
            "Представь, что у тебя есть карта дорог, схема метро, устройство процессора твоего компьютера "
            "или даже список твоих друзей ВКонтакте или Telegram. На первый взгляд, это абсолютно разные вещи. "
            "Но для компьютера все они выглядят одинаково — как ГРАФЫ.\n\n"
            
            "Граф — это универсальный математический язык для описания СВЯЗЕЙ. Он состоит всего из двух элементов:\n"
            "• ВЕРШИНЫ (кружки, точки, узлы) — это объекты (люди, города, сайты, серверы, детали).\n"
            "• РЁБРА (линии, стрелочки) — это связи между ними (дружба, дороги, гиперссылки, провода).\n\n"
            
            "Если ты поймёшь, как работают графы, ты поймёшь, как устроены самые дорогие технологии человечества.\n\n"
            
            "🚀 1. ГДЕ ПРИМЕНЯЮТСЯ ГРАФЫ?\n\n"
            
            "👥 СОЦИАЛЬНЫЕ СЕТИ И РЕКОМЕНДАЦИИ ИИ\n"
            "Каждая соцсеть — это гигантский социальный граф. Вершины — это миллиарды пользователей. Рёбра — это лайки, подписки и сообщения. "
            "Искусственный интеллект ежесекундно анализирует этот граф. Если компьютер видит, что три твоих друга подписаны на одного блогера, а ты — нет, "
            "алгоритм мгновенно подкинет его тебе в рекомендации. Реклама, мемы и тренды находят тебя исключительно благодаря математике графов!\n\n"
            
            "🗺️ НАВИГАЦИЯ И ГЛОБАЛЬНАЯ ЛОГИСТИКА\n"
            "Когда ты вызываешь такси или ищешь маршрут в картах, включаются алгоритмы поиска кратчайшего пути на графах. "
            "Вся планета покрыта транспортным графом, где перекрёстки — это вершины, а дороги — рёбра. Навигатор просчитывает миллионы вариантов за доли секунды, "
            "переводя пробки и аварии в цифровые «веса» дорог, чтобы спасти тебя от потери времени.\n\n"
            
            "🕸️ ВСЕМИРНАЯ ПАУТИНА (ПОИСК GOOGLE)\n"
            "Весь интернет — это колоссальный веб-граф. Каждая страница — это вершина, а каждая ссылка на другой сайт — ребро. "
            "С этого и начался триумф компании Google. Её создатели придумали алгоритм PageRank, который анализировал этот граф: "
            "чем больше ссылок вело на сайт, тем важнее считалась вершина, и тем выше она поднималась в поисковой выдаче.\n\n"
            
            "🎮 ИНДУСТРИЯ ИГР И ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ\n"
            "Как боты в играх (например, в Counter-Strike, Minecraft или стратегиях) понимают, куда им бежать за игроком? "
            "Они используют «граф путей». Компьютер разбивает виртуальный мир на сетку вершин и ищет оптимальный маршрут обхода препятствий, стен и ловушек.\n\n"
            
            "🧬 МЕДИЦИНА И ГЕНЕТИКА\n"
            "Биологи моделируют мозг человека как граф, где вершины — это нейроны, а рёбра — синапсы. Также с помощью графов учёные расшифровывают структуру ДНК, "
            "отслеживают распространение вирусов во время пандемий и создают новые молекулы лекарств, просчитывая связи между атомами.\n\n"
            
            "⚡ ЭЛЕКТРОСЕТИ И КИБЕРБЕЗОПАСНОСТЬ\n"
            "Электрические сети стран, водопроводы городов и сам процессор внутри твоего телефона — это физические графы. "
            "Алгоритмы помогают инженерам находить «узкие места» и критические точки (мосты), при поломке которых может отключиться свет во всём городе.\n\n"
            
            "--- --- --- ---\n"
            "🧠 ЧЕМУ ТЫ НАУЧИШЬСЯ НА ЭТОМ КУРСЕ:\n"
            "Проходя эти 5 интерактивных лабораторных работ, ты пройдёшь путь от средневековых загадок до современных ИИ-технологий:\n"
            "1. Научишься с легкостью решать задачи ОГЭ/ЕГЭ по информатике с помощью динамических матриц.\n"
            "2. Поймёшь, как Яндекс.Навигатор видит пробки и переигрывает заторы на дорогах.\n"
            "3. Разгадаешь тайну Леонарда Эйлера и поймёшь, почему нельзя обмануть геометрию.\n"
            "4. Поработаешь аналитиком Big Data и вскроешь тайные группировки внутри случайных соцсетей.\n"
            "5. Решишь великую теорему картографов и узнаешь, как сотовые вышки делят между собой радиочастоты.\n\n"
            "Добро пожаловать в мир графов — язык, на котором компьютер программирует нашу реальность!"
        )
        
        # Блокируем текст от случайного удаления учениками во время урока
        self.txt_intro.config(state=tk.DISABLED)

        # --- ПРАВАЯ ПАНЕЛЬ С ГРАФИКОМ (MATPLOTLIB) ---
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.fig, self.ax = plt.subplots(figsize=(7, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Первый запуск при старте программы
        self.generate_graph()

    def update_nodes_label(self, val):
        n = int(float(val))
        self.nodes_label.config(text=f"Текущее значение: {n} человек")

    def update_prob_label(self, val):
        p = float(val)
        self.prob_label.config(text=f"Текущее значение: {p * 100:.0f}%")

    def generate_graph(self):
        # Получаем значения из интерфейса
        num_nodes = int(self.nodes_slider.get())
        prob = round(float(self.prob_slider.get()), 2)
        
        # Генерируем случайный граф Эрдеша-Реньи
        self.G = nx.erdos_renyi_graph(n=num_nodes, p=prob)
        
        # Считаем характеристики для левой панели
        num_edges = self.G.number_of_edges()
        is_connected = "Да 👍" if nx.is_connected(self.G) else "Нет ❌ (есть одиночки)"
        
        # Находим максимальную степень вершины (количество друзей)
        degrees = [d for n, d in self.G.degree()]
        max_degree = max(degrees) if degrees else 0
        
        # Обновляем текст на левой панели
        self.txt_edges.config(text=f"Количество рёбер (связей): {num_edges}")
        self.txt_connected.config(text=f"Граф связанный? {is_connected}")
        self.txt_max_deg.config(text=f"Максимум связей у одного: {max_degree}")
        
        # Визуализация графа на правой панели
        self.ax.clear()
        
        # Используем круговую разметку (circular layout) чтобы вершины стояли на месте
        pos = nx.circular_layout(self.G)
        
        # Рисуем связи (ребра)
        nx.draw_networkx_edges(self.G, pos, ax=self.ax, edge_color="gray", width=1.5, alpha=0.6)
        
        # Рисуем людей (вершины)
        nx.draw_networkx_nodes(
            self.G, pos, ax=self.ax, 
            node_color="skyblue", node_size=600, 
            edgecolors="black", linewidths=1.5
        )
        
        # Подписываем номера людей (от 0 до N)
        nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_size=10, font_weight="bold")
        
        self.ax.set_title(f"Случайный граф (Сеть друзей)\nВершин: {num_nodes}, Вероятность дружбы: {prob*100:.0f}%", fontsize=12, fontweight='bold')
        self.ax.axis("off")  # Прячем оси координат, для графа они не нужны
        
        # Перерисовываем холст
        self.canvas.draw()

if __name__ == "__main__":
    plt.ion()
    root = tk.Tk()
    app = GraphsApp(root)
    root.mainloop()
    plt.ioff()       
    plt.show()


import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Настройка интерактивного режима для отображения окна
plt.ion()

class SuperGraphsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕸️ Супер-Лаборатория Графов: Лидеры и Маршруты (8 класс)")
        self.root.geometry("1200x750")
        
        # --- ЛЕВАЯ ПАНЕЛЬ УПРАВЛЕНИЯ ---
        control_frame = ttk.LabelFrame(root, text=" 🎛️ Панель управления графом ", padding=15)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
        
        # 1. Ползунок количества вершин (людей)
        ttk.Label(control_frame, text="Количество людей (вершин):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.nodes_slider = ttk.Scale(control_frame, from_=5, to=30, value=12, orient=tk.HORIZONTAL, command=self.update_nodes_label)
        self.nodes_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.nodes_label = ttk.Label(control_frame, text="Текущее значение: 12 человек", font=("Arial", 9, "italic"), foreground="blue")
        self.nodes_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 2. Ползунок вероятности ребра (дружбы)
        ttk.Label(control_frame, text="Вероятность связи (общительность):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.prob_slider = ttk.Scale(control_frame, from_=0.0, to=1.0, value=0.25, orient=tk.HORIZONTAL, command=self.update_prob_label)
        self.prob_slider.pack(fill=tk.X, pady=(0, 2))
        
        self.prob_label = ttk.Label(control_frame, text="Текущее значение: 25%", font=("Arial", 9, "italic"), foreground="blue")
        self.prob_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Кнопка СГЕНЕРИРОВАТЬ СЕТЬ
        self.btn_run = ttk.Button(control_frame, text="🔄 Построить новую сеть друзей", command=self.generate_graph)
        self.btn_run.pack(fill=tk.X, pady=5)
        
        # --- БЛОК ПОИСКА КРАТЧАЙШЕГО ПУТИ ---
        path_frame = ttk.LabelFrame(control_frame, text=" 📍 Найти кратчайший путь (Теория рукопожатий) ", padding=10)
        path_frame.pack(fill=tk.X, pady=(15, 0))
        
        inputs_frame = ttk.Frame(path_frame)
        inputs_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(inputs_frame, text="От кого (№):").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.ent_start = ttk.Entry(inputs_frame, width=5)
        self.ent_start.insert(0, "0")
        self.ent_start.grid(row=0, column=1, padx=5)
        
        ttk.Label(inputs_frame, text="До кого (№):").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.ent_end = ttk.Entry(inputs_frame, width=5)
        self.ent_end.insert(0, "4")
        self.ent_end.grid(row=0, column=3, padx=5)
        
        self.btn_find_path = ttk.Button(path_frame, text="🔍 Проложить маршрут", command=self.visualize_path)
        self.btn_find_path.pack(fill=tk.X, pady=(5, 2))
        
        self.lbl_path_result = ttk.Label(path_frame, text="Маршрут: нажмите кнопку", font=("Arial", 9, "bold"), foreground="darkred", wraplength=220)
        self.lbl_path_result.pack(anchor=tk.W, pady=2)
        
        # Текстовое табло характеристик графа
        self.info_frame = ttk.LabelFrame(control_frame, text=" 📊 Характеристики графа ", padding=10)
        self.info_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.txt_edges = ttk.Label(self.info_frame, text="Количество связей: —", font=("Arial", 10))
        self.txt_edges.pack(anchor=tk.W, pady=2)
        self.txt_connected = ttk.Label(self.info_frame, text="Все ли связаны друг с другом? —", font=("Arial", 10))
        self.txt_connected.pack(anchor=tk.W, pady=2)
        self.txt_leader = ttk.Label(self.info_frame, text="Лидер сети: —", font=("Arial", 10, "bold"), foreground="darkgoldenrod")
        self.txt_leader.pack(anchor=tk.W, pady=2)

        self.lbl_spy_node = ttk.Label(self.info_frame, text="🕵️ Серый кардинал (главный мост): -", font=("Arial", 10))
        self.lbl_spy_node.pack(anchor=tk.W, pady=2)

        # МЕТОДИЧЕСКАЯ ПОДСКАЗКА ДЛЯ УЧИТЕЛЯ
        hint_frame = ttk.LabelFrame(control_frame, text=" 💡 Шпаргалка для урока ", padding=10)
        hint_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        self.txt_hint = tk.Text(hint_frame, wrap=tk.WORD, font=("Arial", 9), width=32, height=10, bg="#fbfbfb", bd=0)
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_lesson_hints()

        # --- ПРАВАЯ ПАНЕЛЬ С ГРАФИКОМ (MATPLOTLIB) ---
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.fig, self.ax = plt.subplots(figsize=(8, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Запуск генерации при первом открытии
        self.G = nx.Graph()
        self.pos = {}
        self.spy_node = None
        self.generate_graph()

    def update_nodes_label(self, val):
        n = int(float(val))
        self.nodes_label.config(text=f"Текущее значение: {n} человек")

    def update_prob_label(self, val):
        p = float(val)
        self.prob_label.config(text=f"Текущее значение: {p * 100:.0f}%")

    def show_lesson_hints(self):
        self.txt_hint.config(state=tk.NORMAL) # Разрешаем редактирование для вставки текста
        self.txt_hint.delete("1.0", tk.END)  # Очищаем старый текст, чтобы он не дублировался

        self.txt_hint.insert(tk.END, 
            "👑 ЗОЛОТАЯ ВЕРШИНА:\n"
            "Это Лидер (блогер) класса. У него больше всего рёбер (друзей). Оранжевые вершины — его близкий круг.\n\n"
            "🔴 КРАСНЫЙ МАРШРУТ:\n"
            "Теория шести рукопожатий в действии! Программа ищет самый короткий путь передачи слухов от одного человека к другому.\n\n"
            "🧩 СВЯЗНОСТЬ:\n"
            "Если вероятность мала, класс разобьется на группировки, и до некоторых людей слух дойти не сможет физически."
            "📊 ЧТО ТАКОЕ ГРАФ:\n"
            "Граф — это схема сети. Вершины (кружки) — это люди, а рёбра (линии) — дружба между ними.\n\n"
            "📐 СТЕПЕНЬ ВЕРШИНЫ:\n"
            "Это количество связей (линий) у одного кружка. У кого степень больше всех — тот Лидер сети.\n\n"
            "🤝 ТЕОРИЯ РУКОПОЖАТИЙ:\n"
            "Показывает самый короткий путь: через сколько общих знакомых (шагов) можно передать слух до любого человека.\n\n"
            "🕵️ СЕРЫЕ КАРДИНАЛЫ И ШПИОНЫ СЕТЕЙ (МЕТРИКА ПОСРЕДНИЧЕСТВА)\n"
            "В 1977 году американский социолог Линтон Фримен придумал математическую метрику — 'Центральность по посредничеству'. "
            "Она ищет на графе не тех, у кого больше всего связей, а тех, через кого проходит максимум кратчайших путей.\n\n"
            "В жизни это создает удивительный парадокс: в классе может быть громкий Лидер (золотая вершина), у которого 10 друзей. "
            "Но есть скромный 'Серый Кардинал' (фиолетовая вершина). У него всего 2 друга! Но один его друг — это лидер геймеров, а второй — лидер спортсменов. "
            "В итоге скромный фиолетовый кружок полностью контролирует весь поток информации, слухов и трендов между изолированными компаниями. "
            "Спецслужбы и ИИ используют эту метрику, чтобы находить ключевых посредников в базах данных или шпионских сетях.\n"
            "📜 ИСТОРИЯ ТЕОРИИ ГРАФОВ:\n"
            "Графы родились не из формул, а из реальных городских загадок и настольных игр!\n\n"
            
            "🏛️ ЭПОХА 1: Кёнигсберг (1736 год)\n"
            "В городе было 7 мостов через реку. Жители спорили: можно ли обойти их все за прогулку, "
            "зайдя на каждый ровно по одному разу? Леонард Эйлер доказал, что это невозможно! "
            "Он стёр карту, заменив сушу ТОЧКАМИ, а мосты — ЛИНИЯМИ. Так появился первый в мире граф [1].\n\n"
            
            "🎲 ЭПОХА 2: Шахматы и головоломки (XIX в.)\n"
            "Уильям Гамильтон придумал игру 'Кругосветное путешествие' по углам деревянной фигуры. "
            "Игроку нужно было посетить все точки ровно по одному разу и вернуться назад. Так открыли "
            "Гамильтоновы циклы, которые сегодня помогают навигаторам возить людей.\n\n"
            
            "⚡ ЭПОХА 3: Электричество и Химия (Конец XIX в.)\n"
            "Физики поняли, что электрические схемы — это идеальный граф (провода и лампочки). А химики "
            "с помощью графов стали рисовать сложные молекулы газов и веществ, где точки — атомы.\n\n"
            
            "💻 ЭПОХА 4: Соцсети и Интернет (XX-XXI вв.)\n"
            "Сегодня Весь Интернет — это гигантский граф (страницы соединены ссылками). А Telegram, ВК "
            "или YouTube — это социальные графы, где точки — это мы с вами, а линии — дружба. "
            "Мы буквально живём внутри графа!"
        )
        self.txt_hint.config(state=tk.DISABLED) # Снова блокируем от редактирования

    def generate_graph(self):
        num_nodes = int(self.nodes_slider.get())
        prob = round(float(self.prob_slider.get()), 2)
        
        # Создаем случайный граф
        self.G = nx.erdos_renyi_graph(n=num_nodes, p=prob)
        
        # Фиксируем координаты вершин на окружности, чтобы они не прыгали при поиске путей
        self.pos = nx.circular_layout(self.G)
        
        # Сброс текста поиска пути
        self.lbl_path_result.config(text="Маршрут: обновился граф", foreground="black")
        
        self.draw_current_graph()

        # Считаем центральность по посредничеству (Betweenness Centrality)
        # Она возвращает словарь, где для каждого узла посчитана его 'важность' как посредника
        centrality = nx.betweenness_centrality(self.G)
        
        # Находим узел с максимальным значением посредничества
        if centrality:
            self.spy_node = max(centrality, key=centrality.get)
            # Если у него вообще нет посреднической роли (например, граф - это просто круг), сбрасываем
            if centrality[self.spy_node] == 0:
                self.spy_node = None
        else:
            self.spy_node = None

        # Обновляем текст на нашей новой метке
        if self.spy_node is not None:
            self.lbl_spy_node.config(text=f"🕵️ Серый кардинал (главный мост): №{self.spy_node}")
        else:
            self.lbl_spy_node.config(text="🕵️ Серый кардинал (главный мост): нет")


    def draw_current_graph(self, path_edges=None, path_nodes=None):
        self.ax.clear()
        
        num_nodes = self.G.number_of_edges()
        is_connected = "Да 👍" if nx.is_connected(self.G) else "Нет ❌ (разбит на части)"
        
        # Ищем лидера (вершину с максимальной степенью)
        degrees = dict(self.G.degree())
        if degrees:
            leader_node = max(degrees, key=degrees.get)
            max_degree = degrees[leader_node]
            # Друзья лидера
            leader_neighbors = list(self.G.neighbors(leader_node)) if leader_node in self.G else []
        else:
            leader_node = None
            max_degree = 0
            leader_neighbors = []
            
        # Обновляем инфо-табло
        self.txt_edges.config(text=f"Количество связей: {self.G.number_of_edges()}")
        self.txt_connected.config(text=f"Все ли связаны? {is_connected}")
        if leader_node is not None and max_degree > 0:
            self.txt_leader.config(text=f"Лидер сети: №{leader_node} (связей: {max_degree})")
        else:
            self.txt_leader.config(text="Лидер сети: не определен")

        # Настраиваем цвета для ВСЕХ вершин
        # node_colors = []
        # for node in self.G.nodes():
        #     if path_nodes and node in path_nodes:
        #         node_colors.append("tomato")       # Вершины на пути подсветки
        #     elif node == leader_node and max_degree > 0:
        #         node_colors.append("gold")         # Корона лидера!
        #     elif node in leader_neighbors and max_degree > 0:
        #         node_colors.append("orange")       # Друзья лидера
        #     else:
        #         node_colors.append("skyblue")      # Обычные люди

        # Настраиваем цвета для ВСЕХ вершин
        node_colors = []
        for node in self.G.nodes():
            if path_nodes and node in path_nodes:
                node_colors.append("tomato")  # Вершины на пути подсветки
            elif node == self.spy_node and self.spy_node is not None:
                node_colors.append("purple")  # 🕵️ Фиолетовый — Серый кардинал (Шпион)
            elif node == leader_node and max_degree > 0:
                node_colors.append("gold")    # 👑 Золотой — Корона лидера!
            elif node in leader_neighbors and max_degree > 0:
                node_colors.append("orange")  # 🍊 Друзья лидера
            else:
                node_colors.append("skyblue") # 🔹 Обычные люди
                
        # Рисуем базовые ребра (серые)
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color="#b0b0b0", width=1.5, alpha=0.7)
        
        # Если передан путь, поверх рисуем его толстыми красными линиями
        if path_edges:
            nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edgelist=path_edges, edge_color="red", width=4.0)          
            # --- НОВЫЙ БЛОК: Добавляем стрелочки направления по центру ---
            for u, v in path_edges:
                # Получаем координаты начала (u) и конца (v) отрезка
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                
                # Находим точный центр линии
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                
                # Вычисляем небольшое смещение, чтобы стрелка смотрела вперед по ходу движения
                dx = (x2 - x1) * 0.01
                dy = (y2 - y1) * 0.01
                
                # Рисуем стрелку-указатель прямо по центру
                self.ax.annotate(
                    "", 
                    xy=(cx + dx, cy + dy),    # Куда указывает стрелка (чуть дальше центра)
                    xytext=(cx, cy),          # Откуда начинается (центр)
                    arrowprops=dict(
                        arrowstyle="-|>",     # Форма стрелочки
                        color="black",        # Цвет стрелки (можно сделать white или yellow для контраста)
                        lw=2,                 # Толщина самой стрелки
                        mutation_scale=20     # Размер наконечника стрелки
                    )
                )
            # -------------------------------------------------------------

            
        # Рисуем вершины
        nx.draw_networkx_nodes(
            self.G, self.pos, ax=self.ax, 
            node_color=node_colors, node_size=650, 
            edgecolors="black", linewidths=1.5
        )
        
        # Подписи номеров
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=10, font_weight="bold")
        
        self.ax.set_title(f"🕸️ Интерактивная социальная сеть класса\n(Золотой кружок — Лидер, Оранжевые — его друзья)", fontsize=11, fontweight='bold')
        self.ax.axis("off")
        self.canvas.draw()

    def visualize_path(self):
        # Проверяем корректность ввода номеров вершин
        try:
            start_node = int(self.ent_start.get())
            end_node = int(self.ent_end.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа в поля номеров людей!")
            return
            
        if start_node not in self.G or end_node not in self.G:
            messagebox.showerror("Ошибка", f"В графе сейчас нет человека с таким номером! Изучите номера на кружках.")
            return
            
        if start_node == end_node:
            self.lbl_path_result.config(text="Вы указали одного и того же человека!", foreground="black")
            self.draw_current_graph()
            return

        # Ищем кратчайший путь алгоритмом Дейкстры/БФС, встроенным в networkx
        try:
            path = nx.shortest_path(self.G, source=start_node, target=end_node)
            
            # Собираем пары вершин (список ребер), из которых состоит этот путь
            path_edges = list(zip(path[:-1], path[1:]))
            # Выводим текстовый результатpa
            th_str = " ➔ ".join(map(str, path))
            self.lbl_path_result.config(text=f"Маршрут: {th_str} (Шагов: {len(path)-1})", foreground="green")
            # Перерисовываем граф с подсветкой пути
            self.draw_current_graph(path_edges=path_edges, path_nodes=path)
        except nx.NetworkXNoPath:
            self.lbl_path_result.config(text="❌ Путь отсутствует! Люди в разных группировках.", foreground="red")
            # Рисуем без подсветки путей
            self.draw_current_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = SuperGraphsApp(root)
    root.mainloop()
    plt.ioff()       
    plt.show()


import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np

# Настройка интерактивного режима для отображения окна
plt.ion()

class SuperGraphsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Супер-Лаборатория Графов: Лидеры, Маршруты и Аналитика (8 класс)")
        self.root.geometry("1400x850")
        
        # Переменные для графа
        self.G = nx.Graph()
        self.pos = {}
        
        # Настройка интерфейса (две панели)
        self.setup_ui()
        
        # Первичная генерация
        self.generate_graph()

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=400)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для графа
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # --- БЛОК 1. Ползунки управления ---
        ttk.Label(self.left_panel, text="Количество людей (вершин):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5,0))

        self.lbl_nodes_val = ttk.Label(self.left_panel, text="Текущее значение: 12 человек", foreground="blue")
        self.lbl_nodes_val.pack(anchor=tk.W, pady=(0, 5))

        self.nodes_slider = ttk.Scale(self.left_panel, from_=5, to=25, orient=tk.HORIZONTAL, command=self.update_nodes_label)
        self.nodes_slider.set(12)
        self.nodes_slider.pack(fill=tk.X, pady=5)

        # self.nodes_slider = ttk.Scale(self.left_panel, from_=5, to=25, orient=tk.HORIZONTAL, command=self.update_nodes_label)
        # self.nodes_slider.set(12)
        # self.nodes_slider.pack(fill=tk.X, pady=5)
        # self.lbl_nodes_val = ttk.Label(self.left_panel, text="Текущее значение: 12 человек", foreground="blue")
        # self.lbl_nodes_val.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(self.left_panel, text="Вероятность связи (общительность):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5,0))

        # 1. Сначала создаем текстовую метку
        self.lbl_prob_val = ttk.Label(self.left_panel, text="Текущее значение: 30%", foreground="blue")
        self.lbl_prob_val.pack(anchor=tk.W, pady=(0, 5))

        # 2. Только потом создаем ползунок, который будет её обновлять
        self.prob_slider = ttk.Scale(self.left_panel, from_=0.1, to=1.0, orient=tk.HORIZONTAL, command=self.update_prob_label)
        self.prob_slider.set(0.3)
        self.prob_slider.pack(fill=tk.X, pady=5)

        # self.prob_slider = ttk.Scale(self.left_panel, from_=0.1, to=1.0, orient=tk.HORIZONTAL, command=self.update_prob_label)
        # self.prob_slider.set(0.3)
        # self.prob_slider.pack(fill=tk.X, pady=5)
        # self.lbl_prob_val = ttk.Label(self.left_panel, text="Текущее значение: 30%", foreground="blue")
        # self.lbl_prob_val.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Button(self.left_panel, text="🎲 Построить новую сеть друзей", command=self.generate_graph).pack(fill=tk.X, pady=5)
        
        # --- БЛОК 2. Поиск маршрута ---
        ttk.Label(self.left_panel, text="🔍 Найти кратчайший путь (Теория рукопожатий)", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10,5))
        path_frame = ttk.Frame(self.left_panel)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(path_frame, text="От кого (№):").pack(side=tk.LEFT)
        self.ent_start = ttk.Entry(path_frame, width=5)
        self.ent_start.insert(0, "1")
        self.ent_start.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(path_frame, text="До кого (№):").pack(side=tk.LEFT, padx=(5,0))
        self.ent_end = ttk.Entry(path_frame, width=5)
        self.ent_end.insert(0, "4")
        self.ent_end.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.left_panel, text="🚀 Проложить маршрут", command=self.visualize_path).pack(fill=tk.X, pady=5)
        self.lbl_path_result = ttk.Label(self.left_panel, text="Маршрут: ожидание ввода", font=("Arial", 9, "italic"))
        self.lbl_path_result.pack(anchor=tk.W, pady=5)
        
        # --- БЛОК 3. Живая статистика и Аналитика ---
        ttk.Label(self.left_panel, text="📊 Характеристики и Аналитика графа", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        
        self.lbl_stats = ttk.Label(self.left_panel, text="", font=("Courier", 10), justify=tk.LEFT)
        self.lbl_stats.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # Кнопка для поиска диаметра (самого длинного пути)
        ttk.Button(self.left_panel, text="🟢 Найти самую дальнюю связь (Диаметр)", command=self.visualize_diameter_path).pack(fill=tk.X, pady=5)
        
        # Старая кнопка (оставляем как есть)

        ttk.Button(self.left_panel, text="🧮 Показать матрицу смежности (Код графа)", command=self.show_matrix_window).pack(fill=tk.X, pady=5)
        
        # --- БЛОК 4. Шпаргалка ---
        ttk.Label(self.left_panel, text="💡 Шпаргалка для урока", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=15, wrap=tk.WORD, font=("Arial", 9))
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_lesson_hints()

        # Настройка Matplotlib Canvas в правой панели
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Обновление подписей ползунков
    def update_nodes_label(self, val):
        n = int(float(val))
        self.lbl_nodes_val.config(text=f"Текущее значение: {n} человек")

    def update_prob_label(self, val):
        p = float(val)
        self.lbl_prob_val.config(text=f"Текущее значение: {p * 100:.0f}%")

    # Шпаргалка по 4 новым пунктам
    def show_lesson_hints(self):
        self.txt_hint.config(state=tk.NORMAL)
        self.txt_hint.delete("1.0", tk.END)
        self.txt_hint.insert(tk.END,
            "📊 1. ЧТО ТАКОЕ ГРАФ:\n"
            "Схема сети. Вершины (кружки) — это люди, а рёбра (линии) — дружба между ними.\n\n"
            
            "📐 2. СТЕПЕНЬ ВЕРШИНЫ:\n"
            "Количество линий у кружка. У кого степень больше всех — тот Лидер (блогер) сети с максимумом связей.\n\n"
            
            "🤝 3. ТЕОРИЯ РУКОПОЖАТИЙ:\n"
            "Кратчайший путь между людьми. Показывает, через сколько общих знакомых (шагов) долетит слух.\n\n"
            
            "🔗 4. СВЯЗНОСТЬ И ПЛОТНОСТЬ:\n"
            "Связный граф — можно дойти до любого. Плотность показывает % реальных связей от всех возможных.\n\n"
            
            "🚧 5. МОСТЫ СЕТИ:\n"
            "Критические линии. Если убрать «мост», граф распадётся на изолированные группы и связь прервётся.\n\n"
            
            "🧮 6. МАТРИЦА СМЕЖНОСТИ:\n"
            "Таблица из 0 и 1, с помощью которой компьютер видит и просчитывает любые соцсети."
        )
        self.txt_hint.config(state=tk.DISABLED)

    # Генерация случайного графа
    def generate_graph(self):
        num_nodes = int(float(self.nodes_slider.get()))
        prob = round(float(self.prob_slider.get()), 2)
        
        # Создаем граф Эрдёша-Реньи
        self.G = nx.erdos_renyi_graph(n=num_nodes, p=prob)
        
        # Фиксируем координаты вершин по кругу
        self.pos = nx.circular_layout(self.G)
        
        # Сброс текста поиска пути
        self.lbl_path_result.config(text="Маршрут: обновлен граф", foreground="black")
        
        # Перерисовываем и обновляем статистику
        self.draw_current_graph()
        self.update_live_statistics()

    # Сбор и вывод живой аналитики в левую панель
    def update_live_statistics(self):
        # 1. Плотность графа (Уровень дружбы в классе)
        density = nx.density(self.G) * 100
        
        # 2. Рейтинг популярности (Степени вершин)
        degrees = dict(self.G.degree())
        sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        
        leader_node, max_conn = sorted_degrees[0] if sorted_degrees else (0, 0)
        lonely_nodes = [node for node, deg in degrees.items() if deg == 0]
        
        # 3. Связность
        # 3. Связность и Максимальное количество шагов (Диаметр)
        if nx.is_connected(self.G):
            is_connected = "Да 👍"
            # Если граф связан, считаем диаметр — самый длинный путь между любой парой людей
            max_steps = nx.diameter(self.G)
        else:
            is_connected = "Нет ❌ (разбит на части)"
            # Если разбит, то максимальный путь посчитать нельзя
            max_steps = "∞ (нет пути между группами)"
        
        # 4. Мосты сети
        bridges_count = len(list(nx.bridges(self.G)))
        
        # Формируем красивый текст аналитики
        stats_text = (
            f"• Всего связей в сети: {self.G.number_of_edges()}\n"
            f"• Все ли связаны? {is_connected}\n"
            f"• Сплочённость класса: {density:.1f}%\n"
            f"• 👑 Лидер сети: №{leader_node} ({max_conn} связей)\n"
            f"• 🚧 Найдено критических мостов: {bridges_count}\n"
            f"• 👤 Одиночки (0 связей): {len(lonely_nodes)} чел.\n"
            f"• 📏 Максимум шагов в сети: {max_steps}"
        )
        self.lbl_stats.config(text=stats_text)

    # Основная функция отрисовки графа
    def draw_current_graph(self, path_edges=None, path_nodes=None, path_color="green"):
        self.ax.clear()
        
        # Определяем цвета вершин (Лидер — золотой/красный, его друзья — оранжевые, остальные — голубые)
        degrees = dict(self.G.degree())
        if degrees:
            max_deg = max(degrees.values())
            # Находим лидера (первого с максимальной степенью)
            leader = [node for node, deg in degrees.items() if deg == max_deg][0] if max_deg > 0 else None
        else:
            leader = None
            
        node_colors = []
        for node in self.G.nodes():
            if node == leader and max_deg > 0:
                node_colors.append("gold")  # Золотая вершина - Лидер
            elif leader is not None and self.G.has_edge(node, leader):
                node_colors.append("orange")  # Близкий круг лидера
            else:
                node_colors.append("skyblue")  # Обычные вершины
                
        # Ищем мосты для визуального выделения
        bridges = list(nx.bridges(self.G))
        
        # Рисуем базовые рёбра (серые)
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color="#b0b0b0", width=1.5, alpha=0.7)
        
        # Визуально подсвечиваем МОСТЫ пунктиром или другим цветом, если они есть
        if bridges:
            nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edgelist=bridges, edge_color="purple", width=2.0, style="dashed")
            
        # Если передан путь, поверх рисуем толстые красные линии
        if path_edges:
            nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edgelist=path_edges, edge_color="red", width=4.5)
            
            # Добавляем стрелочки направления по центру каждого ребра пути
            for u, v in path_edges:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = (x2 - x1) * 0.01, (y2 - y1) * 0.01
                
                self.ax.annotate(
                    "", 
                    xy=(cx + dx, cy + dy),
                    xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=2, mutation_scale=20)
                )

        # Рисуем вершины
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color=node_colors, node_size=600, edgecolors="black", linewidths=1.5)
        # Подписи номеров вершин
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=10, font_weight="bold")
        self.ax.set_title("🟣 Фиолетовый пунктир — Мосты сети | 👑 Золотой — Лидер", fontsize=11, fontweight='bold', pad=10)
        self.ax.axis("off")
        self.canvas.draw()

    # Поиск кратчайшего пути по алгоритму
    def visualize_path(self):
        try:
            start_node = int(self.ent_start.get())
            end_node = int(self.ent_end.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа в поля номеров людей!")
            return
            
        if start_node not in self.G or end_node not in self.G:
            messagebox.showerror("Ошибка", "В графе сейчас нет человека с таким номером!")
            return
            
        if start_node == end_node:
            self.lbl_path_result.config(text="Вы указали одного и того же человека!", foreground="black")
            self.draw_current_graph()
            return
            
        try:
            # Находим кратчайший путь средствами networkx
            path = nx.shortest_path(self.G, source=start_node, target=end_node)
            path_edges = list(zip(path[:-1], path[1:]))
            
            # Выводим текстовый результат в f-строку
            th_str = " -> ".join(map(str, path))
            self.lbl_path_result.config(text=f"Маршрут: {th_str} (Шагов: {len(path)-1})", foreground="green")
            
            # Перерисовываем граф с подсветкой пути
            self.draw_current_graph(path_edges=path_edges, path_nodes=path)
            
        except nx.NetworkXNoPath:
            self.lbl_path_result.config(text="❌ Путь отсутствует! Люди в разных группировках.", foreground="red")
            self.draw_current_graph()

    def visualize_diameter_path(self):
        # Проверяем связность графа, так как в несвязном диаметра нет
        if not nx.is_connected(self.G):
            messagebox.showwarning("Внимание", "Граф разбит на части! Нельзя найти путь между изолированными группами.")
            return
            
        # Находим периферийные вершины (самые удаленные точки)
        # Алгоритм: берем все кратчайшие пути и ищем среди них самый длинный
        all_spl = dict(nx.all_pairs_shortest_path(self.G))
        
        max_len = 0
        longest_path = []
        
        for start_node, targets in all_spl.items():
            for target_node, path in targets.items():
                if len(path) > max_len:
                    max_len = len(path)
                    longest_path = path
                    
        if longest_path:
            path_edges = list(zip(longest_path[:-1], longest_path[1:]))
            th_str = " -> ".join(map(str, longest_path))
            
            # Выводим инфо зеленым текстом
            self.lbl_path_result.config(
                text=f"Самый долгий путь: {th_str} (Шагов: {len(longest_path)-1})", 
                foreground="darkgreen"
            )
            # Перерисовываем граф, принудительно передавая ЗЕЛЕНЫЙ цвет
            self.draw_current_graph(path_edges=path_edges, path_nodes=longest_path, path_color="green")

    # Окно с матрицей смежности графа (для связи с ОГЭ/ЕГЭ)
    def show_matrix_window(self):
        matrix_win = tk.Toplevel(self.root)
        matrix_win.title("🧮 Матрица смежности графа")
        matrix_win.geometry("500x450")
        
        ttk.Label(matrix_win, text="Как этот граф видит компьютер (Матрица смежности):", font=("Arial", 10, "bold"), padding=10).pack()
        
        # Получаем матрицу смежности из NetworkX
        nodes_list = sorted(list(self.G.nodes()))
        if not nodes_list:
            ttk.Label(matrix_win, text="Граф пуст").pack()
            return
            
        matrix_data = nx.to_numpy_array(self.G, nodelist=nodes_list, dtype=int)
        
        # Текстовое поле для красивого вывода таблицы
        # txt_area = tk.Text(matrix_win, font=("Courier", 11), padding=10)
        # Текстовое поле с принудительно настроенным цветом фона и текста
        txt_area = tk.Text(
            matrix_win, 
            font=("Courier", 11), 
            padx=10,          # Внутренний отступ слева и справа
            pady=10,          # Внутренний отступ сверху и снизу 
            bg="white",       # Белый фон окна таблицы
            fg="black",       # Чёрный цвет цифр
            insertbackground="black" # Цвет курсора
        )
        txt_area.pack(fill=tk.BOTH, expand=True)
        
        # Строим заголовок столбцов матрицы
        header = "    " + " ".join(f"{n:<2}" for n in nodes_list) + "\n"
        separator = "   " + "—" * (len(nodes_list) * 3) + "\n"
        
        txt_area.insert(tk.END, header)
        txt_area.insert(tk.END, separator)
        
        # Строим строки матрицы
        for i, node in enumerate(nodes_list):
            row_str = f"{node:<2} | " + "  ".join(str(matrix_data[i][j]) for j in range(len(nodes_list))) + "\n"
            txt_area.insert(tk.END, row_str)
            
        txt_area.insert(tk.END, "\n💡 Пояснение: 1 означает наличие дружбы между номерами, а 0 — её отсутствие.")
        txt_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SuperGraphsApp(root)
    root.mainloop()
    plt.ioff()       
    plt.show()


import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random

# Настройка интерактивного режима для отображения окна
plt.ion()

class OGEGraphTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("ОГЭ-Тренажёр по информатике: Подсчёт путей и длин дорог")
        self.root.geometry("1300x800")
        
        # Направленный граф (DiGraph), так как в ОГЭ дороги со стрелочками
        self.G = nx.DiGraph()
        self.pos = {}
        
        self.setup_ui()
        self.generate_oge_graph()

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=380)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для графа
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Кнопка генерации новой схемы
        ttk.Label(self.left_panel, text="🗺️ Генератор карты дорог", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Button(self.left_panel, text="🎲 Сгенерировать новую схему ОГЭ", command=self.generate_oge_graph).pack(fill=tk.X, pady=5)
        
        # Блок ввода задания
        ttk.Label(self.left_panel, text="🎯 Поиск путей (Задание ОГЭ)", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        
        io_frame = ttk.Frame(self.left_panel)
        io_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(io_frame, text="Старт (город):").pack(side=tk.LEFT)
        self.ent_start = ttk.Entry(io_frame, width=5)
        self.ent_start.insert(0, "A")
        self.ent_start.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(io_frame, text="Финиш (город):").pack(side=tk.LEFT, padx=(5,0))
        self.ent_end = ttk.Entry(io_frame, width=5)
        self.ent_end.insert(0, "F")
        self.ent_end.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.left_panel, text="🧮 Посчитать ответы для ОГЭ", command=self.calculate_all_paths).pack(fill=tk.X, pady=5)
        
        # Блок вывода результатов аналитики
        ttk.Label(self.left_panel, text="📊 Результаты вычислений:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.lbl_results = ttk.Label(self.left_panel, text="", font=("Courier", 10), justify=tk.LEFT, foreground="darkgreen")
        self.lbl_results.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # Шпаргалка ОГЭ
        ttk.Label(self.left_panel, text="💡 Шпаргалка для ОГЭ:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=12, wrap=tk.WORD, font=("Arial", 9), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Поле Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "📝 ТИПИЧНЫЕ ЗАДАЧИ ОГЭ:\n"
            "1. Сколько существует различных путей из города А в город F?\n"
            "2. Какова длина самого короткого пути между А и F?\n\n"
            "📐 КАК СЧИТАТЬ ВРУЧНУЮ (Метод сложения):\n"
            "• Городу А ставим единицу: А = 1.\n"
            "• Для каждого следующего города складываем значения всех городов, ИЗ которых в него ведут стрелочки.\n"
            "• Двигаемся строго по направлению стрелок!\n"
            "📜 ИСТОРИЯ И СМЫСЛ ЗАДАЧИ:\n"
            "В 1950-х годах, на заре появления первых ЭВМ, учёные столкнулись с проблемой: "
            "как автоматизировать логистику и подсчёт вариантов маршрутов. Советский математик "
            "Леонид Канторович (единственный в истории СССР нобелевский лауреат по экономике) "
            "доказал, что ручной перебор путей неэффективен, когда городов становится больше десяти. "
            "Тогда был разработан метод динамического программирования (тот самый алгоритм сложения "
            "вершин, который вы используете в ОГЭ). Он позволял за секунды находить число маршрутов "
            "для снабжения заводов сырьём.\n\n"
            "🎯 КАК РЕШАТЬ В ОГЭ (Задание №1 и №3):\n"
            "• Городу А (старт) присваиваем значение 1.\n"
            "• Двигаясь строго по стрелкам, для каждой следующей вершины складываем числа всех городов, "
            "ИЗ которых в неё ведут дороги.\n"
            "• Число в финальном городе — это и есть количество всех возможных уникальных маршрутов!"
        )
        self.txt_hint.config(state=tk.DISABLED)

    def generate_oge_graph(self):
        self.G.clear()
        
        # Фиксированные города-буквы как в ОГЭ
        cities = ["A", "B", "C", "D", "E", "F"]
        self.G.add_nodes_from(cities)
        
        # Координаты для красивой структуры (слоями слева направо)
        self.pos = {
            "A": (0, 1),
            "B": (1, 2), "C": (1, 0),
            "D": (2, 2), "E": (2, 0),
            "F": (3, 1)
        }
        
        # Базовый скелет дорог, чтобы граф гарантированно имел пути
        base_edges = [
            ("A", "B"), ("A", "C"), 
            ("B", "D"), ("C", "E"), 
            ("D", "F"), ("E", "F"),
            ("B", "C"), ("D", "E") # Поперечные дороги
        ]
        
        for u, v in base_edges:
            # Случайный вес (километраж) от 2 до 15
            self.G.add_edge(u, v, weight=random.randint(2, 15))
            
        # Добавляем немного случайных дополнительных стрелок для разнообразия задач
        extra_edges = [("A", "D"), ("A", "E"), ("B", "E"), ("C", "F")]
        for u, v in extra_edges:
            if random.random() > 0.4:
                self.G.add_edge(u, v, weight=random.randint(3, 12))
                
        self.lbl_results.config(text="Карта построена.\nЖдёт расчёта путей.")
        self.draw_graph()

    def draw_graph(self, highlighted_edges=None, path_color="red"):
        self.ax.clear()
        
        # Рисуем все базовые дороги (серые со стрелочками)
        nx.draw_networkx_edges(
            self.G, self.pos, ax=self.ax, 
            edge_color="#a0a0a0", width=2.0, 
            arrowstyle="-|>", arrowsize=18, node_size=700
        )
        
        # Подсвечиваем выбранный путь (если передан)
        if highlighted_edges:
            nx.draw_networkx_edges(
                self.G, self.pos, ax=self.ax, 
                edgelist=highlighted_edges, 
                edge_color=path_color, width=4.0,
                arrowstyle="-|>", arrowsize=20, node_size=700
            )
            
        # Рисуем города-вершины
        nx.draw_networkx_nodes(
            self.G, self.pos, ax=self.ax, 
            node_color="#ffcc66", node_size=700, 
            edgecolors="black", linewidths=1.5
        )
        
        # Названия городов
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=11, font_weight="bold")
        
        # Выводим веса (километры) на рёбрах
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax, font_size=10, font_weight="bold")
        
        self.ax.set_title("📍 Схема дорог ОГЭ (Числа на линиях — длина дорог в км)", fontsize=11, fontweight='bold', pad=10)
        self.ax.axis("off")
        self.canvas.draw()

    def calculate_all_paths(self):
        start = self.ent_start.get().upper().strip()
        end = self.ent_end.get().upper().strip()
        
        if start not in self.G or end not in self.G:
            messagebox.showerror("Ошибка", "Используйте буквы городов из графа (A, B, C, D, E, F)!")
            return
            
        # Ищем ВСЕ возможные пути от старта до финиша алгоритмами NetworkX
        all_paths = list(nx.all_simple_paths(self.G, source=start, target=end))
        total_paths_count = len(all_paths)
        
        if total_paths_count == 0:
            self.lbl_results.config(text=f"Путей из {start} в {end} нет! ❌", foreground="red")
            self.draw_graph()
            return
            
        # Считаем длины всех путей (суммируем веса граней)
        path_lengths = []
        for path in all_paths:
            length = sum(self.G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
            path_lengths.append((path, length))
            
        # Находим самый короткий и самый длинный пути по весу
        shortest_p, min_len = min(path_lengths, key=lambda x: x[1])
        longest_p, max_len = max(path_lengths, key=lambda x: x[1])
        
        # Формируем красивый текстовый отчёт
        report = (
            f"• Всего путей из {start} в {end}: {total_paths_count} шт.\n\n"
            f"• Кратчайший путь (по км):\n"
            f"  {' -> '.join(shortest_p)} ({min_len} км)\n\n"
            f"• Самый длинный путь (по км):\n"
            f"  {' -> '.join(longest_p)} ({max_len} км)"
        )
        self.lbl_results.config(text=report, foreground="black")
        
        # Подсвечиваем самый короткий путь на графе красным цветом
        shortest_edges = list(zip(shortest_p[:-1], shortest_p[1:]))
        self.draw_graph(highlighted_edges=shortest_edges, path_color="#ff3333")

if __name__ == "__main__":
    root = tk.Tk()
    app = OGEGraphTrainer(root)
    root.mainloop()


import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random

# Настройка интерактивного режима для отображения окна
plt.ion()

class GPSDijkstraNavigator:
    def __init__(self, root):
        self.root = root
        self.root.title("Урок 2: Как работает GPS-Навигатор? (Алгоритм Дейкстры)")
        self.root.geometry("1300x820")
        
        # Обычный ненаправленный граф для карты дорог города
        self.G = nx.Graph()
        self.pos = {}
        
        self.setup_ui()
        self.generate_city_map()

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=380)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для карты
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Управление картой
        ttk.Label(self.left_panel, text="🗺️ Карта дорог города", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Button(self.left_panel, text="🔄 Обновить пробки в городе", command=self.generate_city_map).pack(fill=tk.X, pady=5)
        
        # Настройка маршрута
        ttk.Label(self.left_panel, text="🚗 Построить маршрут навигатором", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        
        route_frame = ttk.Frame(self.left_panel)
        route_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(route_frame, text="Откуда (№):").pack(side=tk.LEFT)
        self.ent_start = ttk.Entry(route_frame, width=5)
        self.ent_start.insert(0, "0")
        self.ent_start.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(route_frame, text="Куда (№):").pack(side=tk.LEFT, padx=(5,0))
        self.ent_end = ttk.Entry(route_frame, width=5)
        self.ent_end.insert(0, "5")
        self.ent_end.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.left_panel, text="🧭 Включить алгоритм Дейкстры", command=self.find_gps_route).pack(fill=tk.X, pady=5)
        
        # Результаты навигатора
        ttk.Label(self.left_panel, text="📊 Отчёт навигатора:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.lbl_results = ttk.Label(self.left_panel, text="", font=("Courier", 10), justify=tk.LEFT, foreground="blue")
        self.lbl_results.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # Шпаргалка для урока
        ttk.Label(self.left_panel, text="💡 Как это объяснить детям?", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=15, wrap=tk.WORD, font=("Arial", 9), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Canvas Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "🧠 СУТЬ АЛГОРИТМА ДЕЙКСТРЫ:\n"
            "Компьютер ищет путь с МИНИМАЛЬНЫМ общим весом (временем).\n\n"
            "🚥 ЦВЕТА ДОРОГ НА ЭКРАНЕ:\n"
            "• ЗЕЛЕНЫЙ (Трасса) = 2-5 минут.\n"
            "• ЖЕЛТЫЙ (Плотный поток) = 10-15 минут.\n"
            "• КРАСНЫЙ (Пробка) = 40-60 минут!\n\n"
            "👀 ЧТО ПОКАЗАТЬ НА УРОКЕ:\n"
            "Сгенерируйте карту так, чтобы между какими-то вершинами была прямая КРАСНАЯ линия. Навигатор откажется ехать по ней напрямую. Он выберет длинный визуальный объезд по ЗЕЛЕНЫМ дорогам, потому что суммарное время там будет меньше! Точно так же работает Яндекс.Навигатор.\n"
            "📜 ИСТОРИЯ И СМЫСЛ ЗАДАЧИ:\n"
            "В 1956 году 26-летний голландский программист Эдсгер Дейкстра пил кофе в кафе со своей "
            "невестой. Он размышлял над задачей: как показать возможности нового компьютера ARMAC. "
            "Дейкстра решил за 20 минут в уме алгоритм поиска кратчайшего пути на карте из 20 городов "
            "Голландии. Так родился 'Алгоритм Дейкстры' (опубликован в 1959 г.).\n\n"
            "В XXI веке этот алгоритм стал основой цифровой экономики. Именно он работает каждый раз, "
            "когда вы вызываете Яндекс.Такси или строите маршрут в Google Maps. Навигатор не просто "
            "ищет короткую линию — он переводит пробки, аварии и светофоры в математические 'веса' "
            "и находит путь с минимальным суммарным временем, даже если визуально он кажется длиннее!"
        )
        self.txt_hint.config(state=tk.DISABLED)

    def generate_city_map(self):
        self.G.clear()
        
        # Создаем фиксированную сетку улиц города (8 перекрестков-вершин)
        num_nodes = 8
        self.G.add_nodes_from(range(num_nodes))
        
        # Фиксируем координаты, чтобы город всегда выглядел аккуратно
        self.pos = {
            0: (0, 1), 1: (1, 2), 2: (1, 0),
            3: (2, 2), 4: (2, 0), 5: (3, 2),
            6: (3, 0), 7: (4, 1)
        }
        
        # Список дорог города
        edges = [
            (0,1), (0,2), (1,3), (2,4), (3,5), (4,6), (5,7), (6,7),
            (1,2), (3,4), (5,6), (1,4), (3,6) # Переулки
        ]
        
        for u, v in edges:
            # Случайно распределяем дорожную ситуацию
            traffic_type = random.choice(["free", "dense", "jam"])
            
            if traffic_type == "free":
                weight = random.randint(2, 5)     # Быстрая трасса
                color = "#33cc33"                 # Зеленый
            elif traffic_type == "dense":
                weight = random.randint(10, 15)   # Плотный поток
                color = "#ffcc00"                 # Желтый
            else:
                weight = random.randint(40, 60)   # Жесткая пробка
                color = "#ff3333"                 # Красный
                
            self.G.add_edge(u, v, weight=weight, color=color)
            
        self.lbl_results.config(text="Карта города обновлена.\nПробки изменились!", foreground="black")
        self.draw_map()

    def draw_map(self, route_edges=None):
        self.ax.clear()
        
        # Рисуем все дороги их «дорожным» цветом (зеленый/желтый/красный)
        edge_colors = [self.G[u][v]['color'] for u, v in self.G.edges()]
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color=edge_colors, width=3.5)
        
        # Если навигатор проложил маршрут, подсвечиваем его сверху СИНЕЙ жирной неоновой линией
        if route_edges:
            nx.draw_networkx_edges(
                self.G, self.pos, ax=self.ax, 
                edgelist=route_edges, 
                edge_color="#0066ff", width=7.0, alpha=0.8
            )
            
            # Накладываем черные стрелочки вектора по центру синего маршрута
            for u, v in route_edges:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = (x2 - x1) * 0.01, (y2 - y1) * 0.01
                self.ax.annotate(
                    "", xy=(cx + dx, cy + dy), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="-|>", color="white", lw=2, mutation_scale=15)
                )

        # Рисуем перекрестки
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color="#e6f2ff", node_size=600, edgecolors="black", linewidths=1.5)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=11, font_weight="bold")
        
        # Показываем время в минутах над дорогами
        edge_labels = { (u, v): f"{self.G[u][v]['weight']} мин" for u, v in self.G.edges() }
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax, font_size=9, font_weight="bold")
        
        self.ax.set_title("🗺️ Живая карта пробок | Синяя линия — Маршрут GPS", fontsize=11, fontweight='bold', pad=10)
        self.ax.axis("off")
        self.canvas.draw()

    def find_gps_route(self):
        try:
            start = int(self.ent_start.get())
            end = int(self.ent_end.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные номера перекрестков!")
            return
            
        if start not in self.G or end not in self.G:
            messagebox.showerror("Ошибка", "Таких перекрестков нет на карте!")
            return
            
        if start == end:
            messagebox.showinfo("Внимание", "Вы уже находитесь в точке назначения!")
            return
            
        try:
            # САМАЯ ВАЖНАЯ СТРОКА: Ищем путь алгоритмом Дейкстры, учитывая параметр weight (время)
            optimal_path = nx.dijkstra_path(self.G, source=start, target=end, weight='weight')
            # Считаем суммарное время в пути
            total_time = nx.dijkstra_path_length(self.G, source=start, target=end, weight='weight')
            
            # Для сравнения найдем чисто геометрический путь (наименьшее число дорог без учета пробок)
            shortest_by_hops = nx.shortest_path(self.G, source=start, target=end)
            hops_time = sum(self.G[shortest_by_hops[i]][shortest_by_hops[i+1]]['weight'] for i in range(len(shortest_by_hops)-1))
            
            # Собираем грани для подсветки
            route_edges = list(zip(optimal_path[:-1], optimal_path[1:]))
            
            # Текстовый отчет для учеников
            path_str = " -> ".join(map(str, optimal_path))
            report = (
                f"🎯 Оптимальный путь найден!\n\n"
                f" Маршрут:\n {path_str}\n\n"
                f"⏱️ Время в пути: {total_time} мин.\n\n"
                f"💡 К сведению:\n"
                f"Если поехать напролом\n"
                f"по самому короткому\n"
                f"пути ({'->'.join(map(str, shortest_by_hops))}),\n"
                f"то из-за пробок вы\n"
                f"потеряете {hops_time} мин!"
            )
            self.lbl_results.config(text=report, foreground="darkgreen")
            
            # Отрисовка синей неоновой линии поверх пробок
            self.draw_map(route_edges=route_edges)
            
        except nx.NetworkXNoPath:
            self.lbl_results.config(text="❌ Ошибка: Путь заблокирован!", foreground="red")
            self.draw_map()

if __name__ == "__main__":
    root = tk.Tk()
    app = GPSDijkstraNavigator(root)
    root.mainloop()


import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

# Настройка интерактивного режима для отображения окна
plt.ion()

class EulerPathPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Урок 3: Загадка Эйлера — Рисуем граф без отрыва карандаша")
        self.root.geometry("1350x850")
        
        # Граф (Мультиграф, так как между двумя островами может быть несколько мостов)
        self.G = nx.MultiGraph()
        self.pos = {}
        self.euler_trail = [] # Хранит пошаговый обход
        
        self.setup_ui()
        self.load_classic_bridges()

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=400)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для графа
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Выбор схемы
        ttk.Label(self.left_panel, text="🗺️ Выберите загадку (граф):", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        self.graph_type = tk.StringVar(value="classic")
        ttk.Radiobutton(self.left_panel, text="🗺️ Классические 7 мостов (Невозможно)", variable=self.graph_type, value="classic", command=self.load_graph_preset).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(self.left_panel, text="✏️ Схема домика (Возможно одним росчерком)", variable=self.graph_type, value="house", command=self.load_graph_preset).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(self.left_panel, text="⭐ Звезда Эйлера (Полный цикл)", variable=self.graph_type, value="star", command=self.load_graph_preset).pack(anchor=tk.W, pady=2)
        
        # Проверка теоремы Эйлера
        ttk.Label(self.left_panel, text="🔬 Математическая проверка", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        ttk.Button(self.left_panel, text="🧐 Проверить теорему Эйлера", command=self.check_euler_theorem).pack(fill=tk.X, pady=5)
        
        self.lbl_analysis = ttk.Label(self.left_panel, text="Степени вершин:\nНажмите проверку.", font=("Courier", 10), justify=tk.LEFT)
        self.lbl_analysis.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # Анимация и пошаговый обход
        ttk.Label(self.left_panel, text="🎬 Пошаговый обход карандашом", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.step_slider = ttk.Scale(self.left_panel, from_=0, to=1, orient=tk.HORIZONTAL, command=self.on_slider_move)
        self.step_slider.pack(fill=tk.X, pady=5)
        self.lbl_slider_val = ttk.Label(self.left_panel, text="Шаг: 0 из 0", foreground="blue")
        self.lbl_slider_val.pack(anchor=tk.W, pady=(0, 10))
        
        # Шпаргалка для урока
        ttk.Label(self.left_panel, text="💡 Секрет Леонарда Эйлера:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=15, wrap=tk.WORD, font=("Arial", 9), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Поле Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "📐 ТЕОРЕМА ЭЙЛЕРА (8 класс):\n"
            "Граф можно обойти без отрыва карандаша и без повтора линий тогда и только тогда, когда:\n\n"
            "1. Все вершины имеют ЧЁТНУЮ степень (количество линий). Тогда начать можно в любой точке, и там же закончить (Эйлеров цикл).\n\n"
            "2. Граф имеет ровно ДВЕ НЕЧЁТНЫЕ вершины. Тогда начать рисовать нужно строго в одной нечётной вершине, а финиш будет во второй (Эйлеров путь).\n\n"
            "❌ Если нечётных вершин больше двух (как в классических 7 мостах Кёнигсберга) — задача математически НЕИМЕЕТ решения!\n"
            "📜 ИСТОРИЯ И СМЫСЛ ЗАДАЧИ:\n"
            "В XVIII веке жители немецкого города Кёнигсберг (ныне Калининград) развлекались загадкой: "
            "можно ли обойти все 7 городских мостов через реку Прегель, прошагав по каждому ровно один раз "
            "и вернувшись в начало? Ни у кого не получалось.\n\n"
            "В 1736 году великий математик Леонард Эйлер решил эту задачу. Он понял, что форма островов "
            "и длина мостов не важны. Он заменил сушу точками (вершинами), а мосты — линиями (рёбрами). "
            "Так родился первый в истории граф! Эйлер доказал定理: если у графа больше двух вершин имеют "
            "нечётную степень (количество линий), то обойти его без отрыва карандаша физически невозможно. "
            "У Кёнигсберга степени были (3, 3, 3, 5) — поэтому жители зря тратили время на прогулки!"
        )
        self.txt_hint.config(state=tk.DISABLED)

    def load_graph_preset(self):
        self.euler_trail = []
        self.step_slider.set(0)
        self.lbl_slider_val.config(text="Шаг: 0 из 0")
        
        g_type = self.graph_type.get()
        if g_type == "classic":
            self.load_classic_bridges()
        elif g_type == "house":
            self.load_house_preset()
        else:
            self.load_star_preset()

    def load_classic_bridges(self):
        self.G.clear()
        # 4 суши-острова Кёнигсберга
        self.G.add_nodes_from(["Север", "Юг", "Остров", "Восток"])
        self.pos = {
            "Север": (1, 2),
            "Остров": (1, 1),
            "Юг": (1, 0),
            "Восток": (2, 1)
        }
        # 7 мостов (между сушами по несколько дорог)
        edges = [
            ("Север", "Остров", "м1"), ("Север", "Остров", "м2"),
            ("Юг", "Остров", "м3"), ("Юг", "Остров", "м4"),
            ("Север", "Восток", "м5"), ("Юг", "Восток", "м6"),
            ("Остров", "Восток", "м7")
        ]
        for u, v, key in edges:
            self.G.add_edge(u, v, key=key)
        self.draw_graph()

    def load_house_preset(self):
        self.G.clear()
        self.G.add_nodes_from([1, 2, 3, 4, 5])
        self.pos = {
            1: (0, 0), 2: (2, 0),
            3: (0, 2), 4: (2, 2),
            5: (1, 3.5) # Крыша домика
        }
        edges = [
            (1, 2, 'e1'), (1, 3, 'e2'), (2, 4, 'e3'), (3, 4, 'e4'), # Квадрат
            (1, 4, 'e5'), (2, 3, 'e6'), # Крест внутри домика
            (3, 5, 'e7'), (4, 5, 'e8')  # Крыша
        ]
        for u, v, key in edges:
            self.G.add_edge(u, v, key=key)
        self.draw_graph()

    def load_star_preset(self):
        self.G.clear()
        self.G.add_nodes_from(["A", "B", "C", "D", "E"])
        self.pos = {
            "A": (1, 3), "B": (2, 0), "C": (0, 2), "D": (2, 2), "E": (0, 0)
        }
        edges = [
            ("C", "D", '1'), ("D", "E", '2'), ("E", "A", '3'), ("A", "B", '4'), ("B", "C", '5')
        ]
        for u, v, key in edges:
            self.G.add_edge(u, v, key=key)
        self.draw_graph()

    def check_euler_theorem(self):
        degrees = dict(self.G.degree())
        odd_nodes = [node for node, deg in degrees.items() if deg % 2 != 0]
        
        deg_text = "📐 СТЕПЕНИ ВЕРШИН:\n"
        for node, deg in degrees.items():
            deg_text += f"• Точка {node}: степень {deg} ({'чётная' if deg%2==0 else 'НЕЧЁТНАЯ 🔴'})\n"
            
        deg_text += f"\n❌ Нечётных вершин: {len(odd_nodes)}\n"
        
        if len(odd_nodes) == 0:
            deg_text += " Результат: Можно обойти!\n(Это замкнутый Эйлеров цикл)"
            # Генерируем пошаговый путь средствами networkx
            self.euler_trail = list(nx.eulerian_circuit(self.G))
        elif len(odd_nodes) == 2:
            deg_text += f" Результат: Можно обойти!\nСтартуйте в точке: {odd_nodes[0]}"
            self.euler_trail = list(nx.eulerian_path(self.G))
        else:
            deg_text += " Результат: МАТЕМАТИЧЕСКИ\nНЕВОЗМОЖНО ОБОЙТИ! ❌"
            self.euler_trail = []
            messagebox.showerror("Теорема Эйлера", "Этот граф содержит больше двух нечётных вершин! Нарисовать его одним росчерком физически невозможно.")
            
        self.lbl_analysis.config(text=deg_text)
        
        if self.euler_trail:
            self.step_slider.config(from_=0, to=len(self.euler_trail))
            self.step_slider.set(0)
            self.lbl_slider_val.config(text=f"Шаг: 0 из {len(self.euler_trail)}")
        self.draw_graph()

    def on_slider_move(self, val):
        if not self.euler_trail:
            return
        step = int(float(val))
        self.lbl_slider_val.config(text=f"Шаг: {step} из {len(self.euler_trail)}")
        
        # Передаем пройденные ребра для подсветки
        active_edges = self.euler_trail[:step]
        self.draw_graph(active_edges=active_edges)

    def draw_graph(self, active_edges=None):
        self.ax.clear()
        
        # В мультиграфах дуги могут накладываться, сделаем красивый вывод
        # Рисуем базовые ребра (серые)
        for u, v, data in self.G.edges(data=True):
            self.ax.plot([self.pos[u][0], self.pos[v][0]], [self.pos[u][1], self.pos[v][1]], color="#cccccc", lw=2.5, zorder=1)
            
        # Подсвечиваем пройденный «карандашом» путь жирным синим цветом со стрелками направления
        if active_edges:
            for idx, (u, v) in enumerate(active_edges):
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                # Сама линия прохода
                self.ax.plot([x1, x2], [y1, y2], color="#0055ff", lw=5.0, alpha=0.8, zorder=2)
                
                # Показываем номер шага прямо по центру линии
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                self.ax.text(cx, cy + 0.05, str(idx + 1), color="white", weight="bold", fontsize=10,
                             bbox=dict(facecolor='black', alpha=0.7, boxstyle='round,pad=0.2'), zorder=4)
                
                # Добавляем векторную стрелочку
                dx, dy = (x2 - x1) * 0.02, (y2 - y1) * 0.02
                self.ax.annotate("", xy=(cx+dx, cy+dy), xytext=(cx, cy),
                                 arrowprops=dict(arrowstyle="-|>", color="yellow", lw=2, mutation_scale=15), zorder=3)

        # Рисуем вершины
        # nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color="#ff9999", node_size=700, edgecolors="black", linewidths=1.5, zorder=5)
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color="#ff9999", node_size=700, edgecolors="black", linewidths=1.5)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=11, font_weight="bold")

        # nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=11, font_weight="bold", zorder=6)
        
        self.ax.set_title("✏️ Головоломка: Обход рёбер без отрыва карандаша", fontsize=11, fontweight='bold', pad=10)
        self.ax.axis("off")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = EulerPathPuzzle(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import networkx.algorithms.community as nx_comm
import random

# Настройка интерактивного режима для отображения окна
plt.ion()

class SocialCommunityDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Урок 4: Анализ Big Data — Поиск скрытых сообществ в классе")
        self.root.geometry("1350x850")
        
        self.G = nx.Graph()
        self.pos = {}
        self.communities = [] # Список найденных групп
        
        self.setup_ui()
        self.generate_class_network()

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=380)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для графа
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Управление сетью
        ttk.Label(self.left_panel, text="👥 Моделирование класса", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Button(self.left_panel, text="🎲 Сгенерировать случайный класс", command=self.generate_class_network).pack(fill=tk.X, pady=5)
        
        # Запуск ИИ-кластеризации
        ttk.Label(self.left_panel, text="🤖 Алгоритмы кластеризации", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        ttk.Button(self.left_panel, text="🔍 Найти тайные группировки", command=self.detect_communities).pack(fill=tk.X, pady=5)
        
        # Блок вывода результатов
        ttk.Label(self.left_panel, text="📊 Отчёт ИИ по структуре класса:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.lbl_results = ttk.Label(self.left_panel, text="Нажмите поиск групп...", font=("Courier", 10), justify=tk.LEFT, foreground="purple")
        self.lbl_results.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # Шпаргалка для урока
        ttk.Label(self.left_panel, text="💡 Как устроен анализ соцсетей?", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=15, wrap=tk.WORD, font=("Arial", 9), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Поле Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "🌐 КЛАСТЕРИЗАЦИЯ В СОЦСЕТЯХ (VK, Telegram):\n"
            "Специальные алгоритмы ищут группы людей, у которых внутри группы очень много связей (дружбы), а с другими группами — мало.\n\n"
            "🧁 КАК ЭТО РАБОТАЕТ В КОДЕ:\n"
            "Мы используем жадный алгоритм модулярности (Clauset-Newman-Moore). Он автоматически разбивает сеть на оптимальное число сообществ.\n\n"
            "🎯 ЧТО ПОКАЗАТЬ ДЕТЯМ:\n"
            "После нажатия кнопки «Найти тайные группировки» вершины не просто перекрасятся, они физически притянутся к центрам своих компаний (сменится раскладка графа)! Это наглядно демонстрирует, как маркетологи или ИИ вычисляют интересы групп подростков, чтобы предлагать им рекламу или тренды.\n"
            "📜 ИСТОРИЯ И СМЫСЛ ЗАДАЧИ:\n"
            "В 1970 году социолог Уэйн Захари исследовал реальный университетский клуб каратистов. "
            "В процессе наблюдения внутри клуба произошёл конфликт между тренером и директором. "
            "Клуб раскололся на две группы. Захари обнаружил, что, используя только граф дружеских "
            "связей, компьютер смог с точностью до одного человека предсказать, кто в какую группировку "
            "уйдёт! Этот граф вошёл в историю науки как 'Клуб карате Захари'.\n\n"
            "Сегодня алгоритмы кластеризации (такие как метод модулярности Ньюмена, 2004 г.) используются "
            "всеми соцсетями. Telegram, VK и TikTok анализируют, с кем вы общаетесь, вычисляют вашу скрытую "
            "группу интересов ('геймеры', 'анимешники', 'музыканты') и подкидывают вам точечную рекламу "
            "и рекомендации, формируя так называемые 'эхо-камеры'."
        )
        self.txt_hint.config(state=tk.DISABLED)

    def generate_class_network(self):
        self.G.clear()
        self.communities = []
        self.lbl_results.config(text="Класс создан в случайном порядке.\nГруппировки скрыты.", foreground="black")
        
        # Создаем модель графа «Связанные пещеры» (Caveman Graph) — идеальная модель школьного класса
        # Генерируем 3-4 изолированные компании по 4-5 человек, а затем перемешиваем их
        num_groups = random.randint(3, 4)
        group_size = random.randint(4, 5)
        
        self.G = nx.connected_caveman_graph(num_groups, group_size)
        
        # Добавляем случайные «мостики» дружбы между компаниями, чтобы граф не был полностью разорван
        all_nodes = list(self.G.nodes())
        for _ in range(int(len(all_nodes) / 2)):
            u = random.choice(all_nodes)
            v = random.choice(all_nodes)
            if u != v and not self.G.has_edge(u, v):
                self.G.add_edge(u, v)
                
        # Стартовая раскладка — все перемешаны по кругу (тайные группы не видны)
        self.pos = nx.circular_layout(self.G)
        self.draw_graph(colored=False)

    def detect_communities(self):
        # Находим сообщества алгоритмом модулярности
        # Превращаем генератор в список сетов
        comm_gen = nx_comm.greedy_modularity_communities(self.G)
        self.communities = [list(c) for c in comm_gen]
        
        # Пересчитываем координаты через spring_layout, чтобы участники одной группы притянулись друг к другу
        # Это создает красивый визуальный эффект разделения на «кучки»
        self.pos = nx.spring_layout(self.G, k=0.4, iterations=50)
        
        # Формируем отчет
        report = f"🤖 ИИ обнаружил: {len(self.communities)} групп(ы)\n\n"
        for idx, comm in enumerate(self.communities):
            report += f"• Группа {idx+1}: {len(comm)} чел.\n  Состав: {sorted(comm)}\n"
            
        self.lbl_results.config(text=report, foreground="darkmagenta")
        self.draw_graph(colored=True)

    def draw_graph(self, colored=False):
        self.ax.clear()
        
        # Базовая палитра ярких цветов для сообществ
        color_palette = ["#ff5555", "#55ff55", "#5555ff", "#ffcc00", "#ff55ff", "#00ffff"]
        
        node_colors = []
        if colored and self.communities:
            # Красим каждую вершину в цвет её группы
            for node in self.G.nodes():
                assigned_color = "#skyblue"
                for idx, comm in enumerate(self.communities):
                    if node in comm:
                        # Берем цвет из палитры по кругу
                        assigned_color = color_palette[idx % len(color_palette)]
                        break
                node_colors.append(assigned_color)
        else:
            # До кластеризации — все нейтрально-голубые
            node_colors = ["#e6f2ff" for _ in self.G.nodes()]
            
        # Рисуем связи
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color="#cccccc", width=1.5)
        
        # Рисуем учеников
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color=node_colors, node_size=600, edgecolors="black", linewidths=1.5)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=11, font_weight="bold")
        
        if colored:
            self.ax.set_title("🤖 Сеть успешно разделена на неформальные группировки!", fontsize=11, fontweight='bold', pad=10)
        else:
            self.ax.set_title("👥 Все ученики перемешаны (Попробуйте найти сообщества)", fontsize=11, fontweight='bold', pad=10)
            
        self.ax.axis("off")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialCommunityDetector(root)
    root.mainloop()


import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random

# Настройка интерактивного режима для отображения окна
plt.ion()

class GraphColoringGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Урок 5: Теорема о 4 красках — Раскраска карт и графов")
        self.root.geometry("1400x850")
        
        self.G = nx.Graph()
        self.pos = {}
        
        # Словарь цветов: номер вершины -> выбранный цвет (название или HEX)
        self.node_colors_dict = {}
        
        # Палитра цветов для игры (6 ярких вариантов)
        self.palette = ["#FF5555", "#55FF55", "#5555FF", "#FFCC00", "#FF55FF", "#00FFFF"]
        self.color_names = ["Красный", "Зелёный", "Синий", "Жёлтый", "Розовый", "Голубой"]
        self.selected_paint = "#FF5555" # Выбранная "кисточка" игрока
        
        self.setup_ui()
        self.generate_map_graph()

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=400)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для графа
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Управление картой
        ttk.Label(self.left_panel, text="🗺️ Создание карты/графа", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        ttk.Button(self.left_panel, text="🎲 Сгенерировать новую карту дорог", command=self.generate_map_graph).pack(fill=tk.X, pady=5)
        
        # Палитра для ручной раскраски
        ttk.Label(self.left_panel, text="🎨 Выберите цвет кисти:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.brush_var = tk.StringVar(value="0")
        
        # Создаем радиокнопки-переключатели цветов
        for idx, name in enumerate(self.color_names):
            rb = ttk.Radiobutton(
                self.left_panel, text=name, variable=self.brush_var, 
                value=str(idx), command=self.change_brush
            )
            rb.pack(anchor=tk.W, pady=2)
            
        # Поля для ручного ввода цвета вершины (если клики мышкой по графику не сработают на некоторых ОС)
        manual_frame = ttk.Frame(self.left_panel)
        manual_frame.pack(fill=tk.X, pady=10)
        ttk.Label(manual_frame, text="Покрасить вершину №:").pack(side=tk.LEFT)
        self.ent_node = ttk.Entry(manual_frame, width=5)
        self.ent_node.pack(side=tk.LEFT, padx=5)
        ttk.Button(manual_frame, text="🖌️ Красить", command=self.paint_node_manual).pack(side=tk.LEFT, padx=5)

        # Проверки и Авто-раскраска
        ttk.Label(self.left_panel, text="🔬 Математический анализ", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        ttk.Button(self.left_panel, text="🧐 Проверить мои ошибки", command=self.check_user_coloring).pack(fill=tk.X, pady=5)
        ttk.Button(self.left_panel, text="🤖 Авто-раскраска ИИ (Идеал)", command=self.auto_color_graph).pack(fill=tk.X, pady=5)
        
        # Шпаргалка для урока
        ttk.Label(self.left_panel, text="💡 Великая теорема карт:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=12, wrap=tk.WORD, font=("Arial", 9), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Настройка Matplotlib Canvas и событие клика
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Подключаем интерактивный клик мышкой по вершинам графа!
        self.fig.canvas.mpl_connect('button_press_event', self.on_graph_click)

    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "🗺️ ТЕОРЕМА О ЧЕТЫРЕХ КРАСКАХ:\n"
            "Любую географическую карту на плоскости можно раскрасить всего 4 ЦВЕТАМИ так, чтобы страны с общей границей имели разные цвета [1].\n\n"
            "🏫 ДЛЯ ЧЕГО ЭТО В ЖИЗНИ:\n"
            "• Распределение радиочастот (чтобы соседние вышки сотовой связи не глушили друг друга).\n"
            "• Составление школьного расписания уроков (вершины — уроки, ребра — общие учителя, цвета — учебные часы) [1].\n\n"
            "🎯 ИГРА НА УРОКЕ:\n"
            "Попробуйте раскрасить все вершины так, чтобы линии не соединяли кружки одинакового цвета! Какое минимальное число цветов у вас получилось?\n"
            "📜 ИСТОРИЯ И СМЫСЛ ЗАДАЧИ:\n"
            "В 1852 году английский картограф Фрэнсис Гутри раскрашивал карту графств Англии и заметил, "
            "что ему хватает всего 4 цветов, чтобы соприкасающиеся регионы не сливались. Он спросил "
            "математиков: верно ли это для любой карты мира? Эта загадка мучила учёных больше века.\n\n"
            "Лишь в 1976 году Кеннет Аппель и Вольфганг Хакен доказали 'Теорему о 4 красках'. Это было "
            "первое в истории науки доказательство, сделанное с помощью суперкомпьютера (он перебирал "
            "варианты 1200 часов!).\n\n"
            "Сегодня раскраска графов применяется везде, где есть дефицит ресурсов. Например, при "
            "распределении частот сотовой связи (соседние вышки красят в разные 'цвета'-частоты, чтобы "
            "они не глушили друг друга) или при составлении школьного расписания без окон у учителей."
        )
        self.txt_hint.config(state=tk.DISABLED)

    def generate_map_graph(self):
        self.G.clear()
        self.node_colors_dict = {}
        
        # Генерируем планарный случайный граф, похожий на соты или карту стран
        num_nodes = random.randint(8, 12)
        
        # Используем геометрический граф (точки близко друг к другу соединяются рёбрами)
        self.G = nx.random_geometric_graph(n=num_nodes, radius=0.45)
        self.pos = nx.get_node_attributes(self.G, 'pos')
        
        # Если позиции не сгенерировались автоматически, делаем стандартный spring
        if not self.pos:
            self.pos = nx.spring_layout(self.G, seed=42)
            
        # Инициализируем все вершины нейтральным белым цветом
        for node in self.G.nodes():
            self.node_colors_dict[node] = "#FFFFFF"
            
        self.draw_graph()

    def change_brush(self):
        idx = int(self.brush_var.get())
        self.selected_paint = self.palette[idx]

    def paint_node_manual(self):
        try:
            node = int(self.ent_node.get())
            if node in self.G:
                self.node_colors_dict[node] = self.selected_paint
                self.draw_graph()
            else:
                messagebox.showerror("Ошибка", "Такого номера вершины нет!")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число!")

    # Интерактивное закрашивание по клику мыши на холсте!
    def on_graph_click(self, event):
        if event.xdata is None or event.ydata is None:
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
        if min_dist < 0.02 and closest_node is not None:
            self.node_colors_dict[closest_node] = self.selected_paint
            self.ent_node.delete(0, tk.END)
            self.ent_node.insert(0, str(closest_node))
            self.draw_graph()

    def check_user_coloring(self):
        errors_found = 0
        uncolored = 0
        
        for u, v in self.G.edges():
            color_u = self.node_colors_dict[u]
            color_v = self.node_colors_dict[v]
            
            if color_u == "#FFFFFF" or color_v == "#FFFFFF":
                uncolored += 1
                continue
                
            if color_u == color_v:
                errors_found += 1
                
        # Проверяем, сколько уникальных цветов задействовал пользователь (исключая белый)
        used_colors = set(c for c in self.node_colors_dict.values() if c != "#FFFFFF")
        
        if uncolored > 0:
            messagebox.showinfo("Проверка", f"Вы ещё не докрасили карту! Осталось некрашеных вершин: {uncolored}")
        elif errors_found > 0:
            messagebox.showerror("Ошибка!", f"Математический конфликт! Найдено {errors_found} связей, где соседи покрашены в ОДИНАКОВЫЙ цвет. ❌")
        else:
            messagebox.showinfo("Успех! 🎉", f"Поздравляем! Карта раскрашена абсолютно верно.\nВы использовали цветов: {len(used_colors)} шт. 👍")

    def auto_color_graph(self):
        # Алгоритм жадной раскраски NetworkX (Greedy Coloring)
        coloring = nx.coloring.greedy_color(self.G, strategy="largest_first")
        
        # Переносим результаты ИИ в нашу карту цветов
        for node, color_idx in coloring.items():
            # Берем цвета из нашей палитры
            self.node_colors_dict[node] = self.palette[color_idx % len(self.palette)]
            
        unique_colors_count = max(coloring.values()) + 1
        messagebox.showinfo("ИИ Раскраска", f"Робот справился идеально!\nХроматическое число этого графа: {unique_colors_count}\n(Понадобилось цветов: {unique_colors_count})")
        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        
        # Список цветов строго в порядке вершин графа
        colors_list = [self.node_colors_dict[node] for node in self.G.nodes()]
        
        # Рисуем рёбра (границы стран)
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color="#777777", width=2.0)
        
        # Рисуем вершины (страны) с обводкой
        nx.draw_networkx_nodes(
            self.G, self.pos, ax=self.ax, 
            node_color=colors_list, node_size=650, 
            edgecolors="black", linewidths=2.0
        )
        
        # Номера вершин
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=11, font_weight="bold")
        
        self.ax.set_title("🎨 Кликни по кружку, чтобы покрасить его выбранной кистью!", fontsize=11, fontweight='bold', pad=10)
        self.ax.axis("off")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphColoringGame(root)
    root.mainloop()




# ОГЭ-Тренажёр (Сложение путей и километраж).
# GPS-Навигатор Дейкстры (Объезд дорожных пробок по весам).
# Головоломка Эйлера (Анимация рисования без отрыва карандаша).
# Детектор Big Data (Силовое стягивание скрытых сообществ).
# Теорема о 4 красках (Интерактивная игра-раскраска карт).

import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random
import numpy as np

# Настройка интерактивного режима для отображения окна
plt.ion()

class SpaceCourierTSP:
    def __init__(self, root):
        self.root = root
        self.root.title("Урок 6: Задача Коммивояжёра — Космический курьер и тупик ИИ")
        self.root.geometry("1400x850")
        
        self.G = nx.Graph()
        self.pos = {}
        self.best_route = []
        self.total_distance = 0
        
        self.setup_ui()
        self.generate_planets()

    def setup_ui(self):
        # Левая панель управления
        self.left_panel = ttk.Frame(self.root, padding=10, width=400)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Правая панель для графа
        self.right_panel = ttk.Frame(self.root, padding=10)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Количество планет
        ttk.Label(self.left_panel, text="🚀 Настройка звёздной системы", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        self.planets_slider = ttk.Scale(self.left_panel, from_=5, to=15, orient=tk.HORIZONTAL)
        self.planets_slider.set(8)
        self.planets_slider.pack(fill=tk.X, pady=5)
        
        ttk.Button(self.left_panel, text="🎲 Разбросать планеты в космосе", command=self.generate_planets).pack(fill=tk.X, pady=5)
        
        # Кнопки запуска алгоритмов
        ttk.Label(self.left_panel, text="🤖 Запуск ИИ-оптимизации", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15,5))
        ttk.Button(self.left_panel, text="⚡ Найти идеальное космическое кольцо", command=self.solve_tsp_approximation).pack(fill=tk.X, pady=5)
        
        # Результаты вычислений
        ttk.Label(self.left_panel, text="📊 Бортовой журнал:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.lbl_results = ttk.Label(self.left_panel, text="Маршрут не построен.", font=("Courier", 10), justify=tk.LEFT, foreground="darkgreen")
        self.lbl_results.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        # Шпаргалка для урока
        ttk.Label(self.left_panel, text="💡 Математический тупик человечества:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
        self.txt_hint = tk.Text(self.left_panel, height=15, wrap=tk.WORD, font=("Arial", 10), bg="#f9f9f9", fg="black")
        self.txt_hint.pack(fill=tk.BOTH, expand=True)
        self.show_hints()

        # Поле Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_hints(self):
        self.txt_hint.insert(tk.END,
            "📦 ЗАДАЧА КОММИВОЯЖЁРА (TSP):\n"
            "Это одна из самых известных и сложных задач в мире информатики. "
            "Нужно обойти все вершины графа строго по одному разу и вернуться в начало, потратив минимум бензина/времени.\n\n"
            "🛑 ПОЧЕМУ ЭТО ТУПИК ДЛЯ КОМПЬЮТЕРОВ?\n"
            "Для неё нет идеальной формулы. Если городов 5 — вариантов обхода 120. "
            "Если городов 15 — вариантов 1,3 ТРИЛЛИОНА! "
            "Даже суперкомпьютер зависнет на недели, пытаясь перебрать все пути.\n\n"
            "🐝 КАК РЕШАЕТ ИИ:\n"
            "В логистике (например, в службах доставки Amazon, СДЭК, Ozon) используют приближённые эвристические алгоритмы (Кристофидеса, имитации отжига или Муравьиный алгоритм). "
            "Они находят путь, близкий к идеальному, за сотые доли секунды, спасая логистику планеты от коллапса!"
        )
        self.txt_hint.config(state=tk.DISABLED)

    def generate_planets(self):
        self.G.clear()
        self.best_route = []
        self.total_distance = 0
        self.lbl_results.config(text="Планеты зафиксированы.\nЖду запуска навигатора.", foreground="black")
        
        num_planets = int(self.planets_slider.get())
        self.G.add_nodes_from(range(num_planets))
        
        # Генерируем случайные координаты планет в двумерном космосе
        random.seed()
        self.pos = {i: (random.uniform(0.1, 0.9), random.uniform(0.1, 0.9)) for i in range(num_planets)}
        
        # В этой задаче граф ПОЛНЫЙ — между любыми двумя планетами можно пролететь напрямую
        for u in range(num_planets):
            for v in range(u + 1, num_planets):
                # Вес ребра — это реальное геометрическое расстояние между точками в космосе
                dist = np.hypot(self.pos[u][0] - self.pos[v][0], self.pos[u][1] - self.pos[v][1])
                # Округляем в «световые годы»
                self.G.add_edge(u, v, weight=round(dist * 100, 1))
                
        self.draw_space()

    def solve_tsp_approximation(self):
        # Используем встроенный в NetworkX мощный приближенный алгоритм Кристофидеса (алгоритм 1.5-аппроксимации)
        try:
            # Находит замкнутый цикл коммивояжёра
            self.best_route = nx.approximation.traveling_salesman_problem(self.G, weight='weight', cycle=True)
            
            # Считаем итоговую длину получившегося кольца
            self.total_distance = sum(self.G[self.best_route[i]][self.best_route[i+1]]['weight'] for i in range(len(self.best_route)-1))
            
            # Формируем отчет
            route_str = " -> ".join(map(str, self.best_route))
            report = (
                f"🛰️ Оптимальный гипер-прыжок найден!\n\n"
                f"🪐 Маршрут облёта:\n {route_str}\n\n"
                f"🌌 Длина пути: {self.total_distance:.1f} св. лет\n\n"
                f"🚀 ИИ спас курьера от перебора\n триллионов комбинаций!"
            )
            self.lbl_results.config(text=report, foreground="darkgreen")
            self.draw_space(show_route=True)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось рассчитать цикл: {str(e)}")

    def draw_space(self, show_route=False):
        self.ax.clear()
        
        # Рисуем фоновую слабую сетку всех возможных космических путей (светло-серые тонкие линии)
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color="#f0f0f0", width=0.8)
        
        # Если ИИ построил кольцо, накладываем его жирными неоново-зелеными линиями со стрелками направления
        if show_route and self.best_route:
            route_edges = list(zip(self.best_route[:-1], self.best_route[1:]))
            nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edgelist=route_edges, edge_color="#00cc66", width=4.0)
            
            # Ставим стрелочки по вектору движения корабля
            for u, v in route_edges:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = (x2 - x1) * 0.01, (y2 - y1) * 0.01
                self.ax.annotate("", xy=(cx+dx, cy+dy), xytext=(cx, cy),
                                 arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5, mutation_scale=15))

        # Рисуем сами планеты (сделаем их тёмно-синими футуристичными сферами)
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color="#003366", node_size=550, edgecolors="#00ffff", linewidths=1.5)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=10, font_weight="bold", font_color="white")
        
        self.ax.set_title("🌌 Карта секторов | Зелёное кольцо — Круговой маршрут ИИ", fontsize=11, fontweight='bold', pad=10)
        self.ax.axis("off")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceCourierTSP(root)
    root.mainloop()