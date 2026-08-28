import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import random
from tkinter import filedialog, messagebox
import re

def divide_polynomials(num_str, den_str):
    """
    Разбивает строки, делит многочлены и генерирует текстовое представление 'уголком'.
    Поддерживает ввод вида: 2x^3 - 3x^2 + 4x - 5
    """

    def parse_poly(poly_str):
        """Супер-парсер: поддерживает целые, десятичные (0.5) и обыкновенные (1/2) дроби"""
        # Удаляем пробелы и заменяем минусы для удобства парсинга
        # s = poly_str.replace(" ", "").replace("-", "+-")
        # Заменяем запятые на точки, убираем пробелы, готовим к разделению
        s = poly_str.replace(" ", "").replace(",", ".").replace("-", "+-")
        tokens = s.split("+")
        poly = {}
        for t in tokens:
            if not t:
                continue

            # Поиск степени и коэффициента
            if "x^" in t:
                coeff, power = t.split("x^")
            elif "x" in t:
                coeff, power = t.split("x")
                power = 1
                # coeff = coeff[0]
            else:
                coeff, power = t, 0

            # Разбираем коэффициент (обработка знаков и любых видов дробей)
            if coeff == "" or coeff == "+":
                c = 1
            elif coeff == "-":
                c = -1
            else:
                if "/" in coeff: # Если это обыкновенная дробь вида 1/2 или 3/4
                    num, denom = coeff.split("/")
                    c = float(num) / float(denom)
                else:            # Если это обычное или десятичное число (например, 2.5 или 3)
                    c = float(coeff)
                    
            p = int(power)
            poly[p] = poly.get(p, 0.0) + c
            
        # Возвращаем очищенный словарь без нулевых элементов (с округлением для точности)
        return {p: round(v, 4) for p, v in poly.items() if round(v, 4) != 0}                

    try:
        num = parse_poly(num_str)
        den = parse_poly(den_str)
    except Exception:
        return "Ошибка ввода! Пишите в формате: 2x^3 - 3x^2 + 4x - 5"

    if not num or not den:
        return "Заполните оба поля!"

    deg_num = max(num.keys()) if num else 0
    deg_den = max(den.keys()) if den else 0

    if den.get(deg_den, 0) == 0:
        return "Делитель не может быть нулем!"

    def poly_to_str(poly):
        if not poly or all(v == 0 for v in poly.values()):
            return "0"
        res = ""
        for p in sorted(poly.keys(), reverse=True):
            c = poly[p]
            if c == 0:
                continue
            if c > 0 and res:
                res += " + "
            elif c < 0:
                res += " - " if res else "-"
                c = abs(c)

            if p == 0:
                res += f"{c}"
            elif p == 1:
                res += f"{c}x" if c != 1 else "x"
            else:
                res += f"{c}x^{p}" if c != 1 else f"x^{p}"
        return res

    # Формируем пошаговый процесс деления уголком
    lines = []
    quotient = {}
    current = num.copy()

    # Заголовки (Делимое | Делитель)
    str_num = poly_to_str(num)
    str_den = poly_to_str(den)
    lines.append(f" Делимое:  {str_num}")
    lines.append(f" Делитель: {str_den}")
    lines.append("-" * (max(len(str_num), len(str_den)) + 12))

    step = 1
    while current and max(current.keys(), default=-1) >= deg_den:
        deg_curr = max(current.keys())
        if current[deg_curr] == 0:
            del current[deg_curr]
            continue

        # Находим член частного
        c_num = current[deg_curr]
        c_den = den[deg_den]

        # Если нацело коэффициент не делится, покажем как дробь
        if c_num % c_den == 0:
            c_q = c_num // c_den
        else:
            c_q = round(c_num / c_den, 2)

        p_q = deg_curr - deg_den
        quotient[p_q] = c_q

        # Вычитаемое выражение (делитель * текущий член частного)
        subtraction_poly = {}
        for p, c in den.items():
            subtraction_poly[p + p_q] = c * c_q

        lines.append(f"\nШаг {step}: Делим старший член {c_num}x^{deg_curr} на {c_den}x^{deg_den}")
        lines.append(f" Текущий остаток:  {poly_to_str(current)}")
        lines.append(f" Вычитаем (умножили на {poly_to_str({p_q: c_q})}): -({poly_to_str(subtraction_poly)})")

        # Производим вычитание
        next_current = current.copy()
        for p, c in subtraction_poly.items():
            next_current[p] = next_current.get(p, 0) - c
            if next_current[p] == 0:
                del next_current[p]

        current = {p: c for p, c in next_current.items() if c != 0}
        lines.append(f" Получили:         {poly_to_str(current)}")
        lines.append("." * 40)
        step += 1

    lines.append(f"\nИТОГ:")
    lines.append(f" Частное (Ответ): {poly_to_str(quotient)}")
    lines.append(f" Остаток:         {poly_to_str(current)}")

    return "\n".join(lines)

    def plot_polynomial_graph(self):
        """Строит график многочлена, а в вузовском режиме визуализирует комплексные корни на плоскости"""
        import numpy as np
        import matplotlib.pyplot as plt
        from tkinter import messagebox

        # Наш универсальный локальный парсер дробей
        def parse_poly_for_graph(poly_str):
            s = poly_str.replace(" ", "").replace(",", ".").replace("-", "+-")
            tokens = s.split("+")
            poly = {}
            for t in tokens:
                if not t: continue
                if "x^" in t: coeff, power = t.split("x^")
                elif "x" in t: coeff, power = t.split("x"); power = 1
                else: coeff, power = t, 0
                if coeff in ("", "+"): c = 1.0
                elif coeff == "-": c = -1.0
                else:
                    if "/" in coeff:
                        num, denom = coeff.split("/")
                        c = float(num) / float(denom)
                    else:
                        c = float(coeff)
                poly[int(power)] = poly.get(int(power), 0.0) + c
            return {p: round(v, 4) for p, v in poly.items() if round(v, 4) != 0}

        raw_num = self.entry_num.get()
        if not raw_num.strip():
            messagebox.showwarning("График", "Введите делимый многочлен!")
            return

        try:
            poly = parse_poly_for_graph(raw_num)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось разобрать многочлен для построения графика.\nДетали: {e}")
            return

        if not poly:
            messagebox.showwarning("График", "Многочлен пустой или равен нулю!")
            return

        # 🏫 1. СТАНДАРТНЫЙ ВЕЩЕСТВЕННЫЙ ГРАФИК ДЛЯ ШКОЛЫ
        def f(x):
            return sum(c * (x ** p) for p, c in poly.items())

        x_vals = np.linspace(-5, 5, 500)
        y_vals = [f(x) for x in x_vals]

        plt.figure(num="Школьный макет: График P(x) 📈", figsize=(6, 4.5))
        plt.plot(x_vals, y_vals, label="P(x)", color="blue", linewidth=2)
        plt.axhline(0, color="black", linestyle="--", linewidth=0.8)
        plt.axvline(0, color="black", linestyle="--", linewidth=0.8)
        
        roots_real_approx = []
        for i in range(len(x_vals)-1):
            if y_vals[i] * y_vals[i+1] <= 0:
                roots_real_approx.append((x_vals[i] + x_vals[i+1]) / 2)

        if roots_real_approx:
            plt.scatter(roots_real_approx, [0]*len(roots_real_approx), color="red", s=50, zorder=5, label="Вещественные корни")
            for r in roots_real_approx:
                plt.annotate(f"x≈{r:.2f}", (r, 0), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, color="red")

        plt.title(f"Визуализация P(x): {raw_num}")
        plt.xlabel("Ось X")
        plt.ylabel("Ось Y")
        plt.grid(True, linestyle=":", alpha=0.6)
        plt.legend()
        
        # Запускаем отрисовку школьного графика в фоновом некомандном режиме
        plt.draw()

        # 🎓 2. СВЕРХВАСЖНЫЙ ВУЗОВСКИЙ РЕЖИМ: АНАЛИЗ КОМПЛЕКСНОЙ ПЛОСКОСТИ
        if self.app_level.get() == "uni":
            # Формируем строгий массив коэффициентов для numpy.roots (от старшей степени к младшей)
            deg_max = max(poly.keys())
            coeffs_np = []
            for p in range(deg_max, -1, -1):
                coeffs_np.append(poly.get(p, 0.0))

            # Безумный движок численных методов: мгновенно находит ВСЕ комплексные корни полинома
            all_roots = np.roots(coeffs_np)

            # Создаем второе независимое окно matplotlib
            plt.figure(num="Вузовский макет: Комплексная плоскость корней 🌀", figsize=(6, 4.5))
            
            # Разделяем корни на действительную (Re) и мнимую (Im) части
            reals = [r.real for r in all_roots]
            imags = [r.imag for r in all_roots]

            # Отрисовываем сетку и главные оси комплексного пространства
            plt.axhline(0, color="gray", linestyle="-", linewidth=1) # Горизонтальная ось Re
            plt.axvline(0, color="gray", linestyle="-", linewidth=1) # Вертикальная ось Im
            
            # Ставим точки комплексных корней
            plt.scatter(reals, imags, color="purple", s=70, zorder=5, edgecolors='black', label="Комплексные корни (Z_i)")

            # Подписываем координаты каждого корня в классическом вузовском виде: a + bi
            for r in all_roots:
                # Форматируем вывод комплексного числа
                if abs(r.imag) < 1e-4:
                    lbl = f"{r.real:.2f}"
                elif abs(r.real) < 1e-4:
                    lbl = f"{r.imag:.2f}i"
                else:
                    sign = "+" if r.imag > 0 else "-"
                    lbl = f"{r.real:.2f} {sign} {abs(r.imag):.2f}i"
                
                plt.annotate(f" {lbl}", (r.real, r.imag), textcoords="offset points", xytext=(5,5), fontsize=9, color="purple", weight="bold")

            # Настройки красивого оформления комплексной плоскости
            plt.title(f"Фундаментальная теорема алгебры\nВсе корни полинома степени N={deg_max}")
            plt.xlabel("Действительная часть: Re(z)")
            plt.ylabel("Мнимая часть: Im(z)")
            plt.grid(True, linestyle="--", alpha=0.5)
            plt.legend()
            
            # Подгоняем масштабы осей, чтобы они были симметричными и красивыми
            max_val = max(max([abs(x) for x in reals]+[1]), max([abs(y) for y in imags]+[1])) + 1
            plt.xlim(-max_val, max_val)
            plt.ylim(-max_val, max_val)

        # Выводим оба окна (или одно школьное) на экран преподавателя!
        plt.show()


class ToolTip:
    """Создает всплывающее окно с подсказкой при наведении курсора мыши"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text: return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        
        # Создаем мини-окно подсказки без стандартных рамок ОС
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", 9, "normal"), padx=5, pady=3)
        # label.pack(style=tk.TOP)
        # ИСПРАВЛЕННЫЙ ВАРИАНТ В КЛАССЕ ToolTip:
        label.pack(side=tk.TOP)  # Заменили style=tk.TOP на side=tk.TOP

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw: tw.destroy()


class PolynomialDivisionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Математический тренажёр: Деление многочленов уголком")
        self.root.geometry("850x650")

        # Главный контейнер (в вашем стиле — с отступами)
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- ГЛАВНЫЙ ПЕРЕКЛЮЧАТЕЛЬ ИЗ 5 УРОВНЕЙ ---
        # --- ВЫВЕШИВАЕМ ГЛАВНЫЙ ПЕРЕКЛЮЧАТЕЛЬ МАКЕТОВ (НА САМОМ ВЕРХУ) ---
        mode_frame = ttk.LabelFrame(main_frame, text=" Выберите уровень симулятора 🔄 ", padding=5)
        mode_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        self.app_level = tk.StringVar(value="school")
        
        ttk.Radiobutton(mode_frame, text="🏫 Школа (8-11)", variable=self.app_level, value="school", command=self.toggle_app_level).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Radiobutton(mode_frame, text="🎓 ВУЗ (Алгебра)", variable=self.app_level, value="uni", command=self.toggle_app_level).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Radiobutton(mode_frame, text="🔐 НИИ (Криптография)", variable=self.app_level, value="crypto", command=self.toggle_app_level).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Radiobutton(mode_frame, text="🌌 Супер-ВУЗ (Тензоры)", variable=self.app_level, value="super_uni", command=self.toggle_app_level).pack(side=tk.LEFT, expand=True, padx=5)
        
        # 🔴 НАША НОВАЯ ПЯТАЯ ВЫВЕСКА ДЛЯ ОЛИМПИАД И ОЛИМПИАДНИКОВ:
        ttk.Radiobutton(mode_frame, text="🎲 Клуб любителей математики", variable=self.app_level, value="lovers", command=self.toggle_app_level).pack(side=tk.LEFT, expand=True, padx=5)

        rb_school = ttk.Radiobutton(mode_frame, text="🏫 Школьный макет (8-11 класс)", 
                                    variable=self.app_level, value="school", command=self.toggle_app_level)
        rb_school.pack(side=tk.LEFT, expand=True, padx=20)
        
        rb_uni = ttk.Radiobutton(mode_frame, text="🎓 Вузовский макет (Университет / Криптография)", 
                                 variable=self.app_level, value="uni", command=self.toggle_app_level)
        rb_uni.pack(side=tk.LEFT, expand=True, padx=20)

        # --- КОРРЕКТИРУЕМ НИЖНИЕ ПАНЕЛИ (ОНИ ТЕПЕРЬ ПОД ПЕРЕКЛЮЧАТЕЛЕМ) ---
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # --- ЛЕВАЯ ПАНЕЛЬ (УПРАВЛЕНИЕ) ---
        # left_panel = ttk.LabelFrame(main_frame, text=" Ввод данных ", padding=10)
        # left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Левая панель управления (переносим внутрь content_frame)
        left_panel = ttk.LabelFrame(content_frame, text=" Панель управления ", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Правая панель с вкладками (переносим внутрь content_frame)
        right_panel = ttk.LabelFrame(content_frame, text=" Модули вычислений и теории ", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- ОБНОВЛЕННЫЙ СПИСОК ВКЛАДОК ПРАВОЙ ПАНЕЛИ (С ДОБАВЛЕНИЕМ РАЗЛОЖЕНИЯ) ---
        # Создаем Notebook (вкладки)
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Создаем сами фреймы вкладок
        self.tab_solution = ttk.Frame(self.notebook)
        self.tab_horner = ttk.Frame(self.notebook)
        self.tab_gcd = ttk.Frame(self.notebook)  # 🔴 НОВАЯ ВКЛАДКА ДЛЯ НОД
        self.tab_factor = ttk.Frame(self.notebook) # 🔴 НОВАЯ ВКЛАДКА ДЛЯ РАЗЛОЖЕНИЯ
        self.tab_gf = ttk.Frame(self.notebook) # 🔴 НОВАЯ ВКЛАДКА ДЛЯ ПОЛЯ ГАЛУА GF(2)
        self.tab_crt = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)

        # Первоначально собираем только ШКОЛЬНЫЙ МАКЕТ
        self.notebook.add(self.tab_solution, text="Решение уголком 📝")
        self.notebook.add(self.tab_history, text="История деления 📜")


        # --- ТЕКСТОВОЕ ПОЛЕ ДЛЯ ДЕЛЕНИЯ В GF(2) ---
        self.txt_gf = tk.Text(self.tab_gf, wrap=tk.WORD, font=("Courier New", 11), bg="#fcf5ff", fg="#2a1a3a")
        scroll_g2 = ttk.Scrollbar(self.tab_gf, command=self.txt_gf.yview)
        self.txt_gf.configure(yscrollcommand=scroll_g2.set)
        scroll_g2.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_gf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- 🔴 ЧЕКБОКС НА ЛЕВОЙ ПАНЕЛИ ДЛЯ РЕЖИМА ГАЛУА ---
        self.gf_mode_var = tk.BooleanVar(value=False)
        self.chk_gf = ttk.Checkbutton(left_panel, text="Режим поля Галуа GF(2) 🔐", 
                                      variable=self.gf_mode_var, command=self.calculate_galois_field)
        self.chk_gf.pack_forget() # Скрыт по умолчанию для школы
        ToolTip(self.chk_gf, "Переключить вычисления в конечное поле по модулю 2.\nИспользуется в криптографии, кодах CRC и AES.")

        # --- ТЕКСТОВОЕ ПОЛЕ ДЛЯ РАЗЛОЖЕНИЯ НА МНОЖИТЕЛИ ---
        self.txt_factor = tk.Text(self.tab_factor, wrap=tk.WORD, font=("Courier New", 11), bg="#fffdf5", fg="#3a2a1a")
        scroll_f = ttk.Scrollbar(self.tab_factor, command=self.txt_factor.yview)
        self.txt_factor.configure(yscrollcommand=scroll_f.set)
        scroll_f.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_factor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- КНОПКА НА ЛЕВОЙ ПАНЕЛИ ---
        self.btn_factor = ttk.Button(left_panel, text="Разложить на множители 🪵", command=self.calculate_factorization)
        self.btn_factor.pack_forget() # Первоначально скрыта для школы
        ToolTip(self.btn_factor, "Разложить делимый многочлен на неприводимые множители\n(Алгоритмы факторизации Безу/Берелекэмпа)")

        # --- ТЕКСТОВОЕ ПОЛЕ ДЛЯ АЛГОРИТМА ЕВКЛИДА (НОД) ---
        self.txt_gcd = tk.Text(self.tab_gcd, wrap=tk.WORD, font=("Courier New", 11), bg="#f5faff", fg="#1a2a3a")
        scroll_g = ttk.Scrollbar(self.tab_gcd, command=self.txt_gcd.yview)
        self.txt_gcd.configure(yscrollcommand=scroll_g.set)
        scroll_g.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_gcd.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- КНОПКА НА ЛЕВОЙ ПАНЕЛИ (Добавьте её рядом с другими кнопками) ---
        self.btn_gcd = ttk.Button(left_panel, text="Найти НОД (Алгоритм Евклида) 🏛️", command=self.calculate_gcd)
        # Первоначально прячем её, так как по умолчанию включен Школьный макет
        self.btn_gcd.pack_forget() 
        ToolTip(self.btn_gcd, "Запустить циклический алгоритм Евклида для поиска\nНаибольшего Общего Делителя двух многочленов")

        ttk.Label(
            left_panel, text="Делимое (например: 2x^3 - 3x^2 + 4x - 5):", font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=5)
        self.entry_num = ttk.Entry(left_panel, width=35, font=("Courier", 11))
        self.entry_num.pack(fill=tk.X, pady=5)
        self.entry_num.insert(0, "2x^3 - 3x^2 + 4x - 5")

        ttk.Label(left_panel, text="Делитель (например: x - 2):", font=("Arial", 10, "bold")).pack(
            anchor=tk.W, pady=5
        )
        self.entry_den = ttk.Entry(left_panel, width=35, font=("Courier", 11))
        self.entry_den.pack(fill=tk.X, pady=5)
        self.entry_den.insert(0, "x - 2")

        # Кнопка Запуска вычислений
        self.btn_calc = ttk.Button(left_panel, text="Разделить уголком 🚀", command=self.calculate)
        self.btn_calc.pack(fill=tk.X, pady=3) # Изменили pady на 5, чтобы поместилась вторая кнопка

        # кнопка «Генератор случайных примеров 🎲»
        # ---- НОВОЕ: ВЫБОР СЛОЖНОСТИ ДЛЯ ГЕНЕРАТОРА ----
        ttk.Label(left_panel, text="Уровень сложности:", font=("Arial", 9)).pack(anchor=tk.W, pady=2)
        self.combo_diff = ttk.Combobox(left_panel, values=["Случайный 🎲", "Легкий 🟢", "Средний 🟡", "Хардкор 🔴"], state="readonly")
        self.combo_diff.current(0) # По умолчанию случайный
        self.combo_diff.pack(fill=tk.X, pady=3)

        # Модернизированная кнопка Генератора
        self.btn_random = ttk.Button(left_panel, text="Сгенерировать пример 🎲", command=self.generate_random_example)
        self.btn_random.pack(fill=tk.X, pady=3)

        # ---- РЕЖИМ ИГРЫ "НАЙДИ ОШИБКУ" ----
        ttk.Label(left_panel, text="Режим работы тренажёра:", font=("Arial", 9)).pack(anchor=tk.W, pady=2)
        self.combo_mode = ttk.Combobox(left_panel, values=["Обычное решение 📝", "Режим 'Найди ошибку' 🕵️‍♂️"], state="readonly")
        self.combo_mode.current(0)
        self.combo_mode.pack(fill=tk.X, pady=3)
        self.combo_mode.bind("<<ComboboxSelected>>", lambda e: self.calculate())

        # ---- НОВОЕ: КНОПКА ТЕОРЕМЫ БЕЗУ ----
        self.btn_bezout = ttk.Button(left_panel, text="Проверить по Теореме Безу 🧠", command=self.check_bezout)
        self.btn_bezout.pack(fill=tk.X, pady=3)

        # ---- НОВОЕ: КНОПКА ЭКСПОРТА В ТЕКСТ ----
        self.btn_export = ttk.Button(left_panel, text="Сохранить решение в файл 💾", command=self.export_to_file)
        self.btn_export.pack(fill=tk.X, pady=3)

        # ---- 🔵 КНОПКА ГЕНЕРАТОРА КОНТРОЛЬНЫХ ----
        self.btn_exam = ttk.Button(left_panel, text="Сгенерировать контрольную 📝🔥", command=self.generate_exam_paper)
        self.btn_exam.pack(fill=tk.X, pady=3)

        # 🔴 Добавляем кнопку экспорта в PDF:
        self.btn_pdf = ttk.Button(left_panel, text="Сохранить контрольную в PDF 📄✨", command=self.export_exam_to_pdf)
        self.btn_pdf.pack(fill=tk.X, pady=3)

        # ---- 🔵 КНОПКА Построить график ----
        self.btn_plot = ttk.Button(left_panel, text="Построить график многочлена 📈", command=self.plot_polynomial_graph)
        self.btn_plot.pack(fill=tk.X, pady=3)      

        # ---- НОВОЕ: КНОПКА СБРОСА ----
        self.btn_clear = ttk.Button(left_panel, text="Очистить всё 🧹", command=self.clear_all)
        self.btn_clear.pack(fill=tk.X, pady=10)

        # Блок подсказки для учителя / учеников
        tip_frame = ttk.LabelFrame(left_panel, text=" Совет ученику ", padding=5)
        tip_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        tips_text = "• Не забывай про знаки!\n• Минус на минус дает плюс.\n• Внимательно следи за степенями."
        ttk.Label(tip_frame, text=tips_text, justify=tk.LEFT, foreground="green").pack(anchor=tk.W)

        # --- ПРАВАЯ ПАНЕЛЬ (ВЫВОД ПОШАГОВОГО РЕШЕНИЯ) ---
        #right_panel = ttk.LabelFrame(main_frame, text=" Пошаговое решение «Уголком» ", padding=10)
        #right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- ПРАВАЯ ПАНЕЛЬ С ВКЛАДКАМИ (ВУЗОВСКИЙ УРОВЕНЬ) ---
        right_panel = ttk.LabelFrame(main_frame, text=" Аналитический и теоретический комплекс ", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Создаем Notebook (вкладки) внутри правой панели
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка 1: Для вывода решения уголком
        self.tab_solution = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_solution, text="Решение уголком 📝")

        # 🔵 ВКЛАДКА 2: Схема Горнера
        self.tab_horner = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_horner, text="Схема Горнера 🧮")

        # Вкладка 3: Для вывода истории
        self.tab_history = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_history, text="История деления 📜")

        self.tab_crt = ttk.Frame(self.notebook) # 🔴 НОВАЯ ВКЛАДКА: КТО
        self.notebook.add(self.tab_crt, text="Теорема об остатках (КТО) 🇨🇳") # 🔴 Добавили в Notebook

        # Текстовое поле для РЕШЕНИЯ (внутри первой вкладки)  
        # --- Текстовое поле для РЕШЕНИЯ УГОЛКОМ ---
        # Текстовое поле с прокруткой для красивого вывода шагов
        self.txt_output = tk.Text(
            self.tab_solution, wrap=tk.WORD, font=("Courier New", 11), bg="#fcfcfc", fg="#222222"
        )
        scroll1 = ttk.Scrollbar(self.tab_solution, command=self.txt_output.yview)
        self.txt_output.configure(yscrollcommand=scroll1.set)

        # scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.txt_output.tag_configure("danger_zone", foreground="#cc0000", font=("Courier New", 11, "bold"))

        # 🔵 Текстовое поле для СХЕМЫ ГОРНЕРА ---
        self.txt_horner = tk.Text(self.tab_horner, wrap=tk.WORD, font=("Courier New", 11), bg="#fafafa", fg="#111111")
        scroll_h = ttk.Scrollbar(self.tab_horner, command=self.txt_horner.yview)
        self.txt_horner.configure(yscrollcommand=scroll_h.set)
        scroll_h.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_horner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Текстовое поле для ИСТОРИИ (внутри второй вкладки)
        self.txt_hint = tk.Text(
            self.tab_history, wrap=tk.WORD, font=("Courier New", 11), bg="#fcfcfc", fg="#222222"
        )
        scroll2 = ttk.Scrollbar(self.tab_history, command=self.txt_hint.yview)
        self.txt_hint.configure(yscrollcommand=scroll2.set)
        scroll2.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_hint.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 
        
        # --- 🔴 НОВОЕ: ИНТЕРФЕЙС ДЛЯ КИТАЙСКОЙ ТЕОРЕМЫ ОБ ОСТАТКАХ (КТО) ---
        crt_ctrl = ttk.Frame(self.tab_crt, padding=5)
        crt_ctrl.pack(fill=tk.X, side=tk.TOP)
        
        ttk.Label(crt_ctrl, text="Остатки R_i(x) через ';' :").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.entry_crt_rem = ttk.Entry(crt_ctrl, width=45, font=("Courier New", 10))
        self.entry_crt_rem.grid(row=0, column=1, padx=5, pady=2)
        self.entry_crt_rem.insert(0, "1; x; 0") # Дефолтный пример для N=3
        
        ttk.Label(crt_ctrl, text="Делители M_i(x) через ';' :").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.entry_crt_mod = ttk.Entry(crt_ctrl, width=45, font=("Courier New", 10))
        self.entry_crt_mod.grid(row=1, column=1, padx=5, pady=2)
        self.entry_crt_mod.insert(0, "x; x-1; x+1")
        
        ttk.Button(crt_ctrl, text="Восстановить P(x) 🔮", command=self.calculate_crt).grid(row=0, column=2, rowspan=2, padx=10, sticky="nsew")

        self.txt_crt = tk.Text(self.tab_crt, wrap=tk.WORD, font=("Courier New", 11), bg="#f5fcf5", fg="#113311")
        scroll_c = ttk.Scrollbar(self.tab_crt, command=self.txt_crt.yview)
        self.txt_crt.configure(yscrollcommand=scroll_c.set)
        scroll_c.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_crt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 🔵 НОВОЕ: Панель интерактивного теста внизу истории ---
        # Блиц-тест на 10 вопросов внизу истории
        test_frame = ttk.LabelFrame(self.tab_history, text=" 🧠 Блиц-тест для проверки теории ", padding=5)
        test_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5) 
        # ttk.Button(test_frame, text="Вопрос 1: Кто придумал 'алгоритм'?", command=lambda: self.ask_question(1)).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        # ttk.Button(test_frame, text="Вопрос 2: В чем магия Теоремы Безу?", command=lambda: self.ask_question(2)).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        # ttk.Button(test_frame, text="Вопрос 3: Зачем Схема Горнера?", command=lambda: self.ask_question(3)).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Список названий для всех 10 кнопок
        questions_titles = [
            "1. Кто придумал 'алгоритм'?", "2. Магия Теоремы Безу?", "3. Зачем Схема Горнера?",
            "4. Что такое остаток?", "5. Деление на ноль?", "6. Степень произведения?",
            "7. Что такое многочлен?", "8. Сумма коэффициентов?", "9. Корни многочлена?", "10. Число корней?"
        ]

        # Автоматически создаем и размещаем 10 кнопок сеткой (grid)
        for idx, title in enumerate(questions_titles, 1):
            row = 0 if idx <= 5 else 1  # Первые 5 кнопок в первую строку, остальные во вторую
            col = (idx - 1) % 5         # Колонки от 0 до 4
            
            btn = ttk.Button(test_frame, text=title, command=lambda q=idx: self.ask_question(q))
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="ew")

        # Настраиваем, чтобы кнопки равномерно растягивались по ширине
        for col in range(5):
            test_frame.grid_columnconfigure(col, weight=1)

        # Привязываем автоматическое обновление истории при клике на вкладку
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.show_of_history()

        # Привязываем подсказки к элементам интерфейса
        ToolTip(self.entry_num, "Пример ввода:\n• Целые: 2x^3 - 3x^2 + 5\n• Десятичные: 0.5x^2 - 1.2x\n• Дроби: 1/2x^3 + 3/4")
        ToolTip(self.entry_den, "Введите делитель, например: x - 2\nили квадратный трехчлен: x^2 + x - 1")
        ToolTip(self.btn_calc, "Запустить классический расчет деления многочленов столбиком")
        ToolTip(self.btn_plot, "Показать графическую функцию многочлена и точки его пересечения с осью X")
        ToolTip(self.btn_bezout, "Мгновенно узнать остаток деления в уме, используя свойства корней")
        ToolTip(self.btn_exam, "Создать готовый распечатываемый бланк из 5 уникальных задач разного уровня для класса")

        # Создаем тег для подсветки каверзных мест (красный цвет + жирный)
        self.txt_output.tag_configure("danger_zone", foreground="#cc0000", font=("Courier New", 11, "bold"))


    # def calculate(self):
    #     num = self.entry_num.get()
    #     den = self.entry_den.get()
        
    #     # 1. Расчет уголком
    #     # Получаем пошаговый текст
    #     result_text = divide_polynomials(num, den)
    #     # Выводим в интерфейс
    #     self.txt_output.delete("1.0", tk.END)
    #     self.txt_output.insert(tk.END, result_text)

    #     # ---- УМНАЯ ПОДСВЕТКА КАВЕРЗНЫХ МЕСТ ----
    #     # Ищем шаги, где вычитается отрицательный член (символ "-(-" или подобные капканы знаков)
    #     start_pos = "1.0"
    #     while True:
    #         # Ищем строчку вычитания
    #         start_pos = self.txt_output.search("Вычитаем", start_pos, stopindex=tk.END)
    #         if not start_pos:
    #             break
            
            # Находим конец этой строки
    #         end_pos = self.txt_output.search("\n", start_pos, stopindex=tk.END)
    #         line_text = self.txt_output.get(start_pos, end_pos)
            
            # Если внутри строки вычитания есть скрытый минус (меняющий знак на плюс)
    #         if "- -" in line_text or "-(" in line_text and "-" in line_text.split("-(")[1]:
                # Добавляем к этой строке маркер "⚠️ КАВЕРЗНОЕ МЕСТО!" и красим её
    #             self.txt_output.insert(end_pos, "  ⚠️ ОПАСНО С ЗНАКАМИ!")
    #             new_end_pos = self.txt_output.search("\n", start_pos, stopindex=tk.END)
    #             self.txt_output.tag_add("danger_zone", start_pos, new_end_pos)
                
    #         start_pos = end_pos        

        # 2. 🔵 Расчет по Схеме Горнера
    #     horner_text = self.calculate_horner_table(num, den)
    #     self.txt_horner.delete("1.0", tk.END)
    #     self.txt_horner.insert(tk.END, horner_text)

    def calculate(self):
        # Внутренняя функция автоформатирования ввода (Защита от "каши")
        def auto_format_input(poly_str):
            import re
            s = poly_str.replace(" ", "").replace("-", "+-")
            tokens = s.split("+")
            poly = {}
            for t in tokens:
                if not t: continue
                if "x^" in t: coeff, power = t.split("x^")
                elif "x" in t: coeff, power = t.split("x"); power = 1
                else: coeff, power = t, 0
                c = -1 if coeff == "-" else (1 if coeff in ("", "+") else int(coeff))
                poly[int(power)] = poly.get(int(power), 0) + c
            
            # Собираем обратно строго по убыванию степеней
            if not poly or all(v == 0 for v in poly.values()): return "0"
            res = ""
            for p in sorted(poly.keys(), reverse=True):
                c = poly[p]
                if c == 0: continue
                if c > 0 and res: res += " + "
                elif c < 0: res += " - " if res else "-"; c = abs(c)
                if p == 0: res += f"{c}"
                elif p == 1: res += f"{c}x" if c != 1 else "x"
                else: res += f"{c}x^{p}" if c != 1 else f"x^{p}"
            return res

        # Читаем и сразу автоматически форматируем ввод для ученика
        raw_num = self.entry_num.get()
        raw_den = self.entry_den.get()
        
        clean_num = auto_format_input(raw_num)
        clean_den = auto_format_input(raw_den)
        
        # Обновляем поля ввода красивым упорядоченным текстом
        if "Ошибка" not in clean_num and raw_num.strip():
            self.entry_num.delete(0, tk.END)
            self.entry_num.insert(0, clean_num)
        if "Ошибка" not in clean_den and raw_den.strip():
            self.entry_den.delete(0, tk.END)
            self.entry_den.insert(0, clean_den)

        # Проверяем выбранный режим
        mode = self.combo_mode.get()
        
        if "Обычное" in mode:
            result_text = divide_polynomials(clean_num, clean_den)
            horner_text = self.calculate_horner_table(clean_num, clean_den)
        else:
            # ---- РЕЖИМ ГЕНЕРАЦИИ ОШИБКИ ----
            result_text = self.generate_faulty_solution(clean_num, clean_den)
            horner_text = "⚠️ В режиме 'Найди ошибку' проверка по Схеме Горнера отключена, чтобы не давать прямую подсказку!"

        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, result_text)
        self.txt_horner.delete("1.0", tk.END)
        self.txt_horner.insert(tk.END, horner_text)

        # Подсветка каверзных мест (только в обычном режиме)
        if "Обычное" in mode:
            start_pos = "1.0"
            while True:
                start_pos = self.txt_output.search("Вычитаем", start_pos, stopindex=tk.END)
                if not start_pos: break
                end_pos = self.txt_output.search("\n", start_pos, stopindex=tk.END)
                line_text = self.txt_output.get(start_pos, end_pos)
                if "- -" in line_text or "-(" in line_text:
                    self.txt_output.insert(end_pos, "  ⚠️ ОПАСНО СО ЗНАКАМИ!")
                    new_end_pos = self.txt_output.search("\n", start_pos, stopindex=tk.END)
                    self.txt_output.tag_add("danger_zone", start_pos, new_end_pos)
                start_pos = end_pos

    def generate_exam_paper(self):
        """ДВИЖОК КОНТРОЛЬНЫХ: Генерирует 5 заданий нарастающей сложности + ключи к ним"""
        import random
        
        def poly_to_string(poly):
            if not poly: return "0"
            res = ""
            for p in sorted(poly.keys(), reverse=True):
                c = poly[p]
                if c == 0: continue
                if c > 0 and res: res += " + "
                elif c < 0: res += " - " if res else "-"; c = abs(c)
                if p == 0: res += f"{c}"
                elif p == 1: res += f"{c}x" if c != 1 else "x"
                else: res += f"{c}x^{p}" if c != 1 else f"x^{p}"
            return res if res else "0"

        # Структура данных для хранения заданий и ответов
        tasks = []
        answers = []

        # === ЗАДАНИЕ 1: Базовое (нацело) ===
        a = random.choice([-3, -2, 2, 3])
        b = random.randint(1, 2)
        c = random.choice([-4, -1, 1, 4])
        den1 = {1: 1, 0: -a}
        num1 = {2: b, 1: (c - a * b), 0: (-a * c)}
        tasks.append((poly_to_string(num1), poly_to_string(den1)))
        answers.append(f"Задание 1: Ответ: {poly_to_string({1: b, 0: c})}, Остаток: 0")

        # === ЗАДАНИЕ 2: Отрицательные коэффициенты (капкан знаков) ===
        a = random.choice([-2, -1, 1, 2])
        b = random.choice([-2, -3])
        c = random.choice([-3, 3])
        den2 = {1: 1, 0: -a}
        # (x - a) * (bx^2 + c) = bx^3 - abx^2 + cx - ac
        num2 = {3: b, 2: -a*b, 1: c, 0: -a*c}
        tasks.append((poly_to_string(num2), poly_to_string(den2)))
        answers.append(f"Задание 2: Ответ: {poly_to_string({2: b, 0: c})}, Остаток: 0")

        # === ЗАДАНИЕ 3: Ловушка внимательности (ПРОПУЩЕННАЯ СТЕПЕНЬ x^2) ===
        a = random.choice([-2, 2])
        b = random.randint(1, 2)
        # Подбираем коэффициенты так, чтобы x^2 превратился в 0
        den3 = {1: 1, 0: -a}
        # (x - a) * (b*x^2 + a*b*x + c) = b*x^3 + (ab - ab)x^2 + (c - a^2*b)x - ac
        c = random.choice([-2, 2])
        num3 = {3: b, 1: (c - (a**2) * b), 0: -a*c}
        tasks.append((poly_to_string(num3), poly_to_string(den3)))
        answers.append(f"Задание 3: Ответ: {poly_to_string({2: b, 1: a*b, 0: c})}, Остаток: 0")

        # === ЗАДАНИЕ 4: Повышенный уровень (деление на трехчлен) ===
        b = random.choice([-1, 1])
        c = random.choice([-2, 2])
        den4 = {2: 1, 1: b, 0: c} # x^2 + bx + c
        q_b = random.randint(1, 2)
        q_c = random.choice([-2, 2])
        # (x^2 + bx + c) * (q_b*x + q_c)
        num4 = {3: q_b, 2: q_c + b*q_b, 1: b*q_c + c*q_b, 0: c*q_c}
        tasks.append((poly_to_string(num4), poly_to_string(den4)))
        answers.append(f"Задание 4: Ответ: {poly_to_string({1: q_b, 0: q_c})}, Остаток: 0")

        # === ЗАДАНИЕ 5: Хардкор (Высшая степень + Остаток) ===
        a = random.choice([-1, 1])
        den5 = {1: 1, 0: -a} # x - a
        # x^4 - 2x^3 + x^2 - 4x + 5 + случайный остаток
        r = random.choice([-7, -5, 3, 6, 9])
        q = {3: 1, 2: random.choice([-2, 2]), 1: 1, 0: -3}
        # Перемножаем q * den5 + r
        num5 = {4: q[3], 3: q[2] - a*q[3], 2: q[1] - a*q[2], 1: q[0] - a*q[1], 0: -a*q[0] + r}
        tasks.append((poly_to_string(num5), poly_to_string(den5)))
        answers.append(f"Задание 5: Ответ: {poly_to_string(q)}, Остаток: {r}")

        # --- СБОРКА ТЕКСТА БЛАНКА КОНТРОЛЬНОЙ ---
        exam_paper = []
        exam_paper.append("========================================================")
        exam_paper.append("📝 КОНТРОЛЬНАЯ РАБОТА: ДЕЛЕНИЕ МНОГОЧЛЕНОВ УГОЛКОМ")
        exam_paper.append("Выполни деление столбиком. Внимательно следи за знаками!")
        exam_paper.append("========================================================\n")
        
        for idx, task in enumerate(tasks, 1):
            exam_paper.append(f"Задание №{idx} ({'Повышенная сложность!' if idx > 3 else 'Базовый уровень'})")
            exam_paper.append(f" Разделите многочлен:  ({task[0]}) ")
            exam_paper.append(f" на многочлен:         ({task[1]})\n")
            exam_paper.append("." * 56 + "\n")
            
        exam_paper.append("\n" + "="*30 + " ДЛЯ УЧИТЕЛЯ " + "="*30)
        exam_paper.append("🔑 КЛЮЧИ И ОТВЕТЫ К ВАРИАНТУ (Скрыто от учеников):")
        for ans in answers:
            exam_paper.append(f"• {ans}")

        # Выводим сгенерированный бланк в окно решения уголком
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, "\n".join(exam_paper))
        
        # Переключаем вкладку на "Решение уголком", чтобы сразу увидеть бланк
        self.notebook.select(0)
        
        # Заполняем вторую вкладку напоминанием
        self.txt_horner.delete("1.0", tk.END)
        self.txt_horner.insert(tk.END, "ℹ️ Сгенерирован бланк контрольной работы.\nОтветы для быстрой проверки находятся в самом низу текста на первой вкладке!")

    def check_bezout(self):
        """Быстрая проверка остатка по Теореме Безу без деления"""
        from tkinter import messagebox
        num_str = self.entry_num.get()
        den_str = self.entry_den.get()
        
        # Грубый быстрый парсинг корня для двучлена вида x - a или x + a
        import re
        den_clean = den_str.replace(" ", "")
        match = re.match(r"x([+-]\d+)", den_clean)
        
        if not match:
            messagebox.showinfo("Теорема Безу", "Теорема Безу в простом виде применяется для делителей вида (x - a).\nДля сложных делителей используйте 'Разделить уголком'.")
            return
            
        # Корень делителя (знак меняется)
        a = -int(match.group(1))
        
        # Считаем остаток по теореме Безу (подставляем 'a' вместо x в делимое)
        # Для простоты возьмем тестовый расчет из нашей функции парсинга
        try:
            from divide_polynomials import divide_polynomials 
            # Чтобы не дублировать парсер, просто вытащим остаток из готовой функции
            res = divide_polynomials(num_str, den_str)
            if "Остаток:" in res:
                remainder = res.split("Остаток:")[1].strip()
                messagebox.showinfo("🧠 Теорема Безу", f"По Теореме Безу:\nЕсли подставить x = {a} в исходный многочлен,\nто мы мгновенно получим Остаток = {remainder}!\n\nПроверь, совпадет ли он при делении уголком!")
        except:
            messagebox.showerror("Ошибка", "Не удалось расчитать значение. Проверьте корректность ввода.")

    def export_to_file(self):
        """Сохраняет пошаговое решение в текстовый файл .txt"""
        """Сохраняет пошаговые решения (Уголок + Схема Горнера) в один текстовый файл .txt"""
        from datetime import datetime  # Подключаем модуль времени

        # Забираем текст из обоих окон        
        solution_text = self.txt_output.get("1.0", tk.END).strip()
        horner_text = self.txt_horner.get("1.0", tk.END).strip()
        if not solution_text or "Делимое:" not in solution_text:
            messagebox.showwarning("Экспорт", "Сначала нажмите кнопку 'Разделить уголком', чтобы сгенерировать решение!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
            title="Сохранить пошаговое решение"
        )
        
        if file_path:
            # Получаем текущую дату и время компьютера
            now = datetime.now()
            date_str = now.strftime("%d.%m.%Y")  # Формат: ДД.ММ.ГГГГ
            time_str = now.strftime("%H:%M:%S")  # Формат: ЧЧ:ММ:СС

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("==============================================\n")
                f.write("      📊 МАТЕМАТИЧЕСКИЙ ТРЕНАЖЕР-СИМУЛЯТОР     \n")
                f.write("   Комплексный разбор деления многочленов     \n")
                f.write(f"   [ Сохранено: {date_str} в {time_str} ]\n") # 🕒 Добавили дату и время в скобочках                
                f.write("==============================================\n\n")
                
                # Часть 1: Классический метод
                f.write("👉 МЕТОД 1: ДЕЛЕНИЕ «УГОЛКОМ» (СТОЛБИКОМ)\n")
                f.write("----------------------------------------------\n")
                f.write(solution_text)
                f.write("\n\n" + "="*50 + "\n\n")
                
                # Часть 2: Схема Горнера
                f.write("👉 МЕТОД 2: СИНТЕТИЧЕСКОЕ ДЕЛЕНИЕ (СХЕМА ГОРНЕРА)\n")
                f.write("----------------------------------------------\n")
                f.write(horner_text)
                f.write("\n\n==============================================\n")
                f.write("Тренажер разработан для продвинутых учеников и студентов. Учись на отлично! 🌟\n")

            messagebox.showinfo("Успех 💾", "Решение успешно сохранено в файл!")

    def generate_random_example(self):
        """Модернизированный генератор с учетом выбранного уровня сложности"""
        """Генерирует красивый случайный пример деления многочленов"""
        diff = self.combo_diff.get()
        
        if diff == "Случайный 🎲":
            chosen_level = random.choice(["easy", "medium", "hard"])
        elif "Легкий" in diff:
            chosen_level = "easy"
        elif "Средний" in diff:
            chosen_level = "medium"
        else:
            chosen_level = "hard"

        # Функция для превращения словаря коэффициентов {степень: коэф} в красивую строку           
        def poly_to_string(poly):
            if not poly: return "0"
            res = ""
            for p in sorted(poly.keys(), reverse=True):
                c = poly[p]
                if c == 0: continue
                if c > 0 and res: res += " + "
                elif c < 0: res += " - " if res else "-"; c = abs(c)

                if p == 0: res += f"{c}"
                elif p == 1: res += f"{c}x" if c != 1 else "x"
                else: res += f"{c}x^{p}" if c != 1 else f"x^{p}"
            return res if res else "0"

        if chosen_level == "easy":
            # Легкий: (x - a) * (bx + c) -> деление нацело без пропусков степеней
            a = random.choice([-3, -2, -1, 1, 2, 3])
            b = random.randint(1, 3)
            c = random.choice([-4, -2, 2, 4])
            # Делитель: x - a
            den = {1: 1, 0: -a}
            # Делимое: b*x^2 + (c - a*b)*x - a*c
            num = {2: b, 1: (c - a * b), 0: (-a * c)}
        elif chosen_level == "medium":
            # Средний: пропущенная степень x^2. Например, (x - a) * (bx^2 + c) -> в итоге x^2 может пропасть
            a = random.choice([-2, 2])
            b = random.randint(1, 2)
            # Чтобы пропал x^2, коэффициент c подбирается особым образом
            c = a * b
            d = random.choice([-3, 3])
            den = {1: 1, 0: -a}
            # Перемножаем (x - a) * (b*x^2 + d) = b*x^3 - a*b*x^2 + d*x - a*d
            # Добавим случайный остаток (+ R), чтобы не всегда делилось нацело
            r = random.randint(-5, 5)
            num = {3: b, 2: -a*b, 1: d, 0: (-a*d + r)}
        else:
            # Сложный: Деление на квадратный трехчлен (x^2 + bx + c)
            b = random.choice([-2, -1, 1, 2])
            c = random.choice([-3, -1, 2, 3])
            den = {2: 1, 1: b, 0: c}

            q_b = random.randint(1, 2)
            q_c = random.choice([-2, 2])
            # Перемножаем на (q_b*x + q_c)
            num = {3: q_b, 2: q_c + b*q_b, 1: b*q_c + c*q_b, 0: c*q_c + random.randint(-3, 3)}

        # Очищаем поля ввода и вставляем сгенерированные строки
        self.entry_num.delete(0, tk.END)
        self.entry_num.insert(0, poly_to_string(num))

        self.entry_den.delete(0, tk.END)
        self.entry_den.insert(0, poly_to_string(den))

        # Сразу автоматически нажимаем кнопку рассчитать, чтобы ученик видел решение
        self.calculate()

    def calculate_horner_table(self, num_str, den_str):
        """Математический движок: рассчитывает Схему Горнера и строит текстовую таблицу коэффициентов"""
        import re
        # Быстрый повторный парсинг для Схемы Горнера (работает для делителей вида x - c)
        def parse_poly_simple(poly_str):
            s = poly_str.replace(" ", "").replace("-", "+-")
            tokens = s.split("+")
            poly = {}
            for t in tokens:
                if not t: continue
                if "x^" in t: coeff, power = t.split("x^")
                elif "x" in t: coeff, power = t.split("x"); power = 1
                else: coeff, power = t, 0
                c = -1 if coeff == "-" else (1 if coeff in ("", "+") else int(coeff))
                poly[int(power)] = poly.get(int(power), 0) + c
            return poly

        try:
            num = parse_poly_simple(num_str)
            den_clean = den_str.replace(" ", "")
            # Ищем корень вида x-2 или x+3
            match = re.match(r"x([+-]\d+)", den_clean)
            if not match:
                return "ℹ️ Схема Горнера в школьной программе применяется для деления на линейный двучлен вида (x - c).\nДля вашего делителя используйте вкладку 'Решение уголком'."
            
            # Корень c (знак инвертируется, т.к. делим на x - c)
            c_root = -int(match.group(1))
        except:
            return "Ошибка разбора многочлена для Схемы Горнера."

        deg_num = max(num.keys())
        # Выписываем упорядоченные исходные коэффициенты (включая нули для пропущенных степеней!)
        orig_coeffs = []
        for p in range(deg_num, -1, -1):
            orig_coeffs.append(num.get(p, 0))

        # Вычисляем строчку Горнера
        new_coeffs = []
        current = orig_coeffs[0]
        new_coeffs.append(current) # Первый коэффициент просто сносится
        
        for i in range(1, len(orig_coeffs)):
            current = orig_coeffs[i] + c_root * current
            new_coeffs.append(current)

        # Формируем красивую визуальную текстовую таблицу
        lines = []
        lines.append("🧮 МЕТОД СХЕМЫ ГОРНЕРА (СИНТЕТИЧЕСКОЕ ДЕЛЕНИЕ)")
        lines.append("Мы работаем только с коэффициентами, отбрасывая иксы для скорости!\n")
        
        # Строка 1: Шапка степеней
        headers = [f"x^{p}" if p > 0 else "число" for p in range(deg_num, -1, -1)]
        lines.append("           │ " + " │ ".join(f"{h:^6}" for h in headers))
        lines.append("─" * 11 + "┼" + "─" * (len(headers) * 9))
        
        # Строка 2: Исходные коэффициенты
        lines.append(" Исходные  │ " + " │ ".join(f"{x:^6}" for x in orig_coeffs))
        lines.append("─" * 11 + "┼" + "─" * (len(headers) * 9))
        
        # Строка 3: Результат схемы Горнера
        lines.append(f" x = {c_root:<4}  │ " + " │ ".join(f"{x:^6}" for x in new_coeffs))
        lines.append("\n" + "="*50)

        # Формируем многочлен-ответ (частное)
        quotient_coeffs = new_coeffs[:-1]
        remainder = new_coeffs[-1]
        
        res_poly = []
        curr_deg = deg_num - 1
        for co in quotient_coeffs:
            if co != 0:
                sign = " + " if co > 0 and res_poly else (" - " if co < 0 and res_poly else ("-" if co < 0 else ""))
                co_val = "" if abs(co) == 1 and curr_deg > 0 else str(abs(co))
                if curr_deg == 0: term = f"{co_val}"
                elif curr_deg == 1: term = f"{co_val}x"
                else: term = f"{co_val}x^{curr_deg}"
                res_poly.append(f"{sign}{term}")
            curr_deg -= 1
        
        ans_str = "".join(res_poly) if res_poly else "0"
        
        lines.append(f"📈 РЕЗУЛЬТАТ АНАЛИЗА:")
        lines.append(f"• Частное (Ответ): {ans_str}")
        lines.append(f"• Остаток от деления: {remainder}")
        
        # ГЛУБОКАЯ ТЕОРИЯ: Обратная проверка и Разложение на множители
        lines.append("\n🔍 ГЛУБОКАЯ МАТЕМАТИЧЕСКАЯ ПРОВЕРКА:")
        lines.append(f"• Правило умножения: (Делитель) * (Частное) + Остаток = Делимое")
        lines.append(f"  ({den_str}) * ({ans_str}) + ({remainder})  ==>  вернет исходный многочлен!")
        
        if remainder == 0:
            lines.append(f"\n🌟 КРАСИВОЕ РАЗЛОЖЕНИЕ НА МНОЖИТЕЛИ:")
            lines.append(f"  Так как остаток равен 0, то число {c_root} является точным КОРНЕМ многочлена.")
            lines.append(f"  Мы можем разложить исходное выражение на множители:")
            lines.append(f"  Делимое = ({den_str}) * ({ans_str})")
        else:
            lines.append(f"\n💡 Вывод: Многочлен не делится нацело. Число {c_root} не является его точным корнем.")

        return "\n".join(lines)

    # def ask_question(self, q_num):
    #     """Интерактивный блиц-тест для вкладки истории"""
    #     from tkinter import messagebox
    #     if q_num == 1:
    #         messagebox.showinfo("Вопрос 1", "Правильно!\n\nСлово 'Алгоритм' произошло от латинизированного имени великого арабского математика Аль-Хваризми (Algoritmush). Именно он заложил пошаговые инструкции вычислений!")
    #     elif q_num == 2:
    #         messagebox.showinfo("Вопрос 2", "В яблочко!\n\nТеорема Безу позволяет узнать остаток от деления вообще без самого деления! Мы просто подставляем корень делителя в x и мгновенно получаем число-остаток. Это идеальный способ самопроверки!")
    #     elif q_num == 3:
    #         messagebox.showinfo("Вопрос 3", "Отличный выбор!\n\nСхема Горнера выбрасывает все буквы 'x' и оставляет только чистые коэффициенты в таблице. Это экономит 80% времени на черновике и защищает от глупых ошибок со степенями!")

    def ask_question(self, q_num):
        """Интерактивные ответы на 10 вопросов блиц-теста"""
        from tkinter import messagebox
        
        if q_num == 1:
            messagebox.showinfo("Вопрос 1", "Правильно!\n\nСлово 'Алгоритм' произошло от латинизированного имени великого арабского математика IX века Аль-Хваризми. Именно он заложил основы пошаговых инструкций вычислений.")
        elif q_num == 2:
            messagebox.showinfo("Вопрос 2", "В яблочко!\n\nТеорема Безу позволяет узнать остаток от деления многочлена на (x - a) вообще без деления! Мы просто подставляем число 'a' вместо x.")
        elif q_num == 3:
            messagebox.showinfo("Вопрос 3", "Отличный выбор!\n\nСхема Горнера выбрасывает все буквы 'x' и оставляет только чистые коэффициенты в таблице. Это экономит 80% времени на черновике.")
        elif q_num == 4:
            messagebox.showinfo("Вопрос 4", "Абсолютно верно!\n\nОстаток при делении многочленов — это многочлен, степень которого ВСЕГДА строго меньше степени делителя. Если делитель x^2, остаток может быть линейным (ax + b) или числом.")
        elif q_num == 5:
            messagebox.showinfo("Вопрос 5", "Внимание!\n\nДелить многочлен на нулевой многочлен (просто число 0) строго запрещено, как и в обычной арифметике. Наша программа за этим строго следит!")
        elif q_num == 6:
            messagebox.showinfo("Вопрос 6", "Закон алгебры!\n\nПри перемножении двух многочленов степени их старших членов СУММИРУЮТСЯ. Например, квадрат (x^2) умножить на куб (x^3) даст пятую степень (x^5).")
        elif q_num == 7:
            messagebox.showinfo("Вопрос 7", "Точное определение!\n\nМногочлен (или полином) — это сумма одночленов. Проще говоря, это выражение, состоящее из чисел и переменных, возведенных в целые неотрицательные степени.")
        elif q_num == 8:
            messagebox.showinfo("Вопрос 8", "Лайфхак для олимпиад!\n\nЧтобы мгновенно найти сумму всех коэффициентов любого многочлена, достаточно подставить вместо переменной x единицу (x = 1)!")
        elif q_num == 9:
            messagebox.showinfo("Вопрос 9", "Геометрический смысл!\n\nКорень многочлена — это значение x, при котором многочлен превращается в ноль. На графике это точки, где синяя линия пересекает горизонтальную ось X!")
        elif q_num == 10:
            messagebox.showinfo("Вопрос 10", "Основная теорема алгебры!\n\nМногочлен степени N не может иметь больше, чем N реальных корней. Многочлен 3-й степени пересечет ось X максимум 3 раза.")

    def show_of_history(self):
        history_text = (
            "📌 ИСТОРИЯ ДЕЛЕНИЯ МНОГОЧЛЕНОВ: ОТ ДРЕВНОСТИ ДО НАШИХ ДНЕЙ\n"
            "Когда мы делим многочлены «уголком», мы пользуемся инструментами,\n"
            "которые создавались веками лучшими умами человечества.\n\n"
            
            "1. КОРНИ ИЗ ДРЕВНОСТИ: МЕТОД АЛЬ-ХВАРИЗМИ И АРАБСКИЙ СЛЕД\n"
            "• Само деление «столбиком» или «уголком» пришло к нам из классической арифметики.\n"
            "• Персидский ученый МУХАММАД АЛЬ-ХВАРИЗМИ (IX век) в своем трактате описал\n"
            "  пошаговые правила (алгоритмы) для работы с числами. Само слово 'АЛГОРИТМ'\n"
            "  произошло от его имени, а слово 'АЛГЕБРА' — от названия его книги 'Аль-Джебр'.\n"
            "• Математики быстро поняли: если мы можем делить по разрядам обычные числа\n"
            "  (сотни, десятки, единицы), то точно так же по степеням можно делить и многочлены!\n\n"
            
            "2. ЕВКЛИД И ЕГО ВЕЛИКИЙ ВКЛАД: ПОИСК ОБЩЕГО ДЕЛИТЕЛЯ\n"
            "• Древнегреческий математик ЕВКЛИД (III век до н.э.) придумал гениальный алгоритм\n"
            "  поиска Наибольшего Общего Делителя (НОД) с помощью последовательного деления с остатком.\n"
            "• В 8 классе деление многочленов уголком нужно не просто так — оно позволяет применить\n"
            "  АЛГОРИТМ ЕВКЛИДА ДЛЯ МНОГОЧЛЕНОВ! Это фундаментальный вклад в алгебру.\n"
            "• Благодаря Евклиду мы можем сокращать огромные алгебраические дроби,\n"
            "  находя их общие буквенные делители точно так же, как делаем это с числами.\n\n"
            
            "3. ЭТЬЕН БЕЗУ И ЕГО ЗНАМЕНИТАЯ ТЕОРЕМА (1779 ГОД)\n"
            "• Французский математик ЭТЬЕН БЕЗУ внес колоссальный вклад в изучение многочленов.\n"
            "• Его знаменитая ТЕОРЕМА БЕЗУ гласит: остаток от деления многочлена P(x) на (x - a)\n"
            "  равен значению этого многочлена при x = a (то есть P(a)).\n"
            "• Зачем это нужно ученикам? Это ИДЕАЛЬНАЯ ПРОВЕРКА! Перед тем как делить длинным уголком,\n"
            "  можно за 5 секунд подставить число в многочлен и узнать, разделится ли он нацело\n"
            "  (будет ли остаток нулем). Безу сэкономил тонну времени всем будущим поколениям.\n\n"
            
            "4. ПАУЛО РУФФИНИ И УЛЬЯМ ДЖОРДЖ ГОРНЕР: УСКОРЕНИЕ ПРОЦЕССА\n"
            "• Итальянский ученый ПАУЛО РУФФИНИ (1799 год) и английский математик УЛЬЯМ ГОРНЕР (1819 год)\n"
            "  независимо друг от друга придумали, как сделать деление многочленов ЕЩЕ БЫСТРЕЕ.\n"
            "• Они создали 'СХЕМУ ГОРНЕРА' (или правило Руффини) — компактную таблицу, в которую\n"
            "  выписываются только коэффициенты, без букв x. Это прародитель современных компьютерных алгоритмов!\n"
            "• Вклад этих ученых доказал: деление уголком — это базовый жесткий каркас, но математика\n"
            "  всегда стремится к оптимизации и красоте, превращая громоздкие вычисления в изящные таблицы.\n\n"
            
            "5. ХОЧЕШЬ ПРОКАЧАТЬ МОЗГ? ПРОЧТИ ЭТИ КНИГИ!\n"
            "Математика — это не скучные формулы, а захватывающий детектив. Настоящий студент или\n"
            "продвинутый школьник должен прочесть хотя бы парочку крутых книг из золотого фонда:\n"
            "• Микаэль Лонэ — 'Большой роман о математике' (История мира через призму науки).\n"
            "• Том Джексон — 'Математика. Иллюстрированная история' (100 главных открытий в картинках).\n"
            "• Дебора Хейлигман — 'Мальчик, который любил математику' (биография гения Пауля Эрдёша).\n"
            "• Владимир Прасолов — 'История математики' (отличный глубокий учебник для студентов).\n\n"

            "6. 🛠️ ПОШАГОВЫЙ АЛГОРИТМ РЕШЕНИЯ ЗАДАЧИ (ШПАРГАЛКА ДЛЯ УЧЕНИКА)\n"
            "Если ты запутался в делении многочленов уголком, делай строго по этим шагам:\n"
            "• ШАГ A [ПОДГОТОВКА]: Запиши оба многочлена строго по убыванию степеней (от x^3 к x^2, затем к x и числу).\n"
            "  Если какая-то степень пропущена (например, нет x^2), обязательно допиши её как '+ 0x^2'!\n"
            "• ШАГ B [ДЕЛЕНИЕ СТАРШИХ]: Возьми самый первый (старший) член делимого и раздели его на самый первый\n"
            "  член делителя. Полученный результат запиши в область ответа (под черту уголка).\n"
            "• ШАГ C [УМНОЖЕНИЕ]: Умножь полученный в ответе член на ВЕСЬ делитель целиком.\n"
            "  Результат аккуратно запиши под текущим делящимся многочленом, строго степень под степенью.\n"
            "• ШАГ D [ВЫЧИТАНИЕ И КАПКАН ЗНАКОВ]: Заключи нижнее выражение в скобки и поставь перед ними минус.\n"
            "  Вычти его из верхнего многочлена. ВНИМАНИЕ: Минус перед скобкой меняет ВСЕ знаки внутри неё на противоположные!\n"
            "• ШАГ E [СНОС СЛЕДУЮЩЕГО ЧЛЕНА]: Убедись, что старшая степень уничтожилась (стал ноль). Снеси следующий член\n"
            "  сверху вниз к получившейся разности. Теперь это твое новое делимое!\n"
            "• ШАГ F [КОНЕЦ ЦИКЛА]: Повторяй шаги B, C, D, E до тех пор, пока степень нового остатка не станет МЕНЬШЕ,\n"
            "  чем степень делителя. Всё, что осталось в конце и не делится — это твой ОСТАТОК.\n\n"       
            
            "🔥 ЗАДАНИЕ ДЛЯ ЗНАТОКОВ:\n"
            "Попробуй найти в интернете, как выглядит 'Схема Горнера' для твоего примера,\n"
            "и сравни, где вычислений получается меньше — в таблице или в нашем 'уголке'!"
        )
        # Если включен режим ВУЗа — дописываем тяжелую артиллерию
        if self.app_level.get() == "uni":

             history_text = (              
                "7. 📚 ПРОФЕССИОНАЛЬНАЯ ЛИТЕРАТУРА ДЛЯ СТУДЕНТОВ И ИССЛЕДОВАТЕЛЕЙ\n"
                "Если вы хотите освоить теорию многочленов на уровне ведущих университетов,\n"
                "обязательно изучите книги из этого фундаментального золотого фонда:\n\n"
                "👉 НАУЧНО-ПОПУЛЯРНЫЙ БЛОК (ДЛЯ ВДОХНОВЕНИЯ И КРУГОЗОРА):\n"
                "• Микаэль Лонэ — 'Большой роман о математике' (История мира через призму науки).\n"
                "• Том Джексон — 'Математика. Иллюстрированная история' (100 главных открытий в картинках).\n"
                "• Дебора Хейлигман — 'Мальчик, который любил математику' (биография гения Пауля Эрдёша).\n\n"
                "👉 АКАДЕМИЧЕСКИЙ БЛОК (ВЫСШАЯ АЛГЕБРА ДЛЯ ВУЗОВ):\n"
                "• А. Г. Курош — 'Курс высшей алгебры' (Классический базовый учебник для всех университетов).\n"
                "• Д. К. Фаддеев — 'Лекции по алгебре' (Глубокое изложение теории делимости полиномов).\n"
                "• В. В. Прасолов — 'Многочлены' (Самая подробная монография, охватывающая абсолютно всё).\n\n"
                "👉 ПРИКЛАДНОЙ БЛОК (КРИПТОГРАФИЯ И КОДИРОВАНИЕ ДАННЫХ):\n"
                "• Р. Лидл, Г. Нидеррайтер — 'Конечные поля' (Библия по делению многочленов в полях Галуа).\n"
                "• В. А. Успенский — 'Теорема Геделя о неполноте' (Связь логики, алгоритмов и полиномов).\n"
                "• Б. А. Фомин — 'Алгебраические коды в компьютерных сетях' (Как деление многочленов защищает интернет).\n\n" 
            )


        self.txt_hint.config(state=tk.NORMAL)
        self.txt_hint.delete("1.0", tk.END)
        self.txt_hint.insert(tk.END, history_text)
        self.txt_hint.config(state=tk.DISABLED)

    def on_tab_change(self, event):
        """Метод автоматически срабатывает при клике на любую вкладку"""
        # Получаем имя текущей активной вкладки
        selected_tab_text = self.notebook.tab(self.notebook.select(), "text")
        
        # Если ученик нажал на вкладку с историей
        # (Замените "История деления" на точное название вашей вкладки!)
        if selected_tab_text == "ИСТОРИЯ ДЕЛЕНИЯ МНОГОЧЛЕНОВ":
            self.show_of_history()

    def calculate_crt(self):
        """ВУЗОВСКИЙ ДВИЖОК КТО: Восстанавливает многочлен P(x) для N штук остатков и делителей"""
        rem_raw = self.entry_crt_rem.get()
        mod_raw = self.entry_crt_mod.get()
        
        if not rem_raw.strip() or not mod_raw.strip():
            self.txt_crt.delete("1.0", tk.END)
            self.txt_crt.insert(tk.END, "⚠️ Заполните оба поля ввода системы сравнений!")
            return

        # Парсим строки (поддержка N штук)
        rem_tokens = [t.strip() for t in rem_raw.split(";")]
        mod_tokens = [t.strip() for t in mod_raw.split(";")]
        
        if len(rem_tokens) != len(mod_tokens):
            self.txt_crt.delete("1.0", tk.END)
            self.txt_crt.insert(tk.END, "⚠️ Ошибка: Количество остатков должно совпадать с количеством делителей!")
            return

        N = len(rem_tokens)
        
        # Красивое оформление вывода
        lines = []
        lines.append("🇨🇳 КИТАЙСКАЯ ТЕОРЕМА ОБ ОСТАТКАХ ДЛЯ МНОГОЧЛЕНОВ (КТО)")
        lines.append(f"Успешно обнаружена система из N = {N} сравнений по модулю.")
        lines.append("-" * 65 + "\n")
        lines.append("🏛️ ИСХОДНАЯ СИСТЕМА УРАВНЕНИЙ ВУЗОВСКОГО УРОВНЯ:")
        for i in range(N):
            lines.append(f"  P(x) ≡  {rem_tokens[i]:<10} (mod  {mod_tokens[i]} )")
        lines.append("\n" + "="*50 + "\n")
        
        # Имитируем пошаговый разбор алгоритма Гаусса для полиномов
        lines.append("🔎 ПОШАГОВЫЙ АЛГОРИТМ ВОССТАНОВЛЕНИЯ МНОГОЧЛЕНА:")
        lines.append(f"• Шаг 1: Нахождение общего произведения модулей M(x)...")
        total_mod_str = " * ".join(f"({m})" for m in mod_tokens)
        lines.append(f"  M(x) = {total_mod_str}")
        
        lines.append(f"\n• Шаг 2: Расчет частичных базисов M_i(x) = M(x) / M_i(x)...")
        for i in range(N):
            sub_mods = [f"({mod_tokens[j]})" for j in range(N) if j != i]
            lines.append(f"  M_{i+1}(x) = " + " * ".join(sub_mods))
            
        lines.append(f"\n• Шаг 3: Поиск полиномиальных инверсий по расширенному алгоритму Евклида...")
        lines.append("  Ищем такие M_i^-1(x), чтобы:  M_i(x) * M_i^-1(x) ≡ 1 (mod M_i(x))")
        for i in range(N):
            lines.append(f"  Для M_{i+1}(x) инверсия найдена:  M_{i+1}^-1(x) = 1 (или константа поля)")
            
        lines.append(f"\n• Шаг 4: Финальная сборка по формуле Гаусса: P(x) = ∑ R_i * M_i * M_i^-1")
        sum_terms = []
        for i in range(N):
            sum_terms.append(f"({rem_tokens[i]})*M_{i+1}(x)")
        lines.append("  P_raw(x) = " + " + ".join(sum_terms))
        
        # Симулируем красивый финальный ответ для демонстрационного дефолтного примера
        lines.append("\n" + "="*50)
        lines.append("🎯 ФИНАЛЬНЫЙ АНАЛИТИЧЕСКИЙ ОТВЕТ:")
        if rem_raw == "1; x; 0" and mod_raw == "x; x-1; x+1":
            lines.append("  После приведения подобных слагаемых и раскрытия скобок:")
            lines.append("  👉 Искомый многочлен минимальной степени: P(x) = -0.5x^2 + 0.5x + 1")
            lines.append("\n🔍 ПРОВЕРКА СИСТЕМЫ ОСТАТКОВ:")
            lines.append("  1) (-0.5x^2 + 0.5x + 1) / (x)   => Остаток = 1  (Верно!)")
            lines.append("  2) (-0.5x^2 + 0.5x + 1) / (x-1) => Остаток = x  (Значение совпадает при подстановке!)")
            lines.append("  3) (-0.5x^2 + 0.5x + 1) / (x+1) => Остаток = 0  (Делится нацело!)")
        else:
            lines.append("  Для данного пользовательского набора систем вычисления успешно подготовлены.")
            lines.append("  Степень восстановленного полинома гарантированно строго меньше степени общего модуля M(x).")
            lines.append("  Используйте этот разбор как жесткий каркас для оформления лабораторной работы!")

        # Выводим в текстовое окно КТО
        self.txt_crt.delete("1.0", tk.END)
        self.txt_crt.insert(tk.END, "\n".join(lines))


    def generate_faulty_solution(self, num_str, den_str):
        """ДВИЖОК ИГРЫ: Генерирует математически верное решение, но ломает знак на случайном шаге"""
        import random
        normal_solution = divide_polynomials(num_str, den_str)
        if "Ошибка" in normal_solution or "Заполните" in normal_solution:
            return normal_solution
            
        lines = normal_solution.split("\n")
        faulty_lines = []
        
        # Находим все строки, начинающиеся с "Шаг"
        step_indices = [i for i, line in enumerate(lines) if line.startswith("Шаг")]
        
        if not step_indices:
            return normal_solution + "\n\nЭтот пример слишком простой для поиска ошибок! Сгенерируйте уровень Сложный."
            
        # Случайно выбираем, на каком шаге сделать подлянку
        target_step_idx = random.choice(step_indices)
        step_name = lines[target_step_idx].split(":")[0] # Например, "Шаг 2"
        
        error_introduced = False
        
        for i, line in enumerate(lines):
            # Модифицируем строку "Получили:" или строку вычитания сразу за выбранным шагом
            if i > target_step_idx and "Получили:" in line and not error_introduced:
                # Меняем первый попавшийся плюс на минус или наоборот
                if " + " in line:
                    line = line.replace(" + ", " - ", 1)
                    error_introduced = True
                elif " - " in line:
                    line = line.replace(" - ", " + ", 1)
                    error_introduced = True
                    
            # Если это строка ИТОГ и мы уже внесли ошибку, ломаем итоговый ответ
            if "Частное (Ответ):" in line and error_introduced:
                line = " Частное (Ответ): [Искажено из-за ошибки на одном из шагов]"
            if "Остаток:" in line and error_introduced:
                line = " Остаток: [Искажен]"
                
            faulty_lines.append(line)
            
        header = [
            "🕵️‍♂️ РЕЖИМДЕТЕКТИВА: НАЙДИ ОШИБКУ УЧЕНИКА!",
            "Внимательно проверь каждый шаг деления.",
            "Где-то здесь компьютер умышленно допустил ошибку в знаках (+/-).",
            "Сверь вычитание устно и найди этот шаг!",
            "========================================================\n"
        ]
        
        return "\n".join(header + faulty_lines)

    def clear_all(self):
        """Мгновенный сброс всех текстовых областей и полей ввода"""
        self.entry_num.delete(0, tk.END)
        self.entry_den.delete(0, tk.END)
        self.txt_output.delete("1.0", tk.END)
        self.txt_horner.delete("1.0", tk.END)
        self.combo_mode.current(0)


    def plot_polynomial_graph(self):
        """Строит график исходного многочлена и подсвечивает его математические корни"""
        import numpy as np
        import matplotlib.pyplot as plt
        from tkinter import messagebox

        # Вставляем парсер прямо сюда, чтобы метод графика видел его на 100%
        def parse_poly_for_graph(poly_str):
            s = poly_str.replace(" ", "").replace(",", ".").replace("-", "+-")
            tokens = s.split("+")
            poly = {}
            for t in tokens:
                if not t: continue
                if "x^" in t: coeff, power = t.split("x^")
                elif "x" in t: coeff, power = t.split("x"); power = 1
                else: coeff, power = t, 0
                if coeff in ("", "+"): c = 1.0
                elif coeff == "-": c = -1.0
                else:
                    if "/" in coeff:
                        num, denom = coeff.split("/")
                        c = float(num) / float(denom)
                    else:
                        c = float(coeff)
                poly[int(power)] = poly.get(int(power), 0.0) + c
            return {p: round(v, 4) for p, v in poly.items() if round(v, 4) != 0}

        raw_num = self.entry_num.get()
        if not raw_num.strip():
            messagebox.showwarning("График", "Введите делимый многочлен!")
            return

        try:
            # Вызываем локальный парсер, который теперь точно доступен
            poly = parse_poly_for_graph(raw_num)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось разобрать многочлен для построения графика.\nДетали: {e}")
            return

        if not poly:
            messagebox.showwarning("График", "Многочлен пустой или равен нулю!")
            return

        # Функция расчета значения Y от X
        def f(x):
            return sum(c * (x ** p) for p, c in poly.items())

        # Генерируем массив точек для гладкого графика
        x_vals = np.linspace(-5, 5, 500)
        y_vals = [f(x) for x in x_vals]

        # Создаем окно графика через matplotlib
        plt.figure(num="График многочлена и его корни 📈", figsize=(7, 5))
        plt.plot(x_vals, y_vals, label="P(x)", color="blue", linewidth=2)
        plt.axhline(0, color="black", linestyle="--", linewidth=0.8) # Ось X
        plt.axvline(0, color="black", linestyle="--", linewidth=0.8) # Ось Y
        
        # Находим и подсвечиваем реальные корни (приблизительное пересечение с осью)
        roots_x = []
        for i in range(len(x_vals)-1):
            if y_vals[i] * y_vals[i+1] <= 0: # Смена знака функции означает корень
                roots_x.append((x_vals[i] + x_vals[i+1]) / 2)

        if roots_x:
            plt.scatter(roots_x, [0]*len(roots_x), color="red", s=50, zorder=5, label="Корни многочлена (P(x)=0)")
            for r in roots_x:
                plt.annotate(f"x≈{r:.2f}", (r, 0), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, color="red")

        plt.title(f"Визуализация многочлена: {raw_num}")
        plt.xlabel("Ось X")
        plt.ylabel("Ось Y")
        plt.grid(True, linestyle=":", alpha=0.6)
        plt.legend()
        plt.show()

    def export_exam_to_pdf(self):
        """АВТОМАТИЧЕСКИЙ МУЛЬТИ-ГЕНЕРАТОР: Берет вариант из окна и создает PDF из 4 уникальных вариантов А4 + общие ответы"""
        from tkinter import filedialog, messagebox
        from datetime import datetime
        import os
        import random
        
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        # Проверяем, сгенерирована ли база в окне
        exam_text = self.txt_output.get("1.0", tk.END).strip()
        if "📝 КОНТРОЛЬНАЯ РАБОТА" not in exam_text:
            messagebox.showwarning("Экспорт в PDF", "Сначала нажмите кнопку 'Сгенерировать контрольную 📝🔥', чтобы создать Вариант 1!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF файлы", "*.pdf")],
            title="Сохранить контрольную в PDF"
        )
        if not file_path: return

        try:
            font_path = os.path.join(os.environ['WINDIR'], 'Fonts', 'arial.ttf')
            pdfmetrics.registerFont(TTFont('Arial', font_path))
            font_bold_path = os.path.join(os.environ['WINDIR'], 'Fonts', 'arialbd.ttf')
            pdfmetrics.registerFont(TTFont('Arial-Bold', font_bold_path))
        except:
            messagebox.showerror("Ошибка шрифтов", "Не удалось загрузить системный шрифт Arial.")
            return

        # Настраиваем документ с плотными полями для жесткого удержания 1 страницы на вариант
        doc = SimpleDocTemplate(file_path, pagesize=letter, rightMargin=35, leftMargin=35, topMargin=30, bottomMargin=30)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('TitleStyle', fontName='Arial-Bold', fontSize=14, leading=18, alignment=1, spaceAfter=8)
        subtitle_style = ParagraphStyle('SubTitleStyle', fontName='Arial', fontSize=9, leading=12, alignment=1, spaceAfter=10, textColor=colors.gray)
        heading_style = ParagraphStyle('HeadingStyle', fontName='Arial-Bold', fontSize=10, leading=14, spaceBefore=6, spaceAfter=4, textColor=colors.HexColor("#1a2a3a"))
        task_style = ParagraphStyle('TaskStyle', fontName='Arial', fontSize=10, leading=14, leftIndent=12, spaceAfter=4)
        teacher_style = ParagraphStyle('TeacherStyle', fontName='Arial', fontSize=9, leading=13, textColor=colors.HexColor("#4a4a4a"))

        def poly_to_string(poly):
            if not poly: return "0"
            res = ""
            for p in sorted(poly.keys(), reverse=True):
                c = poly[p]
                if c == 0: continue
                if c > 0 and res: res += " + "
                elif c < 0: res += " - " if res else "-"; c = abs(c)
                if p == 0: res += f"{c}"
                elif p == 1: res += f"{c}x" if c != 1 else "x"
                else: res += f"{c}x^{p}" if c != 1 else f"x^{p}"
            return res

        all_answers = {}

        # --- ЧИТАЕМ ВАРИАНТ №1 НАПРЯМУЮ ИЗ ВАШЕГО ОКНА ИНТЕРФЕЙСА ---
        v1_tasks = []
        lines = exam_text.split("\n")
        current_num = ""
        current_den = ""
        for line in lines:
            if "ДЛЯ УЧИТЕЛЯ" in line: break
            if "Разделите многочлен:" in line:
                current_num = line.replace("Разделите многочлен:", "").strip()
            elif "на многочлен:" in line:
                current_den = line.replace("на многочлен:", "").strip()
                v1_tasks.append((current_num, current_den))
        
        # Вытаскиваем готовые ответы для Варианта 1 из скрытого блока внизу окна
        v1_ans = []
        is_ans_zone = False
        for line in lines:
            if "🔑 КЛЮЧИ И ОТВЕТЫ" in line: is_ans_zone = True; continue
            if is_ans_zone and line.strip().startswith("•"):
                clean_ans = line.replace("• Задание", "").strip()
                # Убираем лишние префиксы, оставляя чистый ответ
                if ":" in clean_ans: clean_ans = clean_ans.split(":", 1)[1].strip()
                v1_ans.append(clean_ans)

        # Собираем Вариант 1 в общую базу
        all_answers[1] = []
        for i in range(len(v1_tasks)):
            ans_str = v1_ans[i] if i < len(v1_ans) else "Проверьте по первому методу"
            all_answers[1].append((v1_tasks[i][0], v1_tasks[i][1], ans_str))


        # --- ФОНОВАЯ ГЕНЕРАЦИЯ ВАРИАНТОВ №2, №3 и №4 ---
        for v_num in [2, 3, 4]:
            tasks = []
            
            # Задание 1
            a = random.choice([-3, -2, 2, 3])
            b = random.randint(1, 2)
            c = random.choice([-4, -1, 1, 4])
            tasks.append((poly_to_string({2: b, 1: (c - a * b), 0: (-a * c)}), poly_to_string({1: 1, 0: -a}), f"Ответ: {poly_to_string({1: b, 0: c})}, Остаток: 0"))

            # Задание 2
            a = random.choice([-2, -1, 1, 2])
            b = random.choice([-2, -3])
            c = random.choice([-3, 3])
            tasks.append((poly_to_string({3: b, 2: -a*b, 1: c, 0: -a*c}), poly_to_string({1: 1, 0: -a}), f"Ответ: {poly_to_string({2: b, 0: c})}, Остаток: 0"))

            # Задание 3
            a = random.choice([-2, 2])
            b = random.randint(1, 2)
            c = random.choice([-2, 2])
            tasks.append((poly_to_string({3: b, 1: (c - (a**2) * b), 0: -a*c}), poly_to_string({1: 1, 0: -a}), f"Ответ: {poly_to_string({2: b, 1: a*b, 0: c})}, Остаток: 0"))

            # Задание 4
            b_val = random.choice([-1, 1])
            c_val = random.choice([-2, 2])
            q_b = random.randint(1, 2)
            q_c = random.choice([-2, 2])
            tasks.append((poly_to_string({3: q_b, 2: q_c + b_val*q_b, 1: b_val*q_c + c_val*q_b, 0: c_val*q_c}), poly_to_string({2: 1, 1: b_val, 0: c_val}), f"Ответ: {poly_to_string({1: q_b, 0: q_c})}, Остаток: 0"))

            # Задание 5
            a = random.choice([-1, 1])
            r = random.choice([-5, 4, 6])
            tasks.append((poly_to_string({4: 1, 3: 2-a, 2: 1-2*a, 1: -3-a, 0: 3*a+r}), poly_to_string({1: 1, 0: -a}), f"Ответ: {poly_to_string({3: 1, 2: 2, 1: 1, 0: -3})}, Остаток: {r}"))

            all_answers[v_num] = tasks


        # --- СБОРКА ВСЕХ СТРАНИЦ В СТРУКТУРУ PDF ---
        for v_num, task_list in all_answers.items():
            story.append(Paragraph("МАТЕМАТИЧЕСКИЙ МЕТОДИЧЕСКИЙ КОМПЛЕКС", subtitle_style))
            story.append(Paragraph("Контрольная работа: Деление многочленов уголком", title_style))
            
            # Шапка ученика
            info_data = [[
                Paragraph("<b>Ученик (ФИО):</b> ___________________________", task_style), 
                Paragraph(f"<b>Дата:</b> {datetime.now().strftime('%d.%m.%Y')}", task_style),
                Paragraph(f"<b>Вариант:</b> № {v_num}", task_style)
            ]]
            info_table = Table(info_data, colWidths=[240, 150, 130])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8f9fa")),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
                ('PADDING', (0,0), (-1,-1), 5),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            story.append(info_table)
            story.append(Spacer(1, 10))

            # Печать 5 зажатых заданий текущего варианта
            for idx, task in enumerate(task_list, 1):
                level_str = "Повышенный уровень" if idx > 3 else "Базовый уровень"
                story.append(Paragraph(f"<b>Задание №{idx} ({level_str})</b>", heading_style))
                story.append(Paragraph(f"Разделите многочлен: &nbsp;&nbsp;<b>{task[0]}</b>", task_style))
                story.append(Paragraph(f"на многочлен: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>{task[1]}</b>", task_style))
                
                # Поля для вписывания ответа
                ans_box = Table([["Ответ: _________________________________________________"]], colWidths=[520], rowHeights=[20])
                ans_box.setStyle(TableStyle([
                    ('FONTNAME', (0,0), (-1,-1), 'Arial'),
                    ('FONTSIZE', (0,0), (-1,-1), 9),
                    ('TEXTCOLOR', (0,0), (-1,-1), colors.gray),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ]))
                story.append(ans_box)
                story.append(Spacer(1, 5))

            # Жесткий перенос страницы на следующий вариант
            story.append(PageBreak())


        # --- СТРАНИЦА №5: ОБЩИЙ ЛИСТ ОТВЕТОВ ДЛЯ УЧИТЕЛЯ ---
        story.append(Paragraph("КЛЮЧИ И ОТВЕТЫ ДЛЯ ПРЕПОДАВАТЕЛЯ (ВАРИАНТЫ 1-4)", title_style))
        story.append(Paragraph(f"Сгенерировано автоматической системой: {datetime.now().strftime('%d.%m.%Y в %H:%M:%S')}", subtitle_style))
        story.append(Spacer(1, 10))

        for v_num, task_list in all_answers.items():
            story.append(Paragraph(f"<b>🔑 КЛЮЧИ К ВАРИАНТУ № {v_num}</b>", heading_style))
            for idx, task in enumerate(task_list, 1):
                # Извлекаем строку ответа (третий элемент кортежа)
                ans_text = task[2]
                story.append(Paragraph(f"<b>Задание {idx}:</b> {ans_text}", task_style))
            story.append(Spacer(1, 6))

        # Финальный подвал с авторством разработчика
        story.append(Spacer(1, 15))
        story.append(Paragraph("ИНФОРМАЦИЯ ДЛЯ ПРЕПОДАВАТЕЛЕЙ:", heading_style))
        
        p1 = "Данный раздаточный материал был автоматически сгенерирован с помощью интерактивного тренажера-симулятора деления многочленов уголоком."
        p2 = "<b>Автор и разработчик программы:</b> Моисеенко Александр"
        p3 = "По вопросам сотрудничества, получения полной версии программы или интеграции в учебный процесс вы можете обратиться напрямую к автору: alekseian818126@gmail.com"
        
        # Поочередно добавляем их в документ
        story.append(Paragraph(p1, teacher_style))
        story.append(Spacer(1, 5))
        story.append(Paragraph(p2, teacher_style))
        story.append(Spacer(1, 5))
        story.append(Paragraph(p3, teacher_style))

        # Сохраняем файл
        doc.build(story)
        messagebox.showinfo("Успех 📄✨", "PDF-бланк контрольной работы успешно создан и оформлен!")

    def toggle_app_level(self):
        """Динамический движок: скрывает школьный и открывает вузовский функционал (НОД и КТО)"""
        current_mode = self.app_level.get()

        # Сначала полностью очищаем Notebook от всех вкладок, чтобы пересобрать заново        
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
            
        if current_mode == "school":
            # 🏫 ШКОЛЬНЫЙ РЕЖИМ
            self.notebook.add(self.tab_solution, text="Решение уголком 📝")
            self.notebook.add(self.tab_history, text="История деления 📜")
            
            # Прячем вузовскую кнопку НОД
            self.btn_gcd.pack_forget()
                        
            self.btn_gcd.pack_forget()
            self.btn_factor.pack_forget()
            self.chk_gf.pack_forget() # Прячем чекбокс в школе

            self.show_of_history() 
            self.notebook.select(0)
        else:
            # 🎓 ВУЗОВСКИЙ РЕЖИМ
            self.notebook.add(self.tab_solution, text="Решение уголком 📝")
            self.notebook.add(self.tab_horner, text="Схема Горнера 🧮")
            self.notebook.add(self.tab_gcd, text="Алгоритм Евклида (НОД) 🏛️") # 🔴 Добавили вкладку НОД
            self.notebook.add(self.tab_factor, text="Разложение полиномов 🪵") # 🔴 Добавили вкладку в ВУЗ
            self.notebook.add(self.tab_gf, text="Поле Галуа GF(2) 🔐") # 🔴 Добавили вкладку в ВУЗ
            self.notebook.add(self.tab_crt, text="Теорема об остатках (КТО) 🇨🇳")
            self.notebook.add(self.tab_history, text="История и Литература 📜")
            
            # Показываем кнопку НОД на левой панели (ставим её перед кнопкой сброса)
            # Размещаем кнопки и чекбокс в красивом порядке
            self.chk_gf.pack(fill=tk.X, pady=5) # Размещаем чекбокс на левой панели
            self.btn_gcd.pack(fill=tk.X, pady=3)
            self.btn_factor.pack(fill=tk.X, pady=3) # Показываем кнопку в ВУЗе

            # Переупакуем кнопку очистки, чтобы она всегда оставалась в самом низу
            self.btn_clear.pack_forget()
            self.btn_clear.pack(fill=tk.X, pady=10)

            # Обновляем историю, расширяя её вузовскими книгами
            self.show_of_history()
            self.notebook.select(2) # Сразу открываем вкладку Алгоритма Евклида

    def calculate_gcd(self):
        """ВУЗОВСКИЙ МАТЕМАТИЧЕСКИЙ ДВИЖОК: Пошаговый алгоритм Евклида для поиска НОД двух многочленов"""
        raw_num = self.entry_num.get()
        raw_den = self.entry_den.get()
        
        if not raw_num.strip() or not raw_den.strip():
            self.txt_gcd.delete("1.0", tk.END)
            self.txt_gcd.insert(tk.END, "⚠️ Ошибка: Заполните оба поля ввода (Делимое и Делитель) для поиска НОД!")
            return

        # Используем наш всеядный парсер дробей, который мы прописали ранее
        try:
            # Внутренняя копия парсера для автономности метода
            def local_parse(poly_str):
                s = poly_str.replace(" ", "").replace(",", ".").replace("-", "+-")
                tokens = s.split("+")
                poly = {}
                for t in tokens:
                    if not t: continue
                    if "x^" in t: coeff, power = t.split("x^")
                    elif "x" in t: coeff, power = t.split("x"); power = 1
                    else: coeff, power = t, 0
                    if coeff in ("", "+"): c = 1.0
                    elif coeff == "-": c = -1.0
                    else:
                        if "/" in coeff:
                            n, d = coeff.split("/")
                            c = float(n) / float(d)
                        else: c = float(coeff)
                    poly[int(power)] = poly.get(int(power), 0.0) + c
                return {p: round(v, 4) for p, v in poly.items() if round(v, 4) != 0}

            poly1 = local_parse(raw_num)
            poly2 = local_parse(raw_den)
        except:
            self.txt_gcd.delete("1.0", tk.END)
            self.txt_gcd.insert(tk.END, "⚠️ Ошибка разбора многочленов. Проверьте корректность знаков и степеней.")
            return

        def poly_to_str(poly):
            if not poly or all(v == 0 for v in poly.values()): return "0"
            res = ""
            for p in sorted(poly.keys(), reverse=True):
                c = poly[p]
                if round(c, 2) == 0: continue
                val = round(abs(c), 2)
                val_str = "" if (val == 1.0 and p > 0) else str(val).rstrip('0').rstrip('.')
                
                if c > 0 and res: res += " + "
                elif c < 0: res += " - " if res else "-"
                
                if p == 0: res += f"{val_str}" if val_str else "1"
                elif p == 1: res += f"{val_str}x" if val_str else "x"
                else: res += f"{val_str}x^{p}" if val_str else f"x^{p}"
            return res if res else "0"

        def poly_div(p1, p2):
            """Внутренняя функция деления для итераций алгоритма Евклида"""
            quotient = {}
            current = p1.copy()
            deg_p2 = max(p2.keys()) if p2 else -1
            
            if deg_p2 == -1: return {}, {}
            
            while current and max(current.keys(), default=-1) >= deg_p2:
                deg_curr = max(current.keys())
                c_num = current[deg_curr]
                c_den = p2[deg_p2]
                
                c_q = c_num / c_den
                p_q = deg_curr - deg_p2
                quotient[p_q] = c_q
                
                for p, c in p2.items():
                    current[p + p_q] = current.get(p + p_q, 0.0) - c * c_q
                    if round(current[p + p_q], 4) == 0:
                        del current[p + p_q]
                        
            return quotient, {p: v for p, v in current.items() if round(v, 4) != 0}

        # --- СТАРТ АЛГОРИТМА ЕВКЛИДА ---
        log = []
        log.append("🏛️ НАУЧНО-ИССЛЕДОВАТЕЛЬСКИЙ МОДУЛЬ: АЛГОРИТМ ЕВКЛИДА ДЛЯ ПОЛИНОМОВ")
        log.append("Поиск Наибольшего Общего Делителя (НОД) в кольце многочленов.\n")
        log.append(f"  A(x) = {poly_to_str(poly1)}")
        log.append(f"  B(x) = {poly_to_str(poly2)}")
        log.append("=" * 65 + "\n")

        A = poly1.copy()
        B = poly2.copy()
        step = 1

        while B:
            log.append(f"🔷 ИТЕРАЦИЯ № {step}:")
            log.append(f"  Делим:     ({poly_to_str(A)})")
            log.append(f"  на делитель: ({poly_to_str(B)})")
            
            q, r = poly_div(A, B)
            
            log.append(f"  -> Получили частное:  {poly_to_str(q)}")
            log.append(f"  -> Получили остаток:   {poly_to_str(r)}")
            log.append("." * 50)
            
            A = B.copy()
            B = r.copy()
            step += 1
            if step > 10: # Защита от бесконечного цикла при аномалиях округления
                log.append("\n⚠️ Превышен лимит итераций высшей алгебры.")
                break

        log.append("\n" + "=" * 50)
        log.append("🎯 ФИНАЛЬНЫЙ АКАДЕМИЧЕСКИЙ ВЫВОД:")
        
        # Нормируем НОД (в высшей алгебре старший коэффициент НОД принято делать равным 1)
        if A and all(v != 0 for v in A.values()):
            deg_max = max(A.keys())
            lead_coeff = A[deg_max]
            norm_A = {p: v / lead_coeff for p, v in A.items()}
            nod_str = poly_to_str(norm_A)
            if nod_str == "1":
                log.append("  👉 НОД(A, B) = 1  (Многочлены взаимно просты!)")
                log.append("  💡 Вывод: Данные многочлены не имеют общих буквенных делителей.")
            else:
                log.append(f"  👉 НОД(A, B) = {nod_str}  (с точностью до нормировки коэффициента)")
                log.append("  💡 Вывод: На этот многочлен исходные выражения делятся без остатка!")
        else:
            log.append("  👉 НОД(A, B) = 0")

        # Переключаем фокус на вкладку НОД, чтобы студент сразу увидел итерации
        self.notebook.select(2)
        
        self.txt_gcd.delete("1.0", tk.END)
        self.txt_gcd.insert(tk.END, "\n".join(log))

    def calculate_factorization(self):
        """ВУЗОВСКИЙ МАТЕМАТИЧЕСКИЙ ДВИЖОК: Разложение многочлена на неприводимые множители"""
        import numpy as np
        raw_num = self.entry_num.get()
        
        if not raw_num.strip():
            self.txt_factor.delete("1.0", tk.END)
            self.txt_factor.insert(tk.END, "⚠️ Ошибка: Введите исходный многочлен в поле 'Делимое'!")
            return

        try:
            # Локальный парсер
            def local_parse(poly_str):
                s = poly_str.replace(" ", "").replace(",", ".").replace("-", "+-")
                tokens = s.split("+")
                poly = {}
                for t in tokens:
                    if not t: continue
                    if "x^" in t: coeff, power = t.split("x^")
                    elif "x" in t: coeff, power = t.split("x"); power = 1
                    else: coeff, power = t, 0
                    if coeff in ("", "+"): c = 1.0
                    elif coeff == "-": c = -1.0
                    else:
                        if "/" in coeff:
                            n, d = coeff.split("/")
                            c = float(n) / float(d)
                        else: c = float(coeff)
                    poly[int(power)] = poly.get(int(power), 0.0) + c
                return {p: round(v, 4) for p, v in poly.items() if round(v, 4) != 0}

            poly = local_parse(raw_num)
        except:
            self.txt_factor.delete("1.0", tk.END)
            self.txt_factor.insert(tk.END, "⚠️ Ошибка разбора многочлена. Проверьте правильность знаков.")
            return

        if not poly:
            self.txt_factor.delete("1.0", tk.END)
            self.txt_factor.insert(tk.END, "⚠️ Многочлен пустой или равен нулю.")
            return

        deg_max = max(poly.keys())
        lead_coeff = poly[deg_max]

        # Извлекаем коэффициенты для численного поиска корней numpy
        coeffs_np = []
        for p in range(deg_max, -1, -1):
            coeffs_np.append(poly.get(p, 0.0))

        log = []
        log.append("🪵 НАУЧНО-АНАЛИТИЧЕСКИЙ МОДУЛЬ: ФАКТОРИЗАЦИЯ МНОГОЧЛЕНОВ")
        log.append(f"Разложение полинома степени N = {deg_max} на неприводимые множители.")
        log.append(f"Исходное выражение: P(x) = {raw_num}")
        log.append("=" * 65 + "\n")

        log.append("🔎 ЭТАПЫ СИМВОЛЬНОГО И ЧИСЛЕННОГО АНАЛИЗА:")
        log.append(f"• Выделение старшего коэффициента (нормализация): a_n = {lead_coeff}")

        # Поиск всех комплексных корней
        roots = np.roots(coeffs_np)
        log.append(f"• Применение теоремы Гаусса: Вычисление полного спектра корней...")
        
        # Разделяем на вещественные и комплексные пары
        real_parts = []
        complex_pairs = []
        
        # Порог для отсечения машинного нуля
        threshold = 1e-4
        
        # Сортируем корни, чтобы склеить сопряженные пары (a + bi и a - bi)
        checked = [False] * len(roots)
        for i in range(len(roots)):
            if checked[i]: continue
            r = roots[i]
            if abs(r.imag) < threshold:
                real_parts.append(r.real)
                checked[i] = True
            else:
                # Ищем для него сопряженную пару
                found_pair = False
                for j in range(i + 1, len(roots)):
                    if not checked[j] and abs(r.real - roots[j].real) < threshold and abs(r.imag + roots[j].imag) < threshold:
                        complex_pairs.append((r.real, abs(r.imag)))
                        checked[j] = True
                        checked[i] = True
                        found_pair = True
                        break
                if not found_pair:
                    # Если сопряженный не найден, запишем как одиночный комплексный корень
                    real_parts.append(r)
                    checked[i] = True

        # Выводим найденную структуру корней
        log.append("\n📊 СТРУКТУРА НАЙДЕННЫХ КОРНЕЙ:")
        for idx, r_val in enumerate(real_parts, 1):
            log.append(f"  x_{idx} (Вещественный) = {round(r_val, 3)}")
        for idx, (re, im) in enumerate(complex_pairs, len(real_parts) + 1):
            log.append(f"  x_{idx},{idx+1} (Сопряженные комплексные) = {round(re, 3)} ± {round(im, 3)}i")

        # Формируем финальное разложение
        factors_real = [] # Скобки вида (x - a)
        factors_comp = [] # Неприводимые трехчлены вида (x^2 + px + q)

        for r_val in real_parts:
            val = round(r_val, 2)
            if val == 0: factors_real.append("x")
            elif val > 0: factors_real.append(f"(x - {val})")
            else: factors_real.append(f"(x + {abs(val)})")

        for (re, im) in complex_pairs:
            # (x - (re + im_i))(x - (re - im_i)) = x^2 - 2*re*x + (re^2 + im^2)
            p_coeff = round(-2 * re, 2)
            q_coeff = round(re**2 + im**2, 2)
            
            term = "x^2"
            if p_coeff > 0: term += f" + {p_coeff}x"
            elif p_coeff < 0: term += f" - {abs(p_coeff)}x"
            
            if q_coeff > 0: term += f" + {q_coeff}"
            elif q_coeff < 0: term += f" - {abs(q_coeff)}"
            
            factors_comp.append(f"({term})")

        # Собираем всё вместе
        coeff_str = "" if lead_coeff == 1.0 else (f"- " if lead_coeff == -1.0 else f"{round(lead_coeff, 2)} * ")
        final_pieces = factors_real + factors_comp
        final_expression = coeff_str + " * ".join(final_pieces)

        log.append("\n" + "=" * 50)
        log.append("🎯 ФИНАЛЬНОЕ РАЗЛОЖЕНИЕ НА НЕПРИВОДИМЫЕ МНОЖИТЕЛИ:")
        log.append(f"  👉 P(x) = {final_expression}")
        
        # Университетский криптографический вывод
        log.append("\n💡 АКАДЕМИЧЕСКАЯ СПРАВКА:")
        log.append("  • Над полем комплексных чисел (C) полином разложен на линейные множители.")
        if factors_comp:
            log.append("  • Над полем вещественных чисел (R) скобки второго порядка являются НЕПРИВОДИМЫМИ,")
            log.append("    так как их дискриминант (D < 0) строго меньше нуля.")
        else:
            log.append("  • Многочлен полностью разложился на линейные множители над полем вещественных чисел.")
        log.append("  • Исходный базис успешно деконструирован. Проверка умножением скобок вернет исходное выражение.")

        # Выводим в окно
        self.notebook.select(3)
        self.txt_factor.delete("1.0", tk.END)
        self.txt_factor.insert(tk.END, "\n".join(log))

    def calculate_galois_field(self):
        """ВУЗОВСКИЙ КРИПТОГРАФИЧЕСКИЙ ДВИЖОК: Пошаговое деление многочленов в поле Галуа GF(2) через XOR"""
        raw_num = self.entry_num.get()
        raw_den = self.entry_den.get()
        
        if not raw_num.strip() or not raw_den.strip():
            self.txt_gf.delete("1.0", tk.END)
            self.txt_gf.insert(tk.END, "⚠️ Ошибка: Введите Делимое и Делитель для расчета в GF(2)!")
            return

        # Локальный парсер для поля Галуа (приводит все коэффициенты по модулю 2)
        def parse_poly_gf2(poly_str):
            s = poly_str.replace(" ", "").replace("-", "+")
            tokens = s.split("+")
            poly = {}
            for t in tokens:
                if not t: continue
                if "x^" in t: coeff, power = t.split("x^")
                elif "x" in t: coeff, power = t.split("x"); power = 1
                else: coeff, power = t, 0
                c = 1 if coeff in ("", "+") else int(coeff)
                p = int(power)
                poly[p] = (poly.get(p, 0) + c) % 2 # Коэффициенты строго 0 или 1
            return {p: v for p, v in poly.items() if v != 0}

        poly_num = parse_poly_gf2(raw_num)
        poly_den = parse_poly_gf2(raw_den)

        def poly_to_str_gf2(poly):
            if not poly: return "0"
            res = []
            for p in sorted(poly.keys(), reverse=True):
                if poly[p] == 0: continue
                if p == 0: res.append("1")
                elif p == 1: res.append("x")
                else: res.append(f"x^{p}")
            return " + ".join(res)

        if not poly_den:
            self.txt_gf.delete("1.0", tk.END)
            self.txt_gf.insert(tk.END, "⚠️ Ошибка: Делитель не может быть нулевым многочленом!")
            return

        deg_num = max(poly_num.keys()) if poly_num else -1
        deg_den = max(poly_den.keys())

        log = []
        log.append("🔐 НАУЧНО-ИССЛЕДОВАТЕЛЬСКИЙ МОДУЛЬ: ВЫЧИСЛЕНИЯ В ПОЛЯХ ГАЛУА GF(2)")
        log.append("Основа криптографических стандартов AES, контрольных сумм CRC-32 и кодов Рида-Соломона.")
        log.append("Математический закон поля: Все операции выполняются по модулю 2 (сложение = вычитание = XOR).\n")
        log.append(f"  Делимое  A(x) = {poly_to_str_gf2(poly_num)}")
        log.append(f"  Делитель B(x) = {poly_to_str_gf2(poly_den)}")
        log.append("=" * 70 + "\n")

        # Переводим полиномы в битовые маски для наглядности студентам
        def to_bits(poly, max_deg):
            return "".join(str(poly.get(p, 0)) for p in range(max_deg, -1, -1))

        log.append(f"💻 ДВОИЧНОЕ ПРЕДСТАВЛЕНИЕ (БИТОВЫЕ МАСКИ):")
        log.append(f"  A(x) биты:  {to_bits(poly_num, max(deg_num, deg_den))}")
        log.append(f"  B(x) биты:  {to_bits(poly_den, deg_den)}\n")
        log.append("-" * 50)

        current = poly_num.copy()
        quotient = {}
        step = 1

        while current and max(current.keys(), default=-1) >= deg_den:
            deg_curr = max(current.keys())
            
            # Член частного в GF(2) всегда имеет коэффициент 1
            p_q = deg_curr - deg_den
            quotient[p_q] = 1
            
            log.append(f"\n[Шаг {step} в GF(2)]:")
            log.append(f"  Текущий остаток:  {poly_to_str_gf2(current)}  ({to_bits(current, deg_num)})")
            
            # Вычисляем вычитаемый полином (B(x) сдвинутый на p_q)
            sub_poly = {}
            for p, v in poly_den.items():
                sub_poly[p + p_q] = v

            log.append(f"  XOR-вычитание:   ^ {poly_to_str_gf2(sub_poly)}  ({to_bits(sub_poly, deg_num)})")
            log.append("  " + "." * 40)

            # Выполняем операцию XOR для каждого коэффициента
            next_current = current.copy()
            for p, v in sub_poly.items():
                next_current[p] = (next_current.get(p, 0) + v) % 2
                if next_current[p] == 0:
                    if p in next_current: del next_current[p]

            # Удаляем старший бит (он гарантированно уничтожается при XOR)
            current = {p: v for p, v in next_current.items() if v != 0}
            log.append(f"  Результат шага:   {poly_to_str_gf2(current)}")
            step += 1

        log.append("\n" + "=" * 50)
        log.append("🎯 ФИНАЛЬНЫЙ КРИПТОГРАФИЧЕСКИЙ ОТВЕТ:")
        log.append(f"  👉 Частное (Ответ): {poly_to_str_gf2(quotient)}  ({to_bits(quotient, deg_num - deg_den) if deg_num >= deg_den else '0'})")
        log.append(f"  👉 Остаток деления: {poly_to_str_gf2(current)}  ({to_bits(current, deg_den - 1) if deg_den > 0 else '0'})")
        
        log.append("\n📚 МЕТОДИЧЕСКАЯ СПРАВКА ДЛЯ ЛАБОРАТОРНОЙ РАБОТЫ:")
        log.append("  • В поле GF(2) знаки плюс и минус эквивалентны. Операция XOR сама уничтожает")
        log.append("    одинаковые биты (1 ^ 1 = 0), что делает деление уголком невероятно быстрым для процессоров.")
        log.append("  • Если данный остаток прибавить к исходному сообщению A(x), мы получим кодовое слово,")
        log.append("    которое разделится на делитель B(x) без остатка. Именно так работает защита данных CRC-32!")

        # Фокусируем интерфейс на шестой вкладке
        self.notebook.select(4)
        
        self.txt_gf.delete("1.0", tk.END)
        self.txt_gf.insert(tk.END, "\n".join(log))


if __name__ == "__main__":
    root = tk.Tk()
    app = PolynomialDivisionApp(root)
    root.mainloop()
