import math
import threading
import timeit

# Последовательное интегрирование

def integrate(f, a, b, *, n_iter=1000):
    h = (b - a) / n_iter
    result = 0.0
    x = a

    for _ in range(n_iter):
        result += f(x)
        x += h

    return result * h

def integrate2(f, a, b, n_iter=1000):
    h = (b - a) / n_iter
    result = 0.0
    x = a

    for _ in range(n_iter):
        result += f(x)
        x += h

    return result * h

# Многопоточное интегрирование (Thread + Lock)

def integrate_threaded(f, a, b, *, n_iter=1000, n_threads=4):
    h = (b - a) / n_iter
    total_sum = 0.0
    lock = threading.Lock()

    def worker(start_i, end_i):
        nonlocal total_sum
        local_sum = 0.0
        x = a + start_i * h

        for _ in range(start_i, end_i):
            local_sum += f(x)
            x += h

        with lock:
            total_sum += local_sum

    threads = []
    chunk = n_iter // n_threads

    for i in range(n_threads):
        start = i * chunk
        end = n_iter if i == n_threads - 1 else (i + 1) * chunk
        t = threading.Thread(target=worker, args=(start, end))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return total_sum * h

# Замеры времени

def benchmark():
    print("Последовательное интегрирование")
    for n in (10**4, 10**5, 10**6):
        t = timeit.timeit(
            stmt=f"integrate(math.sin, 0, 1, n_iter={n})",
            globals=globals(),
            number=1
        )
        print(f"n_iter={n:<7} time={t:.6f} sec")

    print("\nМногопоточное интегрирование (4 потока)")
    for n in (10**4, 10**5, 10**6):
        t = timeit.timeit(
            stmt=f"integrate_threaded(math.sin, 0, 1, n_iter={n}, n_threads=4)",
            globals=globals(),
            number=1
        )
        print(f"n_iter={n:<7} time={t:.6f} sec")

# Вызов

if __name__ == "__main__":
    print("integrate(sin, 0, 1, n_iter=100) = ", integrate(math.sin, 0, 1, n_iter=100))
    print("integrate2(cos, 0, 1, 100) = ", integrate2(math.cos, 0, 1, 100))
    print("integrate_threaded(sin, 0, 1) = ", integrate_threaded(math.sin, 0, 1))

    print("\n")
    benchmark()
