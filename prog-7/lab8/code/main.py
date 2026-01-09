import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch

# ----------------------------------------------
# Задача 1: Оптимизация производства электроники
# ----------------------------------------------

c = [-8000, -12000]  # отрицательные для минимизации в linprog

# Ограничения: A_ub @ x <= b_ub
A_ub = [
    [2, 3],   # процессорное время
    [4, 6],   # оперативная память
    [1, 2]    # аккумуляторы
]
b_ub = [240, 480, 150]

# Границы переменных (неотрицательность)
bounds = [(0, None), (0, None)]

# Решение задачи
result1 = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

print("=== Задача оптимизации производства электроники ===")
print(f"Статус: {result1.message}")
if result1.success:
    x1_opt, x2_opt = result1.x
    max_profit = -result1.fun
    print(f"Оптимальное количество смартфонов: {x1_opt:.2f}")
    print(f"Оптимальное количество планшетов: {x2_opt:.2f}")
    print(f"Максимальная прибыль: {max_profit:.2f} руб")

# Визуализация допустимой области и линий уровня целевой функции
x1_vals = np.linspace(0, 150, 400)
x2_constraint1 = (240 - 2*x1_vals)/3
x2_constraint2 = (480 - 4*x1_vals)/6
x2_constraint3 = (150 - 1*x1_vals)/2

plt.figure(figsize=(10, 8))
plt.plot(x1_vals, x2_constraint1, label='Процессорное время')
plt.plot(x1_vals, x2_constraint2, label='Память')
plt.plot(x1_vals, x2_constraint3, label='Аккумуляторы')

# Закрашивание допустимой области
from matplotlib.patches import Polygon

x2_max = np.minimum(np.minimum(x2_constraint1, x2_constraint2), x2_constraint3)
vertices = []
for i in range(len(x1_vals)):
    if x2_max[i] >= 0:
        vertices.append((x1_vals[i], x2_max[i]))
vertices.append((0,0))
poly = Polygon(vertices, facecolor='lightblue', alpha=0.4)
plt.gca().add_patch(poly)

# Оптимальная точка
plt.plot(x1_opt, x2_opt, 'ro', label='Оптимум')

# Линии уровня целевой функции
profit_levels = [-500000, -600000, -700000]
for P in profit_levels:
    y = ( -P/1000 - 8000*x1_vals)/12000
    plt.plot(x1_vals, y, 'k--', alpha=0.3)

plt.xlabel('x1 (смартфоны)')
plt.ylabel('x2 (планшеты)')
plt.title('Оптимизация производства электроники')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# -------------------------------------------
# Задача 2: Оптимизация снабжения военных баз
# -------------------------------------------

# Переменные: [x11, x12, x13, x21, x22, x23]
c2 = [8, 6, 10, 9, 7, 5]  # Стоимости перевозки

# Ограничения равенства A_eq @ x = b_eq
A_eq = [
    [1,1,1,0,0,0],  # Склад 1
    [0,0,0,1,1,1],  # Склад 2
    [1,0,0,1,0,0],  # База Альфа
    [0,1,0,0,1,0],  # База Бета
    [0,0,1,0,0,1],  # База Гамма
]
b_eq = [150, 250, 120, 180, 100]

bounds2 = [(0, None)]*6

# Решение задачи
result2 = linprog(c2, A_eq=A_eq, b_eq=b_eq, bounds=bounds2, method='highs')

print("\n=== Транспортная задача снабжения военных баз ===")
print(f"Статус: {result2.message}")
if result2.success:
    x_opt = result2.x
    print("Оптимальный план перевозок:")
    routes = ['Склад1->Альфа', 'Склад1->Бета', 'Склад1->Гамма',
              'Склад2->Альфа', 'Склад2->Бета', 'Склад2->Гамма']
    for r, val in zip(routes, x_opt):
        print(f"{r}: {val:.2f} тонн")
    print(f"Минимальная общая стоимость: {result2.fun:.2f} у.е.")

# Визуализация сетевой диаграммы
fig, ax = plt.subplots(figsize=(14,10))
warehouses = {'Склад 1': (2,8), 'Склад 2': (2,3)}
bases = {'Альфа': (10,10), 'Бета': (10,5.5), 'Гамма': (10,1)}

# Рисуем склады
for w, (x,y) in warehouses.items():
    ax.add_patch(plt.Rectangle((x-0.5,y-0.5),1,1,facecolor='lightgreen'))
    ax.text(x, y, w, ha='center', va='center', fontsize=12)

# Рисуем базы
for b, (x,y) in bases.items():
    ax.add_patch(plt.Rectangle((x-0.5,y-0.5),1,1,facecolor='lightcoral'))
    ax.text(x, y, b, ha='center', va='center', fontsize=12)

# Рисуем потоки
flows = [
    ('Склад 1','Альфа', x_opt[0]),
    ('Склад 1','Бета', x_opt[1]),
    ('Склад 1','Гамма', x_opt[2]),
    ('Склад 2','Альфа', x_opt[3]),
    ('Склад 2','Бета', x_opt[4]),
    ('Склад 2','Гамма', x_opt[5]),
]

for from_node, to_node, val in flows:
    if val > 0:
        x_start, y_start = warehouses[from_node] if 'Склад' in from_node else bases[from_node]
        x_end, y_end = bases[to_node] if to_node in bases else warehouses[to_node]
        arrow = FancyArrowPatch((x_start,y_start),(x_end,y_end),
                                arrowstyle='->', mutation_scale=15,
                                linewidth=val/20, color='blue')
        ax.add_patch(arrow)
        ax.text((x_start+x_end)/2, (y_start+y_end)/2, f"{val:.0f}", color='blue')

ax.set_xlim(0,12)
ax.set_ylim(0,12)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Оптимальный план снабжения военных баз', fontsize=16, fontweight='bold')
plt.show()
