import asyncio
import datetime
import json

async def task_a(n):
    await asyncio.sleep(0.1 * n)
    return {"task":"A","n":n,"ts":datetime.datetime.now().isoformat()}

async def task_b(text,n):
    await asyncio.sleep(0.2*n)
    return {"task":"B","text":text,"n":n,"ts":datetime.datetime.now().isoformat()}

async def main():
    for i in range(1,6):
        results = await asyncio.gather(task_a(i), task_b("hello",i))
        print(f"Iteration {i}")
        for r in results:
            print(json.dumps(r, ensure_ascii=False))
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())