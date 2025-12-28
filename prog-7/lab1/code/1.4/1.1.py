import asyncio
import datetime

async def show_time_loop():
    try:
        while True:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Завершение 1.1")

if __name__ == "__main__":
    try:
        asyncio.run(show_time_loop())
    except KeyboardInterrupt:
        print("\nCtrl+C — выход")

