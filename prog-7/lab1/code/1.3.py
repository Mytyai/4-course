import math
import timeit
import threading
import multiprocessing
import os
import fnmatch
from urllib.request import urlretrieve
from concurrent.futures import ThreadPoolExecutor, Future
from threading import Lock, RLock, Event, Semaphore, Barrier
from time import sleep

# 2.1 Замеры времени (последовательно / потоки / процессы)

def integrate(f, a, b, *, n_iter=10**6):
    h = (b - a) / n_iter
    s = 0.0
    x = a
    for _ in range(n_iter):
        s += f(x)
        x += h
    return s * h


def integrate_threaded(n_threads):
    threads = []
    lock = Lock()
    result = [0.0]
    n_iter = 10**6
    h = (math.pi / 2) / n_iter
    chunk = n_iter // n_threads

    def worker(start):
        local = 0.0
        x = start * h
        for _ in range(chunk):
            local += math.atan(x)
            x += h
        with lock:
            result[0] += local

    for i in range(n_threads):
        t = threading.Thread(target=worker, args=(i * chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return result[0] * h

def integrate_process(_):
    return integrate(math.atan, 0, math.pi / 2, n_iter=10**6)

def task_2_1():
    print("\n2.1 Timeit benchmark (msec)")

    for n in (2, 4, 6):
        t = timeit.repeat(
            stmt=lambda: integrate_threaded(n),
            repeat=100,
            number=1
        )
        print(f"Threads={n}: {min(t)*1000:.2f} ms")

    for n in (2, 4, 6):
        with multiprocessing.Pool(n) as p:
            t = timeit.repeat(
                stmt=lambda: p.map(integrate_process, range(n)),
                repeat=100,
                number=1
            )
        print(f"Processes={n}: {min(t)*1000:.2f} ms")

# 2.2 Банк с Lock

class BankAccount:
    def __init__(self):
        self.balance = 0
        self.lock = Lock()

    def deposit(self, amount):
        with self.lock:
            self.balance += amount

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount

def task_2_2():
    print("\n2.2 Bank simulation")
    acc = BankAccount()

    def worker():
        for _ in range(1000):
            acc.deposit(10)
            acc.withdraw(10)

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Final balance:", acc.balance)

# 2.3 Future + Semaphore (загрузка изображений)

def task_2_3():
    print("\n2.3 Async download with Future")

    urls = [
        "https://httpbin.org/image/png",
        "https://httpbin.org/image/jpeg",
        "https://httpbin.org/image/webp",
    ]

    sem = Semaphore(2)

    def download(url, idx):
        with sem:
            filename = f"img_{idx}"
            urlretrieve(url, filename)
            return filename

    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = [ex.submit(download, url, i) for i, url in enumerate(urls)]
        for f in futures:
            print("Downloaded:", f.result())

# 2.4 Запись / чтение файла с Future

def task_2_4():
    print("\n2.4 File read/write with Future")

    filename = "data.txt"

    def write_file():
        with open(filename, "w") as f:
            f.write("Hello from writer")

    def read_file():
        with open(filename, "r") as f:
            return f.read()

    with ThreadPoolExecutor() as ex:
        fw = ex.submit(write_file)
        fw.result()
        fr = ex.submit(read_file)
        print("Read:", fr.result())

# 2.5 Event

def task_2_5():
    print("\n2.5 Event")

    event = Event()

    def setter():
        sleep(3)
        event.set()

    def waiter():
        event.wait()
        print("Event occurred")

    def checker():
        while not event.is_set():
            print("Event did not occur")
            sleep(1)

    threading.Thread(target=setter).start()
    threading.Thread(target=waiter).start()
    threading.Thread(target=checker).start()

# 2.6 Queue + RLock

class SafeQueue:
    def __init__(self):
        self.data = []
        self.lock = RLock()

    def push(self, item):
        with self.lock:
            self.data.append(item)

    def pop(self):
        with self.lock:
            if self.data:
                return self.data.pop(0)

def task_2_6():
    print("\n2.6 Queue with RLock")
    q = SafeQueue()

    def worker():
        for i in range(5):
            q.push(i)
            sleep(0.1)
            print("Popped:", q.pop())

    threading.Thread(target=worker).start()

# 2.7 Server / Client + Barrier

def task_2_7():
    print("\n2.7 Barrier")

    barrier = Barrier(2)

    def server():
        print("Server ready")
        barrier.wait()

    def client():
        barrier.wait()
        print("Client sent request")

    threading.Thread(target=server).start()
    threading.Thread(target=client).start()

# 2.8 Параллельный поиск файла

def task_2_8():
    print("\n2.8 Parallel file search")

    root = "."
    pattern = "*.py"
    found = Event()
    lock = Lock()

    def search(files):
        for f in files:
            if found.is_set():
                return
            if fnmatch.fnmatch(f, pattern):
                with lock:
                    if not found.is_set():
                        print("Found:", f)
                        found.set()

    files = os.listdir(root)
    mid = len(files) // 2

    t1 = threading.Thread(target=search, args=(files[:mid],))
    t2 = threading.Thread(target=search, args=(files[mid:],))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

# Вызов

if __name__ == "__main__":
    task_2_1()
    task_2_2()
    task_2_3()
    task_2_4()
    task_2_5()
    sleep(5)
    task_2_6()
    task_2_7()
    task_2_8()
