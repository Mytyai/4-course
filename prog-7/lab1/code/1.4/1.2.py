import asyncio
import datetime
from termcolor import colored
from pynput import keyboard

stop_event = asyncio.Event()

async def print_time():
    color_idx = 0
    colors = ["red","green","yellow","blue","magenta","cyan","white"]
    while not stop_event.is_set():
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(colored(f"\r{now}", colors[color_idx % len(colors)]), end="", flush=True)
        color_idx += 1
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=1.0)
        except asyncio.TimeoutError:
            pass
    print("\r" + " " * 60 + "\r", end="", flush=True)

def on_press(key):
    if key == keyboard.Key.esc:
        asyncio.get_event_loop().call_soon_threadsafe(stop_event.set)
        return False

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    asyncio.run(print_time())
    listener.stop()