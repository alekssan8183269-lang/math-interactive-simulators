import numpy as np
import matplotlib.pyplot as plt

# Отключаем лишние предупреждения
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Настройка шрифта для русского языка
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# Включаем интерактивный режим
plt.ion()

class IntervalMethodApp:
    def __init__(self):
        # Создаем окно: сверху числовая ось, снизу график функции
        self.fig, (self.ax_axis, self.ax_graph) = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [1, 1.8]})
        plt.subplots_adjust(left=0.06, bottom=0.1, right=0.72, hspace=0.35)
        
        # Начальные координаты корней: x1 и x2 - числитель, x3 - знаменатель
        self.roots = [2.0, 6.0, -1.0] # [x1, x2, x3]
        self.active_root_idx = None
        
        # --- 1. Настройка Верхней оси (Школьный метод интервалов) ---
        self.ax_axis.set_xlim(-10, 10)
        self.ax_axis.set_ylim(-2, 2)
        self.ax_axis.axis('off')
        
        # Рисуем числовую прямую X
        self.ax_axis.axhline(0, color='black', lw=2, zorder=1)
        self.ax_axis.text(9.8, -0.3, 'X', fontsize=12, fontweight='bold')
        
        # Заготовки для корней (x1, x2 - закрашенные, x3 - выколотая точка ОДЗ)
        self.dot_x1, = self.ax_axis.plot([], [], 'go', markersize=10, label='Корень числителя (закрашен)', zorder=5)
        self.dot_x2, = self.ax_axis.plot([], [], 'go', markersize=10, zorder=5)
        self.dot_x3, = self.ax_axis.plot([], [], 'ro', markerfacecolor='white', markeredgewidth=2.5, markersize=10, label='Ноль знаменателя (выколот)', zorder=5)
        
        # Текстовые подписи координат под точками
        self.lbl_x1 = self.ax_axis.text(0, -0.6, '', ha='center', color='darkgreen', fontsize=10, fontweight='bold')
        self.lbl_x2 = self.ax_axis.text(0, -0.6, '', ha='center', color='darkgreen', fontsize=10, fontweight='bold')
        self.lbl_x3 = self.ax_axis.text(0, -0.6, '', ha='center', color='darkred', fontsize=10, fontweight='bold')
        
        # Списки для динамических дуг и знаков
        self.arc_lines = []
        self.sign_texts = []
        
        # --- 2. Настройка Нижней оси (График функции) ---
        self.ax_graph.set_xlim(-10, 10)
        self.ax_graph.set_ylim(-15, 15)
        self.ax_graph.grid(True, linestyle=':', alpha=0.6)
        self.ax_graph.axhline(0, color='black', lw=1.2)
        self.ax_graph.set_title("График функции y = (x - x1)(x - x2) / (x - x3)", fontsize=12, fontweight='bold')
        
        self.graph_line, = self.ax_graph.plot([], [], color='royalblue', lw=2.5)
        self.graph_asymptote = self.ax_graph.axvline(0, color='crimson', ls='--', lw=1.5, label='Асимптота (деление на 0)')
        
        # Информационная текстовая панель далеко справа (1.02)
        self.info_text = self.ax_graph.text(1.02, 0.95, '', transform=self.ax_graph.transAxes, 
                                           verticalalignment='top', fontsize=11,
                                           bbox=dict(facecolor='#f9f9f9', alpha=0.95, edgecolor='gray'))
        
        # Подключаем мышку для перетаскивания точек
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        
        self.ax_axis.legend(loc='upper left', fontsize=9, frameon=True)
        self.update_all()
        
        plt.ioff()
        plt.show()

    # Математическая функция дробного выражения
    def evaluate_func(self, x_val):
        x1, x2, x3 = self.roots
        denom = x_val - x3
        # Защита от деления на ноль в массивах NumPy
        with np.errstate(divide='ignore', invalid='ignore'):
            res = ((x_val - x1) * (x_val - x2)) / denom
        return res

    def update_all(self):
        x1, x2, x3 = self.roots
        
        # 1. Обновляем положения точек на числовой прямой
        self.dot_x1.set_data([x1], [0])
        self.dot_x2.set_data([x2], [0])
        self.dot_x3.set_data([x3], [0])
        
        self.lbl_x1.set_position((x1, -0.5)); self.lbl_x1.set_text(f"x1={x1:.1f}")
        self.lbl_x2.set_position((x2, -0.5)); self.lbl_x2.set_text(f"x2={x2:.1f}")
        self.lbl_x3.set_position((x3, -0.5)); self.lbl_x3.set_text(f"x3={x3:.1f}")
        
        # 2. Перерисовываем дуги интервалов и знаки
        # Очищаем старые дуги и знаки
        for line in self.arc_lines: line.remove()
        for txt in self.sign_texts: txt.remove()
        self.arc_lines.clear()
        self.sign_texts.clear()
        
        # Сортируем все критические точки по возрастанию для правильного разбиения прямой
        sorted_pts = sorted(self.roots)
        intervals = [-10.0] + sorted_pts + [10.0]
        
        # Строим дуги для каждого промежутка
        for i in range(len(intervals) - 1):
            left, right = intervals[i], intervals[i+1]
            mid = (left + right) / 2
            
            # Проверяем знак функции в средней точке интервала
            test_val = self.evaluate_func(mid)
            is_positive = test_val > 0
            
            # Рисуем дугу (параболический изгиб вверх)
            arc_x = np.linspace(left, right, 50)
            # Формула перевернутой параболы для красивой дуги: h * (x - left) * (right - x)
            # Ограничиваем высоту для крайних бесконечных интервалов
            width = right - left
            h = 1.2 / (width) if width < 8 else 0.2
            arc_y = h * (arc_x - left) * (right - arc_x)
            
            line, = self.ax_axis.plot(arc_x, arc_y, color='darkgray', lw=2, ls='-', zorder=2)
            self.arc_lines.append(line)
            
            # Ставим знак ПЛЮС или МИНУС по центру дуги
            sign_char = "+" if is_positive else "−"
            color_char = 'green' if is_positive else 'crimson'
            txt = self.ax_axis.text(mid, max(arc_y) + 0.2, sign_char, color=color_char, 
                                    fontsize=14, fontweight='bold', ha='center', va='center')
            self.sign_texts.append(txt)
            
        # 3. Обновляем нижний график функции
        x_grid = np.linspace(-10, 10, 1000)
        y_grid = self.evaluate_func(x_grid)
        # Сглаживаем разрыв графика возле асимптоты, чтобы линии не соединялись вертикально
        y_grid[abs(x_grid - x3) < 0.1] = np.nan
        
        self.graph_line.set_data(x_grid, y_grid)
        self.graph_asymptote.set_xdata([x3, x3])
        
        # 4. Формируем текстовое решение неравенства f(x) ≥ 0
        # Генерируем красивую школьную запись ответа в виде промежутков
        ans_parts = []
        for i in range(len(intervals) - 1):
            left, right = intervals[i], intervals[i+1]
            if self.evaluate_func((left + right) / 2) >= 0:
                # Определяем тип скобок: бесконечность всегда круглая, x3 (знаменатель) всегда круглая
                l_bracket = "(" if left == -10.0 or left == x3 else "["
                r_bracket = ")" if right == 10.0 or right == x3 else "]"
                
                l_str = "−∞" if left == -10.0 else f"{left:.1f}"
                r_str = "+∞" if right == 10.0 else f"{right:.1f}"
                ans_parts.append(f"{l_bracket}{l_str}; {r_str}{r_bracket}")
                
        answer_string = " ∪ ".join(ans_parts) if ans_parts else "Нет решений"
        
        self.info_text.set_text(
            f"МЕТОД ИНТЕРВАЛОВ:\n"
            f"----------------------------------------\n"
            f"Решаем неравенство: f(x) ≥ 0\n\n"
            f"Критические точки (нули):\n"
            f"Числитель (нули функции):\n"
            f"x = {x1:.1f}  и  x = {x2:.1f}\n"
            f"Знаменатель (ОДЗ: x ≠ x3):\n"
            f"x ≠ {x3:.1f}\n\n"
            f"ПРАВИЛО МЕТОДА:\n"
            f"Знаменатель СЕГДА выколот!\n"
            f"Если точка пришла из знаменателя,\n"
            f"скобка около неё будет КРУГЛОЙ.\n\n"
            f"----------------------------------------\n"
            f"ОТВЕТ ДЛЯ f(x) ≥ 0:\n"
            f"x ∈ {answer_string}"
        )
        self.fig.canvas.draw_idle()

    # Логика захвата точек мышкой
    def on_press(self, event):
        if event.inaxes != self.ax_axis: return
        # Ищем, к какому корню кликнули ближе всего
        distances = [abs(event.xdata - r) for r in self.roots]
        min_dist = min(distances)
        if min_dist < 0.6: # радиус захвата точки
            self.active_root_idx = distances.index(min_dist)

    def on_motion(self, event):
        if self.active_root_idx is None or event.xdata is None: return
        # Ограничиваем движение рамками числовой оси
        new_coord = np.clip(round(event.xdata, 1), -9.0, 9.0)
        
        # Не даем точкам сливаться идеально в ноль, чтобы не ломать структуру интервалов
        if any(abs(new_coord - r) < 0.1 for i, r in enumerate(self.roots) if i != self.active_root_idx):
            return
            
        self.roots[self.active_root_idx] = new_coord
        self.update_all()

    def on_release(self, event):
        self.active_point_idx = None
        self.active_root_idx = None

if __name__ == '__main__':
    app = IntervalMethodApp()




import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

# Отключаем лишние предупреждения для стабильности интерфейса
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Настройка шрифта для идеального отображения русского языка
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# Включаем интерактивный режим
plt.ion()

# --- МАТЕМАТИЧЕСКАЯ ФУНКЦИЯ АНАЛИЗА ЧИСЛА ---
def classify_user_number(text):
    # Очищаем текст и заменяем запятую на точку для поддержки дробей
    text = text.strip().replace(',', '.')
    if not text:
        return None, "Введите число"
    
    # Константы Юникода и стандартные математические буквы
    if text.lower() in ['pi', 'π']:
        return ['R'], "Число π ≈ 3.14 — Иррациональное\n(Принадлежит только множеству R)"
    if text.lower() in ['e']:
        return ['R'], "Число e ≈ 2.718 — Иррациональное\n(Принадлежит только множеству R)"
        
    # Проверка на квадратный корень (поддерживает ввод вида sqrt(2) или √2)
    if 'sqrt' in text.lower() or '√' in text:
        clean = text.replace('sqrt', '').replace('√', '').replace('(', '').replace(')', '').strip()
        try:
            val = float(clean)
            root_val = np.sqrt(val)
            # Если корень извлекается нацело (например, √4 = 2)
            if root_val.is_integer():
                if root_val > 0: 
                    return ['N', 'Z', 'Q', 'R'], f"√{clean} = {int(root_val)}\n(Натуральное, Целое, Рациональное, Действительное)"
                return ['Z', 'Q', 'R'], f"√{clean} = {int(root_val)}\n(Целое, Рациональное, Действительное)"
            else:
                # Если корень не извлекается нацело — это иррациональное число
                return ['R'], f"√{clean} ≈ {root_val:.3f} — Иррациональное\n(Принадлежит только множеству R)"
        except:
            return None, "Неверный формат корня"

    # Стандартная проверка через попытку перевода в float
    try:
        val = float(text)
        # Проверяем, является ли число целым (нет дробной части)
        if val.is_integer():
            int_val = int(val)
            if int_val > 0:
                return ['N', 'Z', 'Q', 'R'], f"{int_val} — Натуральное число (для счета).\nОно лежит в самом центре, поэтому\nавтоматически является Целым,\nРациональным и Действительным!"
            else:
                return ['Z', 'Q', 'R'], f"{int_val} — Целое число (но не натуральное).\nОно входит в множества Z, Q и R!"
        else:
            # Обыкновенная или десятичная дробь
            return ['Q', 'R'], f"{val} — Рациональное число (дробь).\nОно входит в множества Q и R!"
    except ValueError:
        return None, "Это не число! Введите цифрами\n(например: 5; -12; 0.75; √2; pi)"


# --- КЛАСС ГРАФИЧЕСКОГО ИНТЕРФЕЙСА ---
class NumberSetsApp:
    def __init__(self):
        # Создаем большое квадратное окно
        self.fig, self.ax = self.subplots_setup()
        
        # Названия множеств и параметры кругов (от большего к меньшему)
        self.set_names = ['R', 'Q', 'Z', 'N']
        self.radii = [10.0, 7.5, 5.0, 2.5]
        
        # Пастельные фоновые цвета (когда галочка/число не активны)
        self.default_colors = ['#ffcccc', '#ffe6cc', '#e6ffcc', '#ccf2ff']
        # Яркие контрастные цвета (когда число входит в это множество)
        self.active_colors = ['#ff4d4d', '#ffa64d', '#99ff33', '#33ccff']
        
        # Рисуем круги-матрёшки
        self.circles = []
        for i in range(4):
            circle = plt.Circle((0, 0), self.radii[i], facecolor=self.default_colors[i], edgecolor='dimgray', lw=2, zorder=i+1)
            self.ax.add_patch(circle)
            self.circles.append(circle)
            
        # Статичные подписи названий множеств на чертеже
        self.ax.text(0, 8.5, "R — Действительные (Все числа)", fontsize=12, fontweight='bold', ha='center', zorder=10)
        self.ax.text(0, 6.0, "Q — Рациональные (Дроби)", fontsize=11, fontweight='bold', ha='center', zorder=10)
        self.ax.text(0, 3.5, "Z — Целые (..., -2, -1, 0, 1, 2...)", fontsize=10, fontweight='bold', ha='center', zorder=10)
        self.ax.text(0, 0, "N — Натуральные (1, 2, 3...)", fontsize=10, fontweight='bold', ha='center', va='center', zorder=10)
        
        # Большая информационная панель справа
        self.info_text = self.ax.text(1.05, 0.5, "", transform=self.ax.transAxes, 
                                           verticalalignment='center', fontsize=12, fontweight='medium',
                                           bbox=dict(facecolor='#f9f9f9', alpha=0.95, edgecolor='gray', boxstyle='round,pad=1'))
        
        # Создаем белое поле ввода текста (TextBox) внизу графика
        ax_box = plt.axes([0.35, 0.04, 0.3, 0.05])
        self.text_box = TextBox(ax_box, 'Введите число и нажмите Enter: ', initial="5", color='white', hovercolor='#f0f0f0')
        self.text_box.on_submit(self.submit)
        
        # Первичный холостой запуск с числом 5, чтобы приложение сразу открылось красивым
        self.submit("5")
        
        plt.ioff()
        plt.show()

    def subplots_setup(self):
        fig, ax = plt.subplots(figsize=(13, 8))
        # left=0.05, right=0.72 освобождает место справа под текстовую панель анализа
        plt.subplots_adjust(left=0.05, bottom=0.15, right=0.72, top=0.92)
        ax.set_xlim(-11, 11)
        ax.set_ylim(-11, 11)
        ax.set_aspect('equal')
        ax.axis('off') # убираем стандартную сетку декартовых координат
        ax.set_title("Классификация чисел: Интерактивная Матрёшка Множеств", fontsize=14, color='#1a365d', fontweight='bold', pad=15)
        return fig, ax

    def submit(self, text):
        # Отправляем текст в математический анализатор
        active_sets, report = classify_user_number(text)
        
        # Если ввели некорректный текст (буквы вместо цифр)
        if active_sets is None:
            self.info_text.set_text(f"ОШИБКА ОПРЕДЕЛЕНИЯ:\n---------------------------\n{report}")
            # Возвращаем всем кругам блеклый дефолтный цвет
            for i in range(4):
                self.circles[i].set_facecolor(self.default_colors[i])
            self.fig.canvas.draw_idle()
            return
            
        # Строим текстовую строку иерархии вложенности
        chain_str = "Иерархия вложенности множеств:\n"
        
        # Перекрашиваем круги: активные делаем яркими, неактивные — тусклыми
        for i, name in enumerate(self.set_names):
            if name in active_sets:
                self.circles[i].set_facecolor(self.active_colors[i])
                chain_str += f" ✅ {name} "
            else:
                self.circles[i].set_facecolor(self.default_colors[i])
                chain_str += f" ❌ {name} "
            if i < 3: 
                chain_str += "⊃ "  # математический знак включения множеств
            
        # Собираем итоговый текст на правую плашку
        full_report = (
            f"АНАЛИЗ ВВЕДЕННОГО ЧИСЛА:\n"
            f"----------------------------------------\n"
            f"Вы ввели: {text}\n\n"
            f"{report}\n\n"
            f"----------------------------------------\n"
            f"{chain_str}"
        )
        
        self.info_text.set_text(full_report)
        self.fig.canvas.draw_idle()

if __name__ == '__main__':
    # Запускаем наше изолированное приложение
    app = NumberSetsApp()



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Настройка интерактивного режима для отображения окна
plt.ion()

# Функция для вычисления корней и дискриминанта
def calculate_quadratic(a, b, c):
    D = b**2 - 4*a*c
    if D > 0:
        x1 = (-b + np.sqrt(D)) / (2*a)
        x2 = (-b - np.sqrt(D)) / (2*a)
        return D, f"D = {D:.2f}\nx1 = {x1:.2f}\nx2 = {x2:.2f}", [x1, x2]
    elif D == 0:
        x1 = -b / (2*a)
        return D, f"D = 0.00\nx1 = x2 = {x1:.2f}", [x1]
    else:
        return D, f"D = {D:.2f}\nКорней нет", []

# Создаем фигуру и оси
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.3)  # Оставляем место внизу для ползунков

# Начальные значения коэффициентов: y = 1*x^2 + 0*x - 4
a_init, b_init, c_init = 1.0, 0.0, -4.0

# Генерируем точки X для графика
x = np.linspace(-10, 10, 400)
y = a_init * x**2 + b_init * x + c_init

# Рисуем оси координат для наглядности
ax.axhline(0, color='black', lw=1, ls='--')
ax.axvline(0, color='black', lw=1, ls='--')

# Строим параболу
line, = ax.plot(x, y, lw=2.5, color='royalblue', label=f'$y = {a_init}x^2 + {b_init}x + {c_init}$')

# Считаем начальные корни и дискриминант
D, info_text, roots = calculate_quadratic(a_init, b_init, c_init)

# Отображаем корни точками на графике
root_dots, = ax.plot(roots, [0]*len(roots), 'ro', markersize=8, label='Корни (x1, x2)')

# Добавляем текстовый блок с информацией
text_box = ax.text(-9, 60, info_text, fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# Настраиваем внешний вид графика
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 80)
ax.set_title("Интерактивное квадратичное уравнение", fontsize=14, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right')

# --- Создаем ползунки (Sliders) ---
# Цвета для интерфейса
ax_color = 'lightgoldenrodyellow'

# Ползунок для 'a' (не должен быть равен 0, поэтому диапазон от -5 до 5 с шагом, исключая 0)
ax_a = plt.axes([0.15, 0.18, 0.7, 0.03], facecolor=ax_color)
slider_a = Slider(ax_a, 'Коэффициент a', -5.0, 5.0, valinit=a_init, valstep=0.1)

# Ползунок для 'b'
ax_b = plt.axes([0.15, 0.12, 0.7, 0.03], facecolor=ax_color)
slider_b = Slider(ax_b, 'Коэффициент b', -10.0, 10.0, valinit=b_init, valstep=0.1)

# Ползунок для 'c'
ax_c = plt.axes([0.15, 0.06, 0.7, 0.03], facecolor=ax_color)
slider_c = Slider(ax_c, 'Коэффициент c', -20.0, 20.0, valinit=c_init, valstep=0.1)

# Функция обновления графика при движении ползунков
def update(val):
    a = slider_a.val
    b = slider_b.val
    c = slider_c.val
    
    # Защита от a = 0 (квадратичное уравнение не должно превращаться в линейное)
    if a == 0:
        a = 0.1
        
    # Обновляем Y-значения параболы
    line.set_ydata(a * x**2 + b * x + c)
    line.set_label(f'$y = {a:.1f}x^2 + {b:.1f}x + {c:.1f}$')
    
    # Пересчитываем дискриминант и корни
    D, info_text, roots = calculate_quadratic(a, b, c)
    
    # Обновляем текст на экране
    text_box.set_text(info_text)
    
    # Обновляем положение точек-корней
    root_dots.set_data(roots, [0]*len(roots))
    
    # Перерисовываем легенду и сам график
    ax.legend(loc='upper right')
    fig.canvas.draw_idle()

# Связываем ползунки с функцией обновления
slider_a.on_changed(update)
slider_b.on_changed(update)
slider_c.on_changed(update)

# Показываем окно (блок iooff переводит в стандартный режим ожидания)
plt.ioff()
plt.show()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.widgets import CheckButtons

# Настройка интерактивного режима
plt.ion()

# Функция для вычисления всех параметров параболы
def calculate_parabola_details(a, b, c):
    # 1. Дискриминант и корни
    D = b**2 - 4*a*c
    if D > 0:
        x1 = (-b + np.sqrt(D)) / (2*a)
        x2 = (-b - np.sqrt(D)) / (2*a)
        roots_text = f"D = {D:.2f}\nx1 = {x1:.2f}\nx2 = {x2:.2f}"
        roots_coords = [x1, x2]
    elif D == 0:
        x1 = -b / (2*a)
        roots_text = f"D = 0.00\nx1 = x2 = {x1:.2f}"
        roots_coords = [x1]
    else:
        roots_text = f"D = {D:.2f}\nКорней нет"
        roots_coords = []
        
    # 2. Вершина параболы (X0, Y0)
    x0 = -b / (2*a)
    y0 = a * x0**2 + b * x0 + c
    
    # 3. Определение максимума/минимума
    vertex_type = "Минимум" if a > 0 else "Максимум"
    vertex_text = f"Вершина ({vertex_type}):\nX0 = {x0:.2f}\nY0 = {y0:.2f}\n\nОсь симметрии:\nX = {x0:.2f}"
    
    return D, roots_text, roots_coords, x0, y0, vertex_text

# Создаем фигуру и оси
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.3, right=0.75)  # Оставляем место внизу для Slider, справа для текста

# Начальные коэффициенты: y = 1*x^2 + 2*x - 3
a_init, b_init, c_init = 1.0, 2.0, -3.0

# Генерируем точки X для параболы
x = np.linspace(-10, 10, 400)
y = a_init * x**2 + b_init * x + c_init

# Рисуем главные оси координат
ax.axhline(0, color='black', lw=1.2, ls='-')
ax.axvline(0, color='black', lw=1.2, ls='-')

# Строим параболу
line, = ax.plot(x, y, lw=2.5, color='royalblue', label='Парабола')

# Расчет начальных данных
D, r_text, roots, x0, y0, v_text = calculate_parabola_details(a_init, b_init, c_init)

# Отображаем корни точками на оси X
root_dots, = ax.plot(roots, [0]*len(roots), 'ro', markersize=8, label='Корни (x1, x2)')

# Отображаем вершину зеленой точкой
vertex_dot, = ax.plot([x0], [y0], 'go', markersize=9, label='Вершина')

# Рисуем вертикальную ось симметрии
symmetry_line = ax.axvline(x0, color='purple', lw=1.5, ls='--', label='Ось симметрии')

# --- Текстовые блоки ---
# Левый блок (Дискриминант и корни)
text_left = ax.text(-9.5, 65, r_text, fontsize=11, bbox=dict(facecolor='white', alpha=0.85, edgecolor='gray'))

# Правый блок за пределами графика (Вершина, Мин/Макс, Ось симметрии)
# Координаты (1.05, 0.5) означают чуть правее основной сетки графика
text_right = ax.text(1.05, 0.5, v_text, fontsize=11, transform=ax.transAxes, 
                     verticalalignment='center', bbox=dict(facecolor='#f9f9f9', alpha=0.9, edgecolor='purple'))

# Настройки сетки и границ
ax.set_xlim(-10, 10)
ax.set_ylim(-15, 80)
ax.set_title("Анализ квадратичной функции", fontsize=14, fontweight='bold', pad=15)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right')

# --- Ползунки (Sliders) ---
ax_color = '#f0f0f0'
ax_a = plt.axes([0.15, 0.18, 0.55, 0.03], facecolor=ax_color)
slider_a = Slider(ax_a, 'Коэфф. a', -5.0, 5.0, valinit=a_init, valstep=0.1)

ax_b = plt.axes([0.15, 0.12, 0.55, 0.03], facecolor=ax_color)
slider_b = Slider(ax_b, 'Коэфф. b', -10.0, 10.0, valinit=b_init, valstep=0.1)

ax_c = plt.axes([0.15, 0.06, 0.55, 0.03], facecolor=ax_color)
slider_c = Slider(ax_c, 'Коэфф. c', -20.0, 20.0, valinit=c_init, valstep=0.1)

# Функция динамического обновления графиков и цифр
def update(val):
    a = slider_a.val
    b = slider_b.val
    c = slider_c.val
    
    # Не даем 'a' стать ровно нулем, чтобы избежать деления на ноль
    if a == 0:
        a = 0.1 if val > 0 else -0.1
        
    # Обновляем параболу
    line.set_ydata(a * x**2 + b * x + c)
    
    # Пересчитываем все параметры
    D, r_text, roots, x0, y0, v_text = calculate_parabola_details(a, b, c)
    
    # Обновляем текстовые панели со значениями
    text_left.set_text(r_text)
    text_right.set_text(v_text)
    
    # Сдвигаем маркеры корней, вершины и линию симметрии
    root_dots.set_data(roots, [0]*len(roots))
    vertex_dot.set_data([x0], [y0])
    symmetry_line.set_xdata([x0, x0])
    
    # Перерисовываем холст
    fig.canvas.draw_idle()

# Привязываем функции обновления к ползункам
slider_a.on_changed(update)
slider_b.on_changed(update)
slider_c.on_changed(update)

plt.ioff()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
# НАЙДИТЕ И ЗАМЕНИТЕ ЭТИ СТРОЧКИ В САМОМ ВЕРХУ КОДА:
plt.rcParams['font.family'] = 'sans-serif'
# Задаем приоритет: сначала Arial для русского текста, затем Symbola для смайликов
plt.rcParams['font.sans-serif'] = ['Arial', 'Symbola'] 
plt.rcParams['axes.unicode_minus'] = False

# Устанавливаем Arial (он отлично поддерживает русский язык и дружит со смайликами)
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False  # Корректное отображение знака минус

# Функция для вычисления площади по координатам вершин (формула Гаусса / шнурования)
def calculate_area(x, y):
    # Координаты должны идти по порядку обхода
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

# Функция для вычисления внутренних углов четырёхугольника
def calculate_angles(x, y):
    angles = []
    num_pts = 4
    for i in range(num_pts):
        # Берем три последовательные точки, чтобы найти угол при вершине i
        p_prev = np.array([x[i-1], y[i-1]])
        p_curr = np.array([x[i], y[i]])
        p_next = np.array([x[(i+1)%num_pts], y[(i+1)%num_pts]])
        
        # Векторы от текущей точки к соседним
        v1 = p_prev - p_curr
        v2 = p_next - p_curr
        
        # Вычисляем угол через скалярное и векторное произведение для точности (от 0 до 360)
        # Вычисление угла через скалярное произведение
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        
        # Защита от микроошибок округления Python (чтобы не вылететь за пределы [-1, 1])
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        
        angle = np.degrees(np.arccos(cos_angle))
        angles.append(angle)
        
    # Небольшая проверка: если фигура стала "вывернутой" (невыпуклой), 
    # сумма углов геометрически всё равно 360, но знаки углов могут потребовать корректировки.
    # Для демонстрации базовых фигур (трапеция, параллелограмм) этого достаточно.
    return angles

# Функция для вычисления длин сторон
def calculate_sides(x, y):
    sides = []
    num_pts = 4
    for i in range(num_pts):
        # Берем текущую точку и следующую (для последней точки следующей будет первая)
        x1, y1 = x[i], y[i]
        x2, y2 = x[(i+1)%num_pts], y[(i+1)%num_pts]
        # Формула расстояния между двумя точками
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        sides.append(distance)
    return sides  # Возвращает список длин: [AB, BC, CD, DA]

def calculate_diagonals_angle(x, y):
    # Вектор AC (от точки 0 к точке 2) и вектор BD (от точки 1 к точке 3)
    v_ac = np.array([x[2] - x[0], y[2] - y[0]])
    v_bd = np.array([x[3] - x[1], y[3] - y[1]])
    
    # Считаем угол через скалярное произведение
    cos_angle = np.dot(v_ac, v_bd) / (np.linalg.norm(v_ac) * np.linalg.norm(v_bd))
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    angle = np.degrees(np.arccos(cos_angle))
    
    # Обычно берут острый угол между прямыми (меньше или равен 90)
    if angle > 90:
        angle = 180 - angle
    return angle

def calculate_centroid(x, y):
    # Координаты центра тяжести для выпуклого четырехугольника
    # вычисляются как среднее арифметическое его вершин
    cx = np.mean(x)
    cy = np.mean(y)
    return cx, cy

# 1. Расчет площади по формуле Брахмагупты (работает ТОЛЬКО для вписанных)
def calculate_brahmagupta_area(sides):
    # sides = [AB, BC, CD, DA]
    p = sum(sides) / 2  # полупериметр
    # Защита от отрицательного значения под корнем, если фигура сильно искажена
    val = (p - sides[0]) * (p - sides[1]) * (p - sides[2]) * (p - sides[3])
    if val < 0:
        return 0
    return np.sqrt(val)

# 2. Расчет уравнения Птолемея (сравнение произведения диагоналей и сторон)
def check_ptolemy_theorem(x, y, sides):
    # Длины диагоналей AC и BD
    d_ac = np.sqrt((x[2] - x[0])**2 + (y[2] - y[0])**2)
    d_bd = np.sqrt((x[3] - x[1])**2 + (y[3] - y[1])**2)
    
    prod_diagonals = d_ac * d_bd
    sum_prod_sides = (sides[0] * sides[2]) + (sides[1] * sides[3])  # AB*CD + BC*DA
    
    return prod_diagonals, sum_prod_sides

# 3. Площадь через диагонали и синус угла между ними
def calculate_area_via_diagonals(x, y, diag_angle):
    d_ac = np.sqrt((x[2] - x[0])**2 + (y[2] - y[0])**2)
    d_bd = np.sqrt((x[3] - x[1])**2 + (y[3] - y[1])**2)
    
    # Формула: 0.5 * d1 * d2 * sin(angle)
    area_via_sin = 0.5 * d_ac * d_bd * np.sin(np.radians(diag_angle))
    return area_via_sin

def get_circumcircle(x, y, angles):
    ang_tol = 2.0  # погрешность для углов
    # Условие существования: сумма противоположных углов ~ 180
    if abs((angles[0] + angles[2]) - 180) < ang_tol and abs((angles[1] + angles[3]) - 180) < ang_tol:
        # Находим центр окружности как пересечение серединных перпендикуляров
        # Для простоты школьной демонстрации возьмем три точки: A(0), B(1), C(2)
        # И построим окружность по трем точкам треугольника ABC
        ax, ay = x[0], y[0]
        bx, by = x[1], y[1]
        cx, cy = x[2], y[2]
        
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(d) < 0.001:
            return None, None, "Невозможно описать"
            
        ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
        uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
        
        radius = np.sqrt((ux - ax)**2 + (uy - ay)**2)
        return ux, uy, radius
    else:
        return None, None, "Углы ≠ 180°"

def get_incircle(x, y, sides, area, perimeter):
    tol = 0.2  # погрешность для сторон
    # Условие существования: AB+CD == BC+DA
    if abs((sides[0] + sides[2]) - (sides[1] + sides[3])) < tol:
        # Радиус вписанной фигуры: r = S / p (где p - полупериметр)
        semi_p = perimeter / 2
        radius = area / semi_p
        
        # Координаты центра (инцентра) через веса сторон для четырехугольника
        # Считаем приближенно для демонстрации как центр пересечения биссектрис
        total_side = sum(sides)
        ix = (sides[2]*x[0] + sides[3]*x[1] + sides[0]*x[2] + sides[1]*x[3]) / total_side
        iy = (sides[2]*y[0] + sides[3]*y[1] + sides[0]*y[2] + sides[1]*y[3]) / total_side
        
        return ix, iy, radius
    else:
        return None, None, "Стороны не равны"

# Функция автоматического определения типа четырёхугольника
def identify_shape(sides, angles, diag_angle):
    # sides = [AB, BC, CD, DA]
    # angles = [A, B, C, D]
    
    # Допуски для округления (компьютер считает с мизерными погрешностями, сглаживаем их)
    tol = 0.15      # для сторон
    ang_tol = 1.5   # для углов
    
    # 1. Проверяем параллельность сторон через равенство противоположных углов
    # В параллелограмме противоположные углы равны: A ≈ C и B ≈ D
    is_opp_angles_equal = abs(angles[0] - angles[2]) < ang_tol and abs(angles[1] - angles[3]) < ang_tol
    
    # 2. Проверяем равенство противоположных сторон
    is_opp_sides_equal = abs(sides[0] - sides[2]) < tol and abs(sides[1] - sides[3]) < tol
    
    # Является ли фигура параллелограммом?
    is_parallelogram = is_opp_angles_equal or is_opp_sides_equal
    
    # 3. Проверяем, все ли углы прямые (близки к 90°)
    all_angles_90 = all(abs(a - 90) < ang_tol for a in angles)
    
    # 4. Проверяем, все ли стороны равны между собой
    all_sides_equal = all(abs(s - sides[0]) < tol for s in sides)
    
    # Классификация на основе признаков:
    if is_parallelogram:
        if all_angles_90 and all_sides_equal:
            return "КВАДРАТ 🟩"
        elif all_angles_90:
            return "ПРЯМОУГОЛЬНИК ▬"
        elif all_sides_equal:
            return "РОМБ 🔷"
        else:
            return "ПАРАЛЛЕЛОГРАММ ▱"
            
    # 5. Если не параллелограмм, проверяем на Трапецию.
    # У трапеции сумма углов, прилежащих к боковой стороне, равна 180°
    # Проверяем пары (A+D) и (B+C) или (A+B) и (C+D)
    trap_cond1 = abs((angles[0] + angles[3]) - 180) < ang_tol and abs((angles[1] + angles[2]) - 180) < ang_tol
    trap_cond2 = abs((angles[0] + angles[1]) - 180) < ang_tol and abs((angles[2] + angles[3]) - 180) < ang_tol
    
    if trap_cond1 or trap_cond2:
        return "ТРАПЕЦИЯ [⏢]"
        
    return "Произвольный четырёхугольник"

def check_parallel_sides(x, y):
    # Проверяем параллельность через равенство углов наклона векторов
    # Векторы сторон AB, BC, CD, DA
    v_ab = np.array([x[1]-x[0], y[1]-y[0]])
    v_bc = np.array([x[2]-x[1], y[2]-y[1]])
    v_cd = np.array([x[3]-x[2], y[3]-y[2]])
    v_da = np.array([x[0]-x[3], y[0]-y[3]])
    
    # Косое произведение векторов противоположных сторон (если близко к 0, то параллельны)
    tol = 0.05
    ab_cd_parallel = abs(np.cross(v_ab, v_cd)) < tol
    bc_da_parallel = abs(np.cross(v_bc, v_da)) < tol
    
    if ab_cd_parallel and bc_da_parallel:
        return "AB || CD  и  BC || DA"
    elif ab_cd_parallel:
        return "AB || CD (основания)"
    elif bc_da_parallel:
        return "BC || DA (основания)"
    else:
        return "Нет параллельных сторон"

# Класс для интерактивного перетаскивания точек мышкой
class InteractivePolygon:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(14, 7.5))
        self.ax.set_xlim(-2, 12)
        self.ax.set_ylim(-2, 12)
        self.ax.grid(True, linestyle=':', alpha=0.5)
        self.ax.set_aspect('equal') # Чтобы углы не искажались визуально
        self.ax.set_title("Свойства четырёхугольника: двигай вершины!", fontsize=14, fontweight='bold')

        
        # Настраиваем новые пропорции: 
        # left=0.06 (минимальный отступ слева)
        # right=0.82 (график теперь занимает аж до 82% ширины окна, освобождая место фигуре)
        plt.subplots_adjust(left=0.06, bottom=0.1, right=0.82, top=0.92)

        # --- БЛОК СОЗДАНИЯ ГАЛОЧЕК ---
        # Выделяем область под графиком для кнопок: [отступ_слева, отступ_снизу, ширина, высота]
        ax_check = plt.axes([0.15, 0.02, 0.2, 0.12], facecolor='#f0f0f0')
        
        # Названия кнопок (должны строго совпадать с тем, что вы хотите скрывать)
        self.labels = ['Диагонали', 'Центр тяжести', 'Описанная окр.', 'Вписанная окр.']
        
        # Начальное состояние (True — галочка стоит, элемент включен)
        self.visibility_states = [True, True, True, True] 
        
        # Создаем сам виджет кнопок
        self.check_buttons = CheckButtons(ax_check, self.labels, self.visibility_states)
        
        # Привязываем функцию toggle_visibility к клику по кнопкам
        self.check_buttons.on_clicked(self.toggle_visibility)

        # Заготовка для отрисовки описанной окружности (зеленый круг без заливки)
        self.circum_circle = plt.Circle((0, 0), 0, color='g', fill=False, ls='--', lw=1.5, label='Описанная окр.')
        self.ax.add_patch(self.circum_circle)

        # Заготовка для отрисовки вписанной окружности (оранжевый круг без заливки)
        self.in_circle = plt.Circle((0, 0), 0, color='darkorange', fill=False, ls='-.', lw=1.5, label='Вписанная окр.')
        self.ax.add_patch(self.in_circle)

        # Заготовка для точки центра тяжести (синяя звездочка)
        self.centroid_dot, = self.ax.plot([], [], 'b*', markersize=11, label='Центр тяжести')
        self.ax.legend(loc='upper left', fontsize=9)

        # Начальные координаты — идеальный квадрат (сторона 4, от 2 до 6)
        self.x = [2.0, 6.0, 6.0, 2.0]
        self.y = [2.0, 2.0, 6.0, 6.0]

        # Заготовка для параллелограмма Вариньона внутри основной фигуры
        self.varignon_poly = Polygon(np.zeros((4, 2)), facecolor='yellow', edgecolor='orange', alpha=0.4, lw=1.5, ls='--')
        self.ax.add_patch(self.varignon_poly)
        
        # Создаем полигон (заливку фигуры)
        self.polygon = Polygon(np.column_stack([self.x, self.y]), facecolor='lightblue', edgecolor='royalblue', alpha=0.6, lw=2)
        self.ax.add_patch(self.polygon)
        
        # Создаем точки вершин, которые можно будет хватать
        self.dots, = self.ax.plot(self.x, self.y, 'ro', markersize=10, picker=True, pickradius=10)
        
        # Текстовые метки для углов возле вершин
        self.angle_labels = [self.ax.text(self.x[i], self.y[i], '', fontsize=10, fontweight='bold') for i in range(4)]
        
        # Боковая панель для вывода площади и суммы углов
        self.info_text = self.ax.text(1.02, 0.5, '', transform=self.ax.transAxes, 
                                      verticalalignment='center', fontsize=12,
                                      bbox=dict(facecolor='#f9f9f9', alpha=0.9, edgecolor='gray'))
        # Заготовки для диагоналей (розовая и оранжевая пунктирные линии)
        self.diag_ac, = self.ax.plot([], [], color='deeppink', ls=':', lw=1.5, label='Диагональ AC')
        self.diag_bd, = self.ax.plot([], [], color='darkorange', ls=':', lw=1.5, label='Диагональ BD')
        
        # Заготовки для средних линий (зеленые линии)
        self.mid_line1, = self.ax.plot([], [], color='green', ls='-.', lw=1.2, label='Ср. линия 1')
        self.mid_line2, = self.ax.plot([], [], color='green', ls='-.', lw=1.2, label='Ср. линия 2')
        
        # Не забудем включить отображение легенды на графике, чтобы ребенок видел названия линий
        self.ax.legend(loc='upper left', fontsize=9)  
        
        # Переменная для отслеживания индекса перетаскиваемой точки
        self.active_point = None
        
        # Подключаем события мыши
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        
        # Первичный расчет и отрисовка текста
        self.update_geometry()

    # Этот метод меняет состояние True/False при клике мышкой на галочку
    def toggle_visibility(self, label):
        # Находим индекс кнопки, на которую нажали
        index = self.labels.index(label)
        # Меняем состояние на противоположное
        self.visibility_states[index] = not self.visibility_states[index]
        # Принудительно обновляем графику, чтобы изменения сразу отобразились
        self.update_geometry()

    def update_geometry(self):
        # Обновляем координаты фигуры и точек
        coords = np.column_stack([self.x, self.y])
        self.polygon.set_xy(coords)
        self.dots.set_data(self.x, self.y)

        # Расчет и обновление положения центра тяжести
        cx, cy = calculate_centroid(self.x, self.y)
        self.centroid_dot.set_data([cx], [cy])

        # ДОБАВИТЬ ЭТУ СТРОКУ: (индекс 1 отвечает за 'Центр тяжести')
        self.centroid_dot.set_visible(self.visibility_states[1])

        # Проверка параллельности
        parallel_status = check_parallel_sides(self.x, self.y)
        
        # Считаем углы и площадь
        angles = calculate_angles(self.x, self.y)
        area = calculate_area(self.x, self.y)
        total_sum = sum(angles)

        # расчет сторон и периметра:
        sides = calculate_sides(self.x, self.y)
        perimeter = sum(sides)

        diag_angle = calculate_diagonals_angle(self.x, self.y)

        # --- НОВЫЕ ГЕОМЕТРИЧЕСКИЕ РАСЧЕТЫ ---
        # 1. Считаем площадь по Брахмагупте
        area_brahma = calculate_brahmagupta_area(sides)
        
        # 2. Проверяем теорему Птолемея
        prod_diag, sum_sides = check_ptolemy_theorem(self.x, self.y, sides)
        
        # 3. Считаем площадь через синус угла диагоналей
        area_sin = calculate_area_via_diagonals(self.x, self.y, diag_angle)
        
        # Рассчитываем линии диагоналей
        self.diag_ac.set_data([self.x[0], self.x[2]], [self.y[0], self.y[2]])
        self.diag_bd.set_data([self.x[1], self.x[3]], [self.y[1], self.y[3]])

        # ДОБАВИТЬ ЭТИ СТРОКИ: (индекс 0 отвечает за 'Диагонали')
        self.diag_ac.set_visible(self.visibility_states[0])
        self.diag_bd.set_visible(self.visibility_states[0])
        
        # 2. Находим середины сторон для средних линий
        mid_ab_x, mid_ab_y = (self.x[0]+self.x[1])/2, (self.y[0]+self.y[1])/2
        mid_bc_x, mid_bc_y = (self.x[1]+self.x[2])/2, (self.y[1]+self.y[2])/2
        mid_cd_x, mid_cd_y = (self.x[2]+self.x[3])/2, (self.y[2]+self.y[3])/2
        mid_da_x, mid_da_y = (self.x[3]+self.x[0])/2, (self.y[3]+self.y[0])/2
        
        # Рисуем средние линии (соединяем противоположные середины)
        self.mid_line1.set_data([mid_ab_x, mid_cd_x], [mid_ab_y, mid_cd_y])
        self.mid_line2.set_data([mid_bc_x, mid_da_x], [mid_bc_y, mid_da_y])

        # Находим середины четырёх сторон
        mid_x = [(self.x[0]+self.x[1])/2, (self.x[1]+self.x[2])/2, (self.x[2]+self.x[3])/2, (self.x[3]+self.x[0])/2]
        mid_y = [(self.y[0]+self.y[1])/2, (self.y[1]+self.y[2])/2, (self.y[2]+self.y[3])/2, (self.y[3]+self.y[0])/2]
        
        # Обновляем координаты жёлтого параллелограмма
        self.varignon_poly.set_xy(np.column_stack([mid_x, mid_y]))
        
        # 3. Считаем угол между диагоналями
        diag_angle = calculate_diagonals_angle(self.x, self.y)

        # Расчет вписанной окружности
        ix, iy, i_res = get_incircle(self.x, self.y, sides, area, perimeter)
        # МОДИФИЦИРОВАТЬ ВАШЕ УСЛОВИЕ (добавить проверку self.visibility_states[3]):
        if isinstance(i_res, float) and self.visibility_states[3]: # Если окружность существует
            self.in_circle.set_center((ix, iy))
            self.in_circle.set_radius(i_res)
            self.in_circle.set_visible(True)
            in_text = f"Возможна (r={i_res:.2f})"
        else:
            self.in_circle.set_visible(False)
            in_text = i_res if isinstance(i_res, str) else "Выключена"

        # Расчет описанной окружности
        ox, oy, o_res = get_circumcircle(self.x, self.y, angles)
        # МОДИФИЦИРОВАТЬ ВАШЕ УСЛОВИЕ (добавить проверку self.visibility_states[2]):
        if isinstance(o_res, float) and self.visibility_states[2]: # Если окружность существует (вернулся радиус)
            self.circum_circle.set_center((ox, oy))
            self.circum_circle.set_radius(o_res)
            self.circum_circle.set_visible(True)
            circum_text = f"Возможна (R={o_res:.2f})"
        else:
            self.circum_circle.set_visible(False)
            # Если выключено галочкой, пишем об этом в текст справа
            circum_text = o_res if isinstance(o_res, str) else "Выключена"

        # Распознаем фигуру
        shape_type = identify_shape(sides, angles, diag_angle)
        
        # Обновляем заголовок графика типом фигуры
        self.ax.set_title(f"Тип фигуры: {shape_type}", fontsize=14, color='darkblue', fontweight='bold', pad=10)

        # Обновляем подписи углов прямо у вершин (с небольшим сдвигом, чтобы не перекрывать точку)
        labels_names = ['A', 'B', 'C', 'D']
        for i in range(4):
            # Смещаем текст чуть наружу от центра для красоты
            dx = 0.3 if self.x[i] >= np.mean(self.x) else -1.2
            dy = 0.3 if self.y[i] >= np.mean(self.y) else -0.5
            self.angle_labels[i].set_position((self.x[i] + dx, self.y[i] + dy))
            self.angle_labels[i].set_text(f"{labels_names[i]}: {angles[i]:.1f}°")


            
        # Обновляем боковую панель данных
        text_content = (
            f"ФИГУРА: {shape_type.split()[0]}\n"
            f"---------------------------\n"
            f"Площадь стандартная (S) = {area:.2f}\n"
            f"Периметр (P) = {perimeter:.2f}\n\n"
            f"Угол между диаг. = {diag_angle:.1f}°\n\n"
            f"Центр тяжести: ({cx:.1f}; {cy:.1f})\n"
            f"Параллельность: {parallel_status}\n"
            f"Описанная окр.: {circum_text}\n"
            f"Вписанная окр.: {in_text}\n"
            f"ТЕОРЕМА О ДИАГОНАЛЯХ (S = 0.5*d1*d2*sin):\n"
            f"Площадь через sin = {area_sin:.2f} (Всегда совпадает!)\n\n"
            f"Длины сторон:\n"
            f"Сторона AB = {sides[0]:.2f}\n"
            f"Сторона BC = {sides[1]:.2f}\n"
            f"Сторона CD = {sides[2]:.2f}\n"
            f"Сторона DA = {sides[3]:.2f}\n\n"
            f"Внутренние углы:\n"
            f"∠A = {angles[0]:.1f}°\n"
            f"∠B = {angles[1]:.1f}°\n"
            f"∠C = {angles[2]:.1f}°\n"
            f"∠D = {angles[3]:.1f}°\n\n"
            f"-------------------\n"
            f"Сумма углов:\n"
            f"A+B+C+D = {total_sum:.1f}°"
            f"ДЛЯ ВПИСАННЫХ ФИГУР (при Окр. Углы=180):\n"
            f"S по Брахмагупте = {area_brahma:.2f}\n"
            f"Т. Птолемея (d1*d2) = {prod_diag:.2f}\n"
            f"Т. Птолемея (ac+bd) = {sum_sides:.2f}\n\n"
        )
        self.info_text.set_text(text_content)
        self.fig.canvas.draw_idle()

    # Срабатывает, когда мы кликаем точно на точку (вершину)
    def on_pick(self, event):
        if event.artist == self.dots:
            self.active_point = event.ind[0]

    # Срабатывает при движении мыши с зажатой кнопкой
    def on_motion(self, event):
        if self.active_point is None or event.xdata is None or event.ydata is None:
            return
        
        # Ограничиваем движение рамками графика для стабильности
        if 0 <= event.xdata <= 10 and 0 <= event.ydata <= 10:
            # Обновляем координату выбранной точки значением из под мышки
            self.x[self.active_point] = round(event.xdata, 1)
            self.y[self.active_point] = round(event.ydata, 1)
            self.update_geometry()

    # Срабатывает, когда отпускаем кнопку мыши
    def on_release(self, event):
        self.active_point = None

# Запуск приложения
if __name__ == '__main__':
    plt.ion()
    app = InteractivePolygon()
    plt.ioff()
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Настройка шрифта для русского языка
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# Включаем интерактивный режим
plt.ion()

# Создаем окно: сверху анимация дороги, снизу график V/t
fig, (ax_road, ax_graph) = plt.subplots(2, 1, figsize=(11, 8), gridspec_kw={'height_ratios': [1, 2]})
plt.subplots_adjust(bottom=0.25, hspace=0.4, right=0.75)

# --- Начальные данные задачи ---
# Задача: Из пунктов А и B, расстояние между которыми 100 км, навстречу друг другу...
S_init = 100.0   # Расстояние, км
v1_init = 15.0   # Скорость 1-го (например, велосипедист), км/ч
v2_init = 25.0   # Скорость 2-го (например, мопедист), км/ч
t_init = 0.0     # Текущее время (старт)

# --- 1. Настройка Верхнего графика (Дорога) ---
ax_road.set_xlim(-5, S_init + 5)
ax_road.set_ylim(-1, 1)
ax_road.axhline(0, color='gray', lw=3, zorder=1) # Сама дорога
ax_road.set_title("Что происходит на дороге:", fontsize=12, fontweight='bold')
ax_road.axis('off') # Прячем оси, оставляем только прямую дороги

# Рисуем пункты А и B
ax_road.text(0, 0.2, 'Пункт А', ha='center', fontweight='bold', color='blue')
ax_road.text(S_init, 0.2, 'Пункт B', ha='center', fontweight='bold', color='red')
ax_road.plot([0, S_init], [0, 0], 'ks', mfc='none', ms=10) # Квадратики пунктов

# Точки-машинки
car1, = ax_road.plot([0], [0], 'bo', markersize=12, label='Первый объект')
car2, = ax_road.plot([S_init], [0], 'ro', markersize=12, label='Второй объект')

# --- 2. Настройка Нижнего графика (Координатная сетка t и S) ---
ax_graph.set_xlim(0, 5) # Максимум 5 часов
ax_graph.set_ylim(0, S_init + 10)
ax_graph.set_xlabel("Время движения, t (в часах)", fontsize=10)
ax_graph.set_ylabel("Пройденный путь / Координата, S (в км)", fontsize=10)
ax_graph.grid(True, linestyle=':', alpha=0.6)
ax_graph.set_title("Графическое решение (Пересечение прямых = Встреча)", fontsize=12, fontweight='bold')

# Линии движения на графике
time_axis = np.linspace(0, 5, 100)
line_car1, = ax_graph.plot([], [], 'b-', lw=2, label='Движение из А')
line_car2, = ax_graph.plot([], [], 'r-', lw=2, label='Движение из B')

# Линия текущего времени (вертикальный маркер)
time_marker = ax_graph.axvline(t_init, color='purple', ls=':', lw=1.5)

# Текстовая панель справа для вывода уравнений
info_text = ax_graph.text(1.05, 0.7, '', transform=ax_graph.transAxes, 
                           verticalalignment='top', fontsize=11,
                           bbox=dict(facecolor='#f9f9f9', alpha=0.95, edgecolor='gray'))

# --- 3. Ползунки управления (Sliders) ---
ax_color = '#f0f0f0'
ax_t  = plt.axes([0.15, 0.14, 0.55, 0.025], facecolor=ax_color)
ax_v1 = plt.axes([0.15, 0.09, 0.55, 0.025], facecolor=ax_color)
ax_v2 = plt.axes([0.15, 0.04, 0.55, 0.025], facecolor=ax_color)

slider_t  = Slider(ax_t, 'Время (ч)', 0.0, 4.0, valinit=t_init, valstep=0.05)
slider_v1 = Slider(ax_v1, 'Скорость V1', 5.0, 50.0, valinit=v1_init, valstep=1)
slider_v2 = Slider(ax_v2, 'Скорость V2', 5.0, 50.0, valinit=v2_init, valstep=1)

# --- 4. Функция обновления графики ---
def update(val):
    t = slider_t.val
    v1 = slider_v1.val
    v2 = slider_v2.val
    S_total = S_init # фиксированное расстояние между городами 100км
    
    # Расчет математики встречи: t_встречи = S / (V1 + V2)
    t_meet = S_total / (v1 + v2)
    S_meet = v1 * t_meet
    
    # Координаты объектов на дороге в текущий момент времени t
    # Первый едет вправо от 0: x = V1 * t
    pos_car1 = min(v1 * t, S_meet if t > t_meet else v1 * t)
    # Второй едет влево от 100: x = 100 - V2 * t
    pos_car2 = max(S_total - v2 * t, S_meet if t > t_meet else S_total - v2 * t)
    
    # Если время вышло за точку встречи — фиксируем объекты в точке встречи
    if t >= t_meet:
        pos_car1 = S_meet
        pos_car2 = S_meet
    
    # Обновляем позиции точек на дороге
    car1.set_data([pos_car1], [0])
    car2.set_data([pos_car2], [0])
    
    # Строим полные прямые движения на нижнем графике до точки встречи
    t_range1 = np.linspace(0, t_meet, 50)
    line_car1.set_data(t_range1, v1 * t_range1)
    line_car2.set_data(t_range1, S_total - v2 * t_range1)
    
    # Двигаем фиолетовый маркер времени
    time_marker.set_xdata([t, t])
    
    # Формируем текст с уравнениями и законами
    text_content = (
        f"УСЛОВИЕ ЗАДАЧИ:\n"
        f"S между А и B = {S_total} км\n"
        f"V1 = {v1} км/ч | V2 = {v2} км/ч\n\n"
        f"ТЕКУЩИЙ МОМЕНТ:\n"
        f"Прошло времени = {t:.2f} ч\n"
        f"1-й проехал = {v1*t if t<t_meet else S_meet:.1f} км\n"
        f"2-й проехал = {v2*t if t<t_meet else (S_total-S_meet):.1f} км\n\n"
        f"МАТЕМАТИКА РЕШЕНИЯ:\n"
        f"Скорость сближения:\n"
        f"Vсбл = V1 + V2 = {v1+v2} км/ч\n"
        f"Уравнение встречи:\n"
        f"t = S / (V1 + V2)\n"
        f"t = {S_total} / ({v1} + {0 if v2<0 else v2})\n\n"
        f"ОТВЕТ ЗАДАЧИ:\n"
        f"Время встречи = {t_meet:.2f} ч\n"
        f"Встреча на отметке = {S_meet:.1f} км"
    )
    
    # Если встретились — выводим крупное уведомление
    if t >= t_meet:
        text_content += "\n\n🎉 ОБЪЕКТЫ ВСТРЕТИЛИСЬ!"
        
    info_text.set_text(text_content)
    fig.canvas.draw_idle()

# Привязываем обновление к ползункам
slider_t.on_changed(update)
slider_v1.on_changed(update)
slider_v2.on_changed(update)

# Первичный запуск отрисовки
update(None)

plt.ioff()
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Rectangle

# Настройка шрифта для идеального отображения русского языка
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# Включаем интерактивный режим
plt.ion()

# Создаем окно: слева бассейн, справа график объема, далеко справа - текст
fig, (ax_pool, ax_graph) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={'width_ratios': [1, 1.5]})
plt.subplots_adjust(left=0.08, bottom=0.25, right=0.72, wspace=0.3)

# --- Начальные данные ---
p1_init = 20.0   # Производительность 1-й трубы (% бассейна в час)
p2_init = 10.0   # Производительность 2-й трубы (% бассейна в час)
t_init = 0.0     # Начальное время (ч)

# --- 1. Настройка левого графика (Бассейн) ---
ax_pool.set_xlim(-1, 5)
ax_pool.set_ylim(-10, 110)
ax_pool.axis('off')
ax_pool.set_title("Анимация бассейна", fontsize=12, fontweight='bold', pad=15)

# Рисуем каркас бассейна (серый прямоугольник)
pool_frame = Rectangle((0, 0), 4, 100, edgecolor='dimgray', facecolor='#e6f2ff', lw=3, zorder=1)
ax_pool.add_patch(pool_frame)

# Заготовка для синей воды (изначально уровень 0)
water_patch = Rectangle((0, 0), 4, 0, edgecolor='none', facecolor='#3399ff', alpha=0.8, zorder=2)
ax_pool.add_patch(water_patch)

# Визуальные трубы (стрелочки для наглядности)
pipe1_text = ax_pool.text(0.5, 105, f"Труба 1: +{p1_init}%/ч", color='blue', fontsize=10, fontweight='bold')
pipe2_text = ax_pool.text(3.5, 105, f"Труба 2: +{p2_init}%/ч", color='darkgreen', fontsize=10, fontweight='bold', ha='right')

# --- 2. Настройка правого графика (Координатная сетка t и V) ---
ax_graph.set_xlim(0, 10)  # Максимум 10 часов
ax_graph.set_ylim(0, 110)
ax_graph.set_xlabel("Время работы, t (в часах)", fontsize=10)
ax_graph.set_ylabel("Заполненность бассейна (в %)", fontsize=10)
ax_graph.grid(True, linestyle=':', alpha=0.6)
ax_graph.set_title("График работы (100% = Полный бассейн)", fontsize=12, fontweight='bold', pad=15)

# Красная пунктирная линия — отметка 100% (целый бассейн)
ax_graph.axhline(100, color='red', ls='--', lw=1.5, label='Бассейн заполнен (100%)')

# Линия изменения объема воды на графике
graph_line, = ax_graph.plot([], [], 'b-', lw=2.5, label='Объем воды')

# Маркер текущего времени (вертикальный фиолетовый пунктир)
time_marker = ax_graph.axvline(t_init, color='purple', ls=':', lw=1.5)
time_point, = ax_graph.plot([], [], 'ro', mfc='white', ms=8) # Точка на графике

# Текстовая панель справа для вывода уравнений
info_text = ax_graph.text(1.06, 0.95, '', transform=ax_graph.transAxes, 
                           verticalalignment='top', fontsize=11,
                           bbox=dict(facecolor='#f9f9f9', alpha=0.95, edgecolor='gray'))

# --- 3. Ползунки управления (Sliders) ---
ax_color = '#f0f0f0'
ax_t  = plt.axes([0.15, 0.14, 0.5, 0.025], facecolor=ax_color)
ax_p1 = plt.axes([0.15, 0.09, 0.5, 0.025], facecolor=ax_color)
ax_p2 = plt.axes([0.15, 0.04, 0.5, 0.025], facecolor=ax_color)

slider_t  = Slider(ax_t, 'Время (ч)', 0.0, 10.0, valinit=t_init, valstep=0.1)
slider_p1 = Slider(ax_p1, 'Труба 1 (%/ч)', 0.0, 50.0, valinit=p1_init, valstep=1)
# Для второй трубы сделаем диапазон от -30 до 50, чтобы она могла работать НА СЛИВ!
slider_p2 = Slider(ax_p2, 'Труба 2 (%/ч)', -30.0, 50.0, valinit=p2_init, valstep=1)

# --- 4. Функция обновления графики ---
def update(val):
    t = slider_t.val
    p1 = slider_p1.val
    p2 = slider_p2.val
    
    # Общая производительность совместной работы: P = P1 + P2
    p_total = p1 + p2
    
    # Расчет времени полного заполнения бассейна (100% / P)
    if p_total > 0:
        t_full = 100.0 / p_total
        status_msg = f"Время до полного заполнения = {t_full:.2f} ч"
    elif p_total < 0:
        t_full = float('inf')
        status_msg = "Бассейн никогда не заполнится\n(слив быстрее наполнения!)"
    else:
        t_full = float('inf')
        status_msg = "Вода не движется (P1 + P2 = 0)"
        
    # Вычисляем текущий объем воды в процентах (V = P_total * t)
    # Ограничиваем рамками от 0% до 100%
    current_volume = p_total * t
    if current_volume > 100:
        current_volume = 100.0
    elif current_volume < 0:
        current_volume = 0.0
        
    # Если бассейн заполнился раньше текущего времени t, фиксируем 100%
    if t >= t_full:
        current_volume = 100.0
        
    # 1. Обновляем анимацию бассейна
    water_patch.set_height(current_volume)
    
    # Меняем подписи над трубами в зависимости от их режима
    pipe1_text.set_text(f"Труба 1:\n+{p1}%/ч" if p1 >= 0 else f"Труба 1:\n{p1}%/ч")
    if p2 >= 0:
        pipe2_text.set_text(f"Труба 2:\n+{p2}%/ч")
        pipe2_text.set_color('darkgreen')
    else:
        pipe2_text.set_text(f"Труба 2 (СЛИВ):\n{p2}%/ч")
        pipe2_text.set_color('crimson') # Если труба сливает — делаем её красной
        
    # 2. Обновляем линию на правом графике
    # Рисуем линию до момента заполнения, а потом она становится горизонтальной на 100%
    t_points = np.linspace(0, max(t, 10), 200)
    v_points = p_total * t_points
    v_points = np.clip(v_points, 0, 100) # Ограничиваем график диапазоном 0-100%
    graph_line.set_data(t_points, v_points)
    
    # Двигаем маркер времени и точку текущего состояния
    time_marker.set_xdata([t, t])
    time_point.set_data([t], [current_volume])
    
    # 3. Формируем математический текст для правой панели
    text_content = (
        f"УСЛОВИЕ ЗАДАЧИ:\n"
        f"Весь бассейн принят за 100%\n"
        f"Производительность 1-й (P1) = {p1}%/ч\n"
        f"Производительность 2-й (P2) = {p2}%/ч\n\n"
        f"МАТЕМАТИКА ДЕЙСТВИЯ:\n"
        f"Совместная скорость работы:\n"
        f"P_общая = P1 + P2\n"
        f"P_общая = {p1} + ({p2}) = {p_total}%/ч\n\n"
        f"ТЕКУЩИЙ СТАТУС:\n"
        f"Прошло времени (t) = {t:.1f} ч\n"
        f"Уровень воды = {current_volume:.1f}%\n"
        f"Формула: V = P_общая * t\n"
        f"V = {p_total} * {t:.1f} = {p_total*t:.1f}%\n\n"
        f"РЕШЕНИЕ И ОТВЕТ:\n"
        f"Формула времени: t = 100% / P_общая\n"
        f"{status_msg}"
    )
    
    if t >= t_full and t_full != float('inf'):
        text_content += "\n\n🎉 БАССЕЙН ПОЛНОСТЬЮ НАПОЛНЕН!"
    elif current_volume == 0 and p_total < 0 and t > 0:
        text_content += "\n\n🚰 БАССЕЙН ПУСТ (ВСЁ ВЫЛИЛОСЬ)"
        
    info_text.set_text(text_content)
    fig.canvas.draw_idle()

# Привязываем функции обновления к ползункам
slider_t.on_changed(update)
slider_p1.on_changed(update)
slider_p2.on_changed(update)

# Первичный запуск отрисовки
update(None)

# Переводим в стандартный режим ожидания
plt.ioff()
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons
from matplotlib.patches import Rectangle

# Отключаем предупреждения для стабильности интерфейса
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Настройка шрифта для русского языка
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# Включаем интерактивный режим
plt.ion()

# --- МАТЕМАТИЧЕСКАЯ ФУНКЦИЯ РАСЧЕТА ---
def calculate_pool_state(t, p1, p2, p3, use_p3, init_vol, use_init_vol):
    # Определяем реальную начальную воду
    v0 = init_vol if use_init_vol else 0.0
    
    # Считаем суммарную производительность открытых труб
    p_total = p1 + p2
    if use_p3:
        p_total += p3
        
    # Формула объема: V(t) = V0 + P * t
    # Но бассейн ограничен рамками от 0% до 100%
    if p_total > 0:
        t_full = (100.0 - v0) / p_total
        t_empty = float('inf')
    elif p_total < 0:
        t_full = float('inf')
        t_empty = v0 / abs(p_total)
    else:
        t_full = float('inf')
        t_empty = float('inf')
        
    # Вычисляем текущий объем для конкретного времени t
    if p_total > 0 and t >= t_full:
        current_volume = 100.0
    elif p_total < 0 and t >= t_empty:
        current_volume = 0.0
    else:
        current_volume = v0 + p_total * t
        
    # На всякий случай жестко страхуем границы
    current_volume = np.clip(current_volume, 0.0, 100.0)
    
    return p_total, v0, t_full, t_empty, current_volume

# --- ИНТЕРФЕЙС И ГРАФИКА ---

class InteractivePool:
    def __init__(self):
        # Огромное окно для наглядности (15 на 8)
        self.fig, (self.ax_pool, self.ax_graph) = plt.subplots(1, 2, figsize=(15, 8), gridspec_kw={'width_ratios': [1, 1.4]})
        plt.subplots_adjust(left=0.06, bottom=0.32, right=0.74, wspace=0.3)
        
        # Начальные настройки элементов
        self.p1, self.p2, self.p3 = 15.0, 10.0, -10.0
        self.init_vol = 30.0
        self.use_p3 = False
        self.use_init_vol = False
        
        # --- 1. Настройка бассейна (Слева) ---
        self.ax_pool.set_xlim(-1, 5)
        self.ax_pool.set_ylim(-10, 110)
        self.ax_pool.axis('off')
        self.ax_pool.set_title("Анимация бассейна", fontsize=13, fontweight='bold', pad=15)
        
        # Каркас бассейна
        pool_frame = Rectangle((0, 0), 4, 100, edgecolor='dimgray', facecolor='#e6f2ff', lw=3, zorder=1)
        self.ax_pool.add_patch(pool_frame)
        
        # Синяя вода
        self.water_patch = Rectangle((0, 0), 4, 0, edgecolor='none', facecolor='#3399ff', alpha=0.8, zorder=2)
        self.ax_pool.add_patch(self.water_patch)
        
        # Линия начального уровня (желтый пунктир)
        self.init_vol_line = self.ax_pool.axhline(-100, color='gold', ls='--', lw=2, zorder=3)
        
        # Текстовые подписи к трубам
        self.t1_text = self.ax_pool.text(0.3, 105, '', color='blue', fontsize=10, fontweight='bold')
        self.t2_text = self.ax_pool.text(2.0, 105, '', color='darkgreen', fontsize=10, fontweight='bold', ha='center')
        self.t3_text = self.ax_pool.text(3.7, 105, '', color='crimson', fontsize=10, fontweight='bold', ha='right')
        
        # --- 2. Настройка графика (Справа) ---
        self.ax_graph.set_xlim(0, 10)
        self.ax_graph.set_ylim(0, 110)
        self.ax_graph.set_xlabel("Время работы, t (в часах)", fontsize=10)
        self.ax_graph.set_ylabel("Заполненность бассейна (в %)", fontsize=10)
        self.ax_graph.grid(True, linestyle=':', alpha=0.6)
        self.ax_graph.set_title("График работы (V = V0 + P*t)", fontsize=13, fontweight='bold', pad=15)
        
        self.ax_graph.axhline(100, color='red', ls='--', lw=1.5, label='100% (Заполнен)')
        self.graph_line, = self.ax_graph.plot([], [], 'b-', lw=2.5, label='Объем воды')
        self.time_marker = self.ax_graph.axvline(0, color='purple', ls=':', lw=1.5)
        self.time_point, = self.ax_graph.plot([], [], 'ro', mfc='white', ms=8)
        
        # Панель вывода текста (сдвинута вплотную к правому краю 1.02)
        self.info_text = self.ax_graph.text(1.02, 0.95, '', transform=self.ax_graph.transAxes, 
                                           verticalalignment='top', fontsize=10.5,
                                           bbox=dict(facecolor='#f9f9f9', alpha=0.95, edgecolor='gray'))
        
        # --- 3. Создание ползунков (Sliders) ---
        ax_color = '#f5f5f5'
        self.ax_slider_t   = plt.axes([0.15, 0.22, 0.45, 0.02], facecolor=ax_color)
        self.ax_slider_p1  = plt.axes([0.15, 0.17, 0.45, 0.02], facecolor=ax_color)
        self.ax_slider_p2  = plt.axes([0.15, 0.12, 0.45, 0.02], facecolor=ax_color)
        self.ax_slider_p3  = plt.axes([0.15, 0.07, 0.45, 0.02], facecolor=ax_color)
        self.ax_slider_v0  = plt.axes([0.15, 0.02, 0.45, 0.02], facecolor=ax_color)
        
        self.slider_t   = Slider(self.ax_slider_t, 'Время (ч)', 0.0, 10.0, valinit=0.0, valstep=0.1)
        self.slider_p1  = Slider(self.ax_slider_p1, 'Труба 1 (%/ч)', 0.0, 40.0, valinit=self.p1, valstep=1)
        self.slider_p2  = Slider(self.ax_slider_p2, 'Труба 2 (%/ч)', -30.0, 40.0, valinit=self.p2, valstep=1)
        self.slider_p3  = Slider(self.ax_slider_p3, 'Труба 3 (%/ч)', -40.0, 40.0, valinit=self.p3, valstep=1)
        self.slider_v0  = Slider(self.ax_slider_v0, 'Нач. вода V0 (%)', 0.0, 90.0, valinit=self.init_vol, valstep=5)
        
        self.slider_t.on_changed(self.update)
        self.slider_p1.on_changed(self.update)
        self.slider_p2.on_changed(self.update)
        self.slider_p3.on_changed(self.update)
        self.slider_v0.on_changed(self.update)
        
        # --- 4. Создание Галочек (Включение модулей) ---
        # Размещаем галочки чуть правее ползунков, чтобы они стояли ровно в ряд
        ax_check = plt.axes([0.65, 0.02, 0.25, 0.12], facecolor='#f0f0f0')
        self.check_labels = ['Включить Трубу 3', 'Бассейн частично заполнен']
        self.check_buttons = CheckButtons(ax_check, self.check_labels, [False, False])
        self.check_buttons.on_clicked(self.toggle_features)
        
        self.update(None)

    def toggle_features(self, label):
        if label == 'Включить Трубу 3':
            self.use_p3 = not self.use_p3
        elif label == 'Бассейн частично заполнен':
            self.use_init_vol = not self.use_init_vol
        self.update(None)

    def update(self, val):
        t = self.slider_t.val
        p1 = self.slider_p1.val
        p2 = self.slider_p2.val
        p3 = self.slider_p3.val
        init_vol = self.slider_v0.val
        
        # Считаем математику процесса через внешнюю функцию
        p_total, v0, t_full, t_empty, current_volume = calculate_pool_state(
            t, p1, p2, p3, self.use_p3, init_vol, self.use_init_vol
        )
        
        # 1. Визуализируем воду и трубы в бассейне
        self.water_patch.set_height(current_volume)
        
        # Показывать или прятать линию стартовой воды V0
        if self.use_init_vol:
            self.init_vol_line.set_ydata([v0, v0])
            self.ax_slider_v0.set_visible(True) # делаем активным сам ползунок V0
        else:
            self.init_vol_line.set_ydata([-100, -100]) # прячем далеко вниз
            self.ax_slider_v0.set_visible(False)
            
        # Текстовые статусы труб над бассейном
        self.t1_text.set_text(f"Труба 1:\n+{p1}%/ч")
        self.t2_text.set_text(f"Труба 2:\n+{p2}%/ч" if p2 >= 0 else f"Труба 2 (СЛИВ):\n{p2}%/ч")
        self.t2_text.set_color('darkgreen' if p2 >= 0 else 'crimson')
        
        if self.use_p3:
            self.t3_text.set_text(f"Труба 3:\n+{p3}%/ч" if p3 >= 0 else f"Труба 3 (СЛИВ):\n{p3}%/ч")
            self.t3_text.set_color('darkgreen' if p3 >= 0 else 'crimson')
            self.ax_slider_p3.set_visible(True)
        else:
            self.t3_text.set_text("")
            self.ax_slider_p3.set_visible(False)
            
        # 2. Обновляем кривую на графике
        t_points = np.linspace(0, max(t, 10), 200)
        v_points = v0 + p_total * t_points
        v_points = np.clip(v_points, 0, 100)
        self.graph_line.set_data(t_points, v_points)
        
        self.time_marker.set_xdata([t, t])
        self.time_point.set_data([t], [current_volume])
        
        # 3. Текстовое сопровождение задачи
        pipe3_str = f" + P3 ({p3})" if self.use_p3 else ""
        pipe3_val_str = f" + ({p3 if p3<0 else p3})" if self.use_p3 else ""
        
        status_msg = "Вода не движется"
        if p_total > 0:
            status_msg = f"До полного бака (100%):\nч = {t_full:.2f} ч"
        elif p_total < 0:
            status_msg = f"До полного слива (0%):\nч = {t_empty:.2f} ч"
            
        text_content = (
            f"УСЛОВИЕ ЗАДАЧИ:\n"
            f"Полный бассейн = 100%\n"
            f"Начальный объем V0 = {v0:.0f}%\n"
            f"P1 = {p1}%/ч | P2 = {p2}%/ч\n"
            f"P3 = {p3}%/ч ({'ВКЛ' if self.use_p3 else 'ВЫКЛ'})\n\n"
            
            f"МАТЕМАТИКА РАБОТЫ:\n"
            f"Формула скорости:\n"
            f"P_общ = P1 + P2{pipe3_str}\n"
            f"P_общ = {p1} + ({p2}){pipe3_val_str}\n"
            f"P_общ = {p_total}%/ч\n\n"
            
            f"ТЕКУЩИЙ СТАТУС (t = {t:.1f} ч):\n"
            f"Формула: V = V0 + P_общ * t\n"
            f"V = {v0:.0f} + ({p_total}) * {t:.1f}\n"
            f"Текущий объем = {current_volume:.1f}%\n\n"
            
            f"ОТВЕТ И РЕШЕНИЕ:\n"
            f"{status_msg}"
        )
        
        if p_total > 0 and t >= t_full:
            text_content += "\n\n🎉 БАССЕЙН ПОЛНОСТЬЮ НАПОЛНЕН!"
        elif p_total < 0 and current_volume == 0 and t > 0:
            text_content += "\n\n🚰 БАССЕЙН ПОЛНОСТЬЮ ПУСТ!"
            
        self.info_text.set_text(text_content)
        self.fig.canvas.draw_idle()

if __name__ == '__main__':

    plt.ion()
    app = InteractivePool()
    plt.ioff()
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Отключаем лишние предупреждения для стабильности интерфейса
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Настройка шрифта для русского языка
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# Включаем интерактивный режим
plt.ion()

# --- МАТЕМАТИЧЕСКИЙ РАСЧЕТ ДВИЖЕНИЯ ---
def calculate_river_motion(t, v_boat, v_river, s_turn):
    # Скорости катера на разных участках
    v_with_river = v_boat + v_river     # По течению
    v_against_river = v_boat - v_river  # Против течения
    
    # Время, за которое катер доплывет до точки разворота (S_turn)
    t_turn = s_turn / v_with_river
    
    # 1. Положение плота в любой момент времени t (он плывет всегда со скоростью реки)
    pos_raft = v_river * t
    
    # 2. Положение катера
    if t <= t_turn:
        # Катер плывет ТУДА (по течению)
        pos_boat = v_with_river * t
        is_returning = False
    else:
        # Катер плывет ОБРАТНО (против течения)
        time_back = t - t_turn
        pos_boat = s_turn - v_against_river * time_back
        # Катер не должен уплыть левее нуля (старта)
        pos_boat = max(pos_boat, 0.0)
        is_returning = True
        
    # 3. Расчет математической точки встречи на обратном пути
    # Уравнение: V_теч * t = S_разворота - (V_собств - V_теч) * (t - t_разворота)
    # После упрощения: t_встречи = (S_разворота + (V_собств - V_теч) * t_разворота) / V_собств
    t_meet = (s_turn + (v_boat - v_river) * t_turn) / v_boat
    pos_meet = v_river * t_meet
    
    # Если текущее время вышло за точку встречи, фиксируем их вместе
    if t >= t_meet:
        pos_raft = pos_meet
        pos_boat = pos_meet
        
    return t_turn, t_meet, pos_meet, pos_raft, pos_boat, v_with_river, v_against_river

# --- ИНТЕРФЕЙС И ГРАФИКА ---

class RiverSimulation:
    def __init__(self):
        # Настройка оконного пространства
        self.fig, (self.ax_river, self.ax_graph) = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [1, 2.2]})
        plt.subplots_adjust(left=0.08, bottom=0.22, right=0.74, hspace=0.35)
        
        # Начальные параметры задачи
        self.v_boat_init = 25.0    # Собственная скорость катера (км/ч)
        self.v_river_init = 5.0    # Скорость течения / плота (км/ч)
        self.s_turn_init = 80.0    # Точка разворота катера (км)
        
        # --- 1. Настройка Верхнего графика (Река) ---
        self.ax_river.set_xlim(-5, 105)
        self.ax_river.set_ylim(-1, 2)
        self.ax_river.axis('off')
        self.ax_river.set_title("Движение на реке (Течение направлено ВПРАВО ->)", fontsize=12, fontweight='bold')
        
        # Рисуем линии берегов и течения
        self.ax_river.axhline(1.5, color='lightblue', lw=40, alpha=0.3) # Русло реки
        self.ax_river.axhline(0.8, color='gray', ls=':', lw=1, alpha=0.5) # Разделитель дорожек
        
        # Объекты на реке (Плот - коричневый квадрат, Катер - синий треугольник)
        self.raft_marker, = self.ax_river.plot([], [], 's', color='saddlebrown', markersize=14, label='Плот')
        self.boat_marker, = self.ax_river.plot([], [], '>', color='blue', markersize=14, label='Катер')
        
        # Текстовые подписи объектов прямо на реке
        self.raft_label = self.ax_river.text(0, 1.15, 'Плот', color='saddlebrown', fontweight='bold', ha='center')
        self.boat_label = self.ax_river.text(0, 0.15, 'Катер', color='blue', fontweight='bold', ha='center')
        
        # Рисуем флажок в точке разворота
        self.turn_flag = self.ax_river.axvline(self.s_turn_init, color='crimson', ls='-', lw=1.5)
        self.turn_text = self.ax_river.text(self.s_turn_init, 1.8, 'Разворот', color='crimson', ha='center', fontsize=9)
        
        # --- 2. Настройка Нижнего графика (Координатная сетка t и S) ---
        self.ax_graph.set_xlim(0, 6) # Максимум 6 часов
        self.ax_graph.set_ylim(0, 105)
        self.ax_graph.set_xlabel("Время движения, t (в часах)", fontsize=10)
        self.ax_graph.set_ylabel("Пройденный путь от старта, S (в км)", fontsize=10)
        self.ax_graph.grid(True, linestyle=':', alpha=0.6)
        self.ax_graph.set_title("Графическое решение задачи", fontsize=12, fontweight='bold')
        
        # Траектории на графике
        self.graph_raft, = self.ax_graph.plot([], [], color='saddlebrown', lw=2, label='Траектория ПЛОТА')
        self.graph_boat, = self.ax_graph.plot([], [], color='blue', lw=2.5, label='Траектория КАТЕРА')
        
        # Маркер текущего времени (вертикальный фиолетовый пунктир)
        self.time_marker = self.ax_graph.axvline(0, color='purple', ls=':', lw=1.5)
        self.raft_point, = self.ax_graph.plot([], [], 'o', color='saddlebrown', ms=6)
        self.boat_point, = self.ax_graph.plot([], [], 'ob', mfc='white', ms=7)
        
        self.ax_graph.legend(loc='upper left', fontsize=9)
        
        # Панель вывода текста справа
        self.info_text = self.ax_graph.text(1.03, 0.95, '', transform=self.ax_graph.transAxes, 
                                           verticalalignment='top', fontsize=10.5,
                                           bbox=dict(facecolor='#f9f9f9', alpha=0.95, edgecolor='gray'))
        
        # --- 3. Создание ползунков (Sliders) ---
        ax_color = '#f5f5f5'
        self.ax_slider_t     = plt.axes([0.15, 0.14, 0.5, 0.025], facecolor=ax_color)
        self.ax_slider_vboat = plt.axes([0.15, 0.09, 0.5, 0.025], facecolor=ax_color)
        self.ax_slider_vriv  = plt.axes([0.15, 0.04, 0.5, 0.025], facecolor=ax_color)
        
        self.slider_t     = Slider(self.ax_slider_t, 'Время (ч)', 0.0, 6.0, valinit=0.0, valstep=0.05)
        self.slider_vboat = Slider(self.ax_slider_vboat, 'V катера собств.', 10.0, 45.0, valinit=self.v_boat_init, valstep=1)
        self.slider_vriv  = Slider(self.ax_slider_vriv, 'V течения (плота)', 1.0, 10.0, valinit=self.v_river_init, valstep=0.5)
        
        self.slider_t.on_changed(self.update)
        self.slider_vboat.on_changed(self.update)
        self.slider_vriv.on_changed(self.update)
        
        self.update(None)

    def update(self, val):
        t = self.slider_t.val
        v_boat = self.slider_vboat.val
        v_river = self.slider_vriv.val
        s_turn = self.s_turn_init # Фиксируем точку разворота на 80 км для стабильности визуализации
        
        # Математический расчет
        t_turn, t_meet, pos_meet, pos_raft, pos_boat, v_with, v_against = calculate_river_motion(
            t, v_boat, v_river, s_turn
        )
        
        # 1. Обновляем анимацию на реке
        self.raft_marker.set_data([pos_raft], [0.8])
        self.raft_label.set_position((pos_raft, 1.15))
        
        self.boat_marker.set_data([pos_boat], [0.3])
        self.boat_label.set_position((pos_boat, -0.05))
        
        # Меняем направление стрелочки катера в зависимости от того, плывет он туда или обратно
        if t <= t_turn:
            self.boat_marker.set_marker('>') # плывет вправо
        else:
            self.boat_marker.set_marker('<') # плывет влево
            
        # 2. Обновляем графики линий путей
        # Линия плота (всегда прямая до момента встречи)
        t_points_raft = np.linspace(0, t_meet, 100)
        self.graph_raft.set_data(t_points_raft, v_river * t_points_raft)
        
        # Линия катера (кусочно-линейная ломаная)
        t_points_boat = np.linspace(0, t_meet, 200)
        v_points_boat = np.zeros_like(t_points_boat)
        for i, tp in enumerate(t_points_boat):
            if tp <= t_turn:
                v_points_boat[i] = v_with * tp
            else:
                v_points_boat[i] = s_turn - v_against * (tp - t_turn)
        self.graph_boat.set_data(t_points_boat, v_points_boat)
        
        # Двигаем фиолетовый маркер времени и точки
        self.time_marker.set_xdata([t, t])
        self.raft_point.set_data([t], [pos_raft])
        self.boat_point.set_data([t], [pos_boat])
        
        # 3. Формируем текстовую панель с формулами
        text_content = (
            f"УСЛОВИЕ ЗАДАЧИ:\n"
            f"V собств. катера = {v_boat} км/ч\n"
            f"V течения (плота) = {v_river} км/ч\n"
            f"Пункт разворота = {s_turn} км\n\n"
            
            f"СКОРОСТИ ДВИЖЕНИЯ:\n"
            f"Плот (только река) = {v_river} км/ч\n"
            f"Катер ПО течению:\n"
            f"V1 = Vсобств + Vтеч = {v_with} км/ч\n"
            f"Катер ПРОТИВ течения:\n"
            f"V2 = Vсобств - Vтеч = {v_against} км/ч\n\n"
            
            f"ТЕКУЩИЙ СТАТУС (t = {t:.2f} ч):\n"
            f"Плот проплыл = {pos_raft:.1f} км\n"
            f"Катер находится = {pos_boat:.1f} км\n"
            f"{'Катер плывет ОБРАТНО' if t > t_turn else 'Катер плывет ТУДА'}\n\n"
            
            f"МАТЕМАТИКА РЕШЕНИЯ:\n"
            f"Время катера ТУДА:\n"
            f"t1 = {s_turn} / {v_with} = {t_turn:.2f} ч\n"
            f"Уравнение встречи ОБРАТНО:\n"
            f"Vтеч*t = Sразв - Vпротив*(t - t1)\n\n"
            
            f"ОТВЕТ ЗАДАЧИ:\n"
            f"Время встречи = {t_meet:.2f} ч\n"
            f"Встреча на отметке = {pos_meet:.1f} км"
        )
        
        if t >= t_meet:
            text_content += "\n\n🎉 КАТЕР ДОГНАЛ ПЛОТ!"
            
        self.info_text.set_text(text_content)
        self.fig.canvas.draw_idle()

if __name__ == '__main__':
    app = RiverSimulation()
    plt.ioff()
    plt.show()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Rectangle

# Настройка шрифта для русского языка
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# Включаем интерактивный режим
plt.ion()

# --- ИНТЕРФЕЙС И ГРАФИКА ---

class MixtureSimulation:
    def __init__(self):
        # Создаем широкое окно для наглядности
        self.fig, self.ax = plt.subplots(figsize=(14, 7.5))
        plt.subplots_adjust(left=0.06, bottom=0.28, right=0.72, top=0.9)
        
        self.ax.set_xlim(-1, 14)
        self.ax.set_ylim(-10, 110)
        self.ax.axis('off')
        self.ax.set_title("Лаборатория текстовых задач: Смеси и Растворы", fontsize=14, fontweight='bold', pad=15)
        
        # --- Стартовые параметры ---
        self.m1_init, self.w1_init = 200.0, 10.0  # Сосуд 1: 200г, 10%
        self.m2_init, self.w2_init = 300.0, 60.0  # Сосуд 2: 300г, 60%
        
        # --- Рисуем каркасы сосудов (Серые стаканы) ---
        # Стакан 1 (слева)
        self.ax.add_patch(Rectangle((0.5, 0), 2.5, 100, edgecolor='dimgray', facecolor='none', lw=2.5, zorder=1))
        self.ax.text(1.75, 103, "Сосуд 1", fontsize=11, fontweight='bold', ha='center', color='#b38600')
        
        # Стакан 2 (справа)
        self.ax.add_patch(Rectangle((10.0, 0), 2.5, 100, edgecolor='dimgray', facecolor='none', lw=2.5, zorder=1))
        self.ax.text(11.25, 103, "Сосуд 2", fontsize=11, fontweight='bold', ha='center', color='darkblue')
        
        # Стакан 3 (Смесь посередине, он шире)
        self.ax.add_patch(Rectangle((4.5, 0), 4.5, 100, edgecolor='black', facecolor='none', lw=3, zorder=1))
        self.ax.text(6.75, 103, "ИТОГОВАЯ СМЕСЬ", fontsize=12, fontweight='bold', ha='center', color='darkgreen')
        
        # --- Заготовки для жидкостей (Изначально пустые прямоугольники) ---
        # Жидкость 1 (Желтоватая)
        self.fluid1 = Rectangle((0.5, 0), 2.5, 0, edgecolor='none', zorder=2)
        self.ax.add_patch(self.fluid1)
        
        # Жидкость 2 (Синеватая)
        self.fluid2 = Rectangle((10.0, 0), 2.5, 0, edgecolor='none', zorder=2)
        self.ax.add_patch(self.fluid2)
        
        # Жидкость 3 (Результат смешивания — зеленоватая)
        self.fluid3 = Rectangle((4.5, 0), 4.5, 0, edgecolor='none', zorder=2)
        self.ax.add_patch(self.fluid3)
        
        # Текстовые метки процентов прямо на стаканах
        self.txt_w1 = self.ax.text(1.75, 50, '', ha='center', va='center', fontsize=12, fontweight='bold', color='black', zorder=3)
        self.txt_w2 = self.ax.text(11.25, 50, '', ha='center', va='center', fontsize=12, fontweight='bold', color='white', zorder=3)
        self.txt_w3 = self.ax.text(6.75, 50, '', ha='center', va='center', fontsize=14, fontweight='bold', color='black', zorder=3)
        
        # Текстовая панель уравнений справа (1.02 прижимает к краю)
        self.info_text = self.ax.text(1.02, 0.95, '', transform=self.ax.transAxes, 
                                           verticalalignment='top', fontsize=10.5,
                                           bbox=dict(facecolor='#f9f9f9', alpha=0.95, edgecolor='gray'))
        
        # --- Ползунки управления ---
        ax_color = '#f5f5f5'
        self.ax_m1 = plt.axes([0.15, 0.19, 0.45, 0.025], facecolor=ax_color)
        self.ax_w1 = plt.axes([0.15, 0.14, 0.45, 0.025], facecolor=ax_color)
        self.ax_m2 = plt.axes([0.15, 0.09, 0.45, 0.025], facecolor=ax_color)
        self.ax_w2 = plt.axes([0.15, 0.04, 0.45, 0.025], facecolor=ax_color)
        
        self.slider_m1 = Slider(self.ax_m1, 'Масса M1 (г)', 50.0, 500.0, valinit=self.m1_init, valstep=10)
        self.slider_w1 = Slider(self.ax_w1, 'Кислота W1 (%)', 0.0, 100.0, valinit=self.w1_init, valstep=5)
        self.slider_m2 = Slider(self.ax_m2, 'Масса M2 (г)', 50.0, 500.0, valinit=self.m2_init, valstep=10)
        self.slider_w2 = Slider(self.ax_w2, 'Кислота W2 (%)', 0.0, 100.0, valinit=self.w2_init, valstep=5)
        
        self.slider_m1.on_changed(self.update)
        self.slider_w1.on_changed(self.update)
        self.slider_m2.on_changed(self.update)
        self.slider_w2.on_changed(self.update)
        
        self.update(None)

    def update(self, val):
        # Получаем значения с ползунков
        m1 = self.slider_m1.val
        w1 = self.slider_w1.val
        m2 = self.slider_m2.val
        w2 = self.slider_w2.val
        
        # --- Математический расчет смеси ---
        # 1. Считаем массу чистой кислоты в каждом сосуде
        pure_acid1 = m1 * (w1 / 100.0)
        pure_acid2 = m2 * (w2 / 100.0)
        
        # 2. Итоговые параметры смеси
        m_total = m1 + m2
        pure_acid_total = pure_acid1 + pure_acid2
        w_total = (pure_acid_total / m_total) * 100.0
        
        # --- Визуальное отображение уровней жидкостей ---
        # Максимальный объем стакана рассчитан на 500г. Переводим массу в высоту стакана (0-100)
        h1 = (m1 / 500.0) * 100
        h2 = (m2 / 500.0) * 100
        # Итоговый стакан шире, его высота — это среднее заполнение относительно максимума в 1000г
        h3 = (m_total / 1000.0) * 100
        
        self.fluid1.set_height(h1)
        self.fluid2.set_height(h2)
        self.fluid3.set_height(h3)
        
        # --- Управление динамическим цветом (RGBA) ---
        # Сосуд 1: желтый цвет. Насыщенность (альфа-канал) зависит от концентрации кислоты
        alpha1 = np.clip(w1 / 100.0, 0.1, 0.9) if w1 > 0 else 0.05
        self.fluid1.set_facecolor((1.0, 0.8, 0.0, alpha1))
        
        # Сосуд 2: синий цвет. Насыщенность зависит от кислоты
        alpha2 = np.clip(w2 / 100.0, 0.1, 0.9) if w2 > 0 else 0.05
        self.fluid2.set_facecolor((0.0, 0.3, 1.0, alpha2))
        
        # Итоговый сосуд 3: зеленый цвет (смесь желтого и синего).
        # Тон зеленого цвета зависит от того, какого раствора по массе или концентрации больше
        green_tone = np.clip(w_total / 100.0, 0.1, 0.9)
        self.fluid3.set_facecolor((0.1, 0.7, 0.2, green_tone))
        
        # Двигаем текстовые метки процентов вслед за уровнем жидкостей
        self.txt_w1.set_position((1.75, h1 / 2 if h1 > 15 else 10))
        self.txt_w1.set_text(f"{w1:.0f}%" if w1 > 0 else "Вода")
        
        self.txt_w2.set_position((11.25, h2 / 2 if h2 > 15 else 10))
        self.txt_w2.set_text(f"{w2:.0f}%" if w2 > 0 else "Вода")
        
        self.txt_w3.set_position((6.75, h3 / 2 if h3 > 15 else 10))
        self.txt_w3.set_text(f"{w_total:.1f}%")
        
        # --- Формируем разбор задачи на правой панели ---
        text_content = (
            f"КОМПОНЕНТЫ ЗАДАЧИ:\n"
            f"---------------------------\n"
            f"Раствор 1:\n"
            f"Масса (M1) = {m1:.0f} г\n"
            f"Концентрация (W1) = {w1:.0f}%\n"
            f"Чистая кислота = {m1:.0f} * {w1/100:.2f} = {pure_acid1:.1f} г\n\n"
            
            f"Раствор 2:\n"
            f"Масса (M2) = {m2:.0f} г\n"
            f"Концентрация (W2) = {w2:.0f}%\n"
            f"Чистая кислота = {m2:.0f} * {w2/100:.2f} = {pure_acid2:.1f} г\n\n"
            
            f"ЛОГИКА СОСТАВЛЕНИЯ УРАВНЕНИЯ:\n"
            f"---------------------------\n"
            f"1. Итоговая масса смеси:\n"
            f"M_общ = M1 + M2\n"
            f"M_общ = {m1:.0f} + {m2:.0f} = {m_total:.0f} г\n\n"
            
            f"2. Итоговая масса кислоты:\n"
            f"Кислота_общ = Кислота1 + Кислота2\n"
            f"Кислота_общ = {pure_acid1:.1f} + {pure_acid2:.1f} = {pure_acid_total:.1f} г\n\n"
            
            f"3. Вычисление концентрации:\n"
            f"W_итог = (Кислота_общ / M_общ) * 100%\n"
            f"W_итог = ({pure_acid_total:.1f} / {m_total:.0f}) * 100%\n\n"
            
            f"ОТВЕТ ЗАДАЧИ:\n"
            f"Концентрация смеси = {w_total:.2f}%"
        )
        self.info_text.set_text(text_content)
        self.fig.canvas.draw_idle()

if __name__ == '__main__':
    app = MixtureSimulation()
    plt.ioff()
    plt.show()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons

# Отключаем лишние предупреждения для стабильности интерфейса
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Настройка шрифта для русского языка
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# Включаем интерактивный режим
plt.ion()

class TrigonometrySimulation:
    def __init__(self):
        # Создаем окно: слева тригонометрический круг, справа - развертка графиков
        self.fig, (self.ax_circle, self.ax_graph) = plt.subplots(1, 2, figsize=(15, 7.5), 
                                                                 gridspec_kw={'width_ratios': [1, 1.4]})
        plt.subplots_adjust(left=0.06, bottom=0.28, right=0.74, wspace=0.3)
        
        # Переменные видимости функций (по умолчанию включены синус и косинус)
        self.show_sin = True
        self.show_cos = True
        self.show_tan = False
        self.show_ctg = False
        
        # --- 1. Настройка Левого графика (Тригонометрический круг) ---
        self.ax_circle.set_xlim(-2.2, 2.2)
        self.ax_circle.set_ylim(-2.2, 2.2)
        self.ax_circle.set_aspect('equal')
        self.ax_circle.grid(True, linestyle=':', alpha=0.5)
        self.ax_circle.set_title("Тригонометрический круг", fontsize=12, fontweight='bold')
        
        # Главные оси координат на круге
        self.ax_circle.axhline(0, color='black', lw=1.2)
        self.ax_circle.axvline(0, color='black', lw=1.2)
        
        # Рисуем единичную окружность
        theta = np.linspace(0, 2*np.pi, 200)
        self.ax_circle.plot(np.cos(theta), np.sin(theta), color='gray', lw=1.5, ls='--')
        
        # Линия тангенсов (x = 1) и котангенсов (y = 1)
        self.tan_axis = self.ax_circle.axvline(1, color='orange', lw=1.5, ls=':', visible=False)
        self.ctg_axis = self.ax_circle.axhline(1, color='purple', lw=1.5, ls=':', visible=False)
        
        # Графические элементы на круге
        self.radius_line, = self.ax_circle.plot([], [], color='black', lw=2.5, marker='o', mfc='white') # Стрелка-радиус
        self.sin_line_c, = self.ax_circle.plot([], [], color='red', lw=3, label='Синус (Y)')             # Отрезок синуса
        self.cos_line_c, = self.ax_circle.plot([], [], color='royalblue', lw=3, label='Косинус (X)')        # Отрезок косинуса
        self.tan_line_c, = self.ax_circle.plot([], [], color='orange', lw=3, visible=False, label='Тангенс') # Отрезок тангенса
        self.ctg_line_c, = self.ax_circle.plot([], [], color='purple', lw=3, visible=False, label='Котангенс')# Отрезок котангенса
        
        # --- 2. Настройка Правого графика (Развёртка во времени/углах) ---
        self.ax_graph.set_xlim(0, 360)
        self.ax_graph.set_ylim(-2.2, 2.2)
        self.ax_graph.set_xticks([0, 90, 180, 270, 360])
        self.ax_graph.set_xticklabels(['0°', '90° (π/2)', '180° (π)', '270° (3π/2)', '360° (2π)'])
        self.ax_graph.grid(True, linestyle=':', alpha=0.6)
        self.ax_graph.set_title("Графики функций", fontsize=12, fontweight='bold')
        self.ax_graph.axhline(0, color='black', lw=1)
        
        # Волны графиков
        self.angles_range = np.linspace(0, 360, 360)
        self.rad_range = np.radians(self.angles_range)
        
        self.graph_sin, = self.ax_graph.plot(self.angles_range, np.sin(self.rad_range), color='red', lw=2, label='Синусоида')
        self.graph_cos, = self.ax_graph.plot(self.angles_range, np.cos(self.rad_range), color='royalblue', lw=2, label='Косинусоида')
        
        # Тангенс и котангенс имеют разрывы, сглаживаем их для красивого графика
        tan_y = np.tan(self.rad_range)
        tan_y[abs(tan_y) > 5] = np.nan
        ctg_y = 1 / np.tan(self.rad_range)
        ctg_y[abs(ctg_y) > 5] = np.nan
        
        self.graph_tan, = self.ax_graph.plot(self.angles_range, tan_y, color='orange', lw=2, visible=False, label='Тангенсоида')
        self.graph_ctg, = self.ax_graph.plot(self.angles_range, ctg_y, color='purple', lw=2, visible=False, label='Котангенсоида')
        
        # Вертикальная линия текущего угла и точки на графиках
        self.angle_marker = self.ax_graph.axvline(0, color='black', ls=':', lw=1.5)
        self.dot_sin, = self.ax_graph.plot([], [], 'ro', ms=7)
        self.dot_cos, = self.ax_graph.plot([], [], 'ob', ms=7)
        self.dot_tan, = self.ax_graph.plot([], [], 'o', color='orange', ms=7, visible=False)
        self.dot_ctg, = self.ax_graph.plot([], [], 'o', color='purple', ms=7, visible=False)
        
        self.ax_graph.legend(loc='upper right', fontsize=8)
        
        # Информационная панель справа (1.02 прижимает к краю экрана)
        self.info_text = self.ax_graph.text(1.02, 0.95, '', transform=self.ax_graph.transAxes, 
                                           verticalalignment='top', fontsize=11,
                                           bbox=dict(facecolor='#f9f9f9', alpha=0.95, edgecolor='gray'))
        
        # --- 3. Ползунок угла ---
        ax_color = '#f5f5f5'
        self.ax_slider_alpha = plt.axes([0.15, 0.16, 0.45, 0.03], facecolor=ax_color)
        self.slider_alpha = Slider(self.ax_slider_alpha, 'Угол α (градусы)', 0.0, 360.0, valinit=30.0, valstep=1)
        self.slider_alpha.on_changed(self.update)
        
        # --- 4. Кнопки-галочки управления видимостью функций ---
        ax_check = plt.axes([0.15, 0.02, 0.45, 0.11], facecolor='#f0f0f0')
        self.check_labels = ['Показать Синус (Красный)', 'Показать Косинус (Синий)', 
                             'Показать Тангенс (Оранжевый)', 'Показать Котангенс (Фиолетовый)']
        self.check_buttons = CheckButtons(ax_check, self.check_labels, [True, True, False, False])
        self.check_buttons.on_clicked(self.toggle_features)
        
        self.update(None)

    def toggle_features(self, label):
        if 'Синус' in label: self.show_sin = not self.show_sin
        elif 'Косинус' in label: self.show_cos = not self.show_cos
        elif 'Тангенс' in label: self.show_tan = not self.show_tan
        elif 'Котангенс' in label: self.show_ctg = not self.show_ctg
        self.update(None)

    def update(self, val):
        alpha = self.slider_alpha.val
        rad = np.radians(alpha)
        
        # Расчет базовых значений тригонометрии
        sin_val = np.sin(rad)
        cos_val = np.cos(rad)
        
        # Тангенс и котангенс с защитой от деления на 0
        tan_val = np.tan(rad) if abs(cos_val) > 0.001 else float('inf')
        ctg_val = 1 / np.tan(rad) if abs(sin_val) > 0.001 else float('inf')
        
        # Координаты движущейся точки на окружности
        x_p, y_p = cos_val, sin_val
        
        # 1. Обновление левого чертежа (Круг)
        self.radius_line.set_data([0, x_p], [0, y_p])
        
        # Синус (Вертикальный отрезок)
        self.sin_line_c.set_data([x_p, x_p], [0, y_p])
        self.sin_line_c.set_visible(self.show_sin)
        
        # Косинус (Горизонтальный отрезок на оси X)
        self.cos_line_c.set_data([0, x_p], [0, 0])
        self.cos_line_c.set_visible(self.show_cos)
        
        # Тангенс (Отрезок на касательной x=1)
        self.tan_axis.set_visible(self.show_tan)
        if self.show_tan and abs(cos_val) > 0.001:
            self.tan_line_c.set_data([1, 1], [0, tan_val])
            self.tan_line_c.set_visible(True)
        else:
            self.tan_line_c.set_visible(False)
            
        # Котангенс (Отрезок на касательной y=1)
        self.ctg_axis.set_visible(self.show_ctg)
        if self.show_ctg and abs(sin_val) > 0.001:
            self.ctg_line_c.set_data([0, ctg_val], [1, 1])
            self.ctg_line_c.set_visible(True)
        else:
            self.ctg_line_c.set_visible(False)
            
        # 2. Обновление правого чертежа (Графики волн)
        self.graph_sin.set_visible(self.show_sin)
        self.graph_cos.set_visible(self.show_cos)
        self.graph_tan.set_visible(self.show_tan)
        self.graph_ctg.set_visible(self.show_ctg)
        
        self.angle_marker.set_xdata([alpha, alpha])
        
        # Точки на графиках волн
        if self.show_sin:
            self.dot_sin.set_data([alpha], [sin_val])
            self.dot_sin.set_visible(True)
        else: self.dot_sin.set_visible(False)
            
        if self.show_cos:
            self.dot_cos.set_data([alpha], [cos_val])
            self.dot_cos.set_visible(True)
        else: self.dot_cos.set_visible(False)
            
        if self.show_tan and abs(cos_val) > 0.001 and abs(tan_val) < 2.2:
            self.dot_tan.set_data([alpha], [tan_val])
            self.dot_tan.set_visible(True)
        else: self.dot_tan.set_visible(False)
            
        if self.show_ctg and abs(sin_val) > 0.001 and abs(ctg_val) < 2.2:
            self.dot_ctg.set_data([alpha], [ctg_val])
            self.dot_ctg.set_visible(True)
        else: self.dot_ctg.set_visible(False)
        
        # 3. Текстовое сопровождение на панели
        tan_str = f"{tan_val:.3f}" if abs(cos_val) > 0.001 else "не сущ. (деление на 0)"
        ctg_str = f"{ctg_val:.3f}" if abs(sin_val) > 0.001 else "не сущ. (деление на 0)"
        
        text_content = (
            f"ТЕКУЩИЙ УГОЛ α = {alpha:.0f}°\n"
            f"Радианы = {rad:.3f} rad\n"
            f"---------------------------\n"
            f"ЗНАЧЕНИЯ ФУНКЦИЙ:\n\n"
            f"Синус (Высота точки Y):\n"
            f"sin({alpha:.0f}°) = {sin_val:.3f}\n\n"
            f"Косинус (Длина по X):\n"
            f"cos({alpha:.0f}°) = {cos_val:.3f}\n\n"
            f"Тангенс (sin / cos):\n"
            f"tg({alpha:.0f}°) = {tan_str}\n\n"
            f"Котангенс (cos / sin):\n"
            f"ctg({alpha:.0f}°) = {ctg_str}\n"
            f"---------------------------\n"
            f"ЧЕТВЕРТЬ: {int(alpha // 90) + 1 if alpha < 360 else 4}-я"
        )
        self.info_text.set_text(text_content)
        self.fig.canvas.draw_idle()
if __name__ == '__main__':
    app = TrigonometrySimulation()   
    plt.ioff()       
    plt.show()     
