import threading
import requests
import random
from queue import Queue
from urllib.request import urlretrieve

# 1.1 Создание нескольких потоков и вывод их имён

print("1.1 Потоки и их имена")

def worker():
    print(f"Поток запущен: {threading.current_thread().name}")

threads = []
for i in range(5):
    t = threading.Thread(target=worker, name=f"Thread-{i}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# 1.2 Загрузка файлов с использованием потоков

print("\n1.2 Многопоточная загрузка файлов")

urls = [
        "https://httpbin.org/image/png",
        "https://httpbin.org/image/jpeg",
        "https://httpbin.org/image/webp",
    ]

def download(url, idx):
    print(f"Начало загрузки {url}")
    filename = f"image_{idx}"
    urlretrieve(url, filename)
    print(f"Файл загружен: {filename}")

threads = []
for i, url in enumerate(urls):
    t = threading.Thread(target=download, args=(url, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# 1.3 Одновременные HTTP-запросы (requests + Thread)

print("\n1.3 Одновременные HTTP-запросы")

urls = [
    "https://httpbin.org/get",
    "https://httpbin.org/uuid",
    "https://httpbin.org/delay/1",
]

lock = threading.Lock()

def fetch(url):
    response = requests.get(url)
    with lock:
        print(f"{url} → статус {response.status_code}")

threads = []
for url in urls:
    t = threading.Thread(target=fetch, args=(url,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# 1.4 Вычисление факториала с использованием потоков

print("\n1.4 Факториал с использованием потоков")

n = 10
result = [1]
lock = threading.Lock()

def multiply(start, end):
    local = 1
    for i in range(start, end + 1):
        local *= i
    with lock:
        result[0] *= local

mid = n // 2
t1 = threading.Thread(target=multiply, args=(1, mid))
t2 = threading.Thread(target=multiply, args=(mid + 1, n))

t1.start()
t2.start()
t1.join()
t2.join()

print(f"{n}! = {result}")

# 1.5 Многопоточная быстрая сортировка

print("\n1.5 Многопоточная быстрая сортировка")

def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left, middle, right = [], [], []

    for x in arr:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            middle.append(x)

    left_sorted = []
    right_sorted = []

    def sort_left():
        nonlocal left_sorted
        left_sorted = quicksort(left)

    def sort_right():
        nonlocal right_sorted
        right_sorted = quicksort(right)

    t1 = threading.Thread(target=sort_left)
    t2 = threading.Thread(target=sort_right)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return left_sorted + middle + right_sorted

data = [random.randint(0, 100) for _ in range(20)]
print("Исходный массив:", data)
sorted_data = quicksort(data)
print("Отсортированный массив:", sorted_data)
