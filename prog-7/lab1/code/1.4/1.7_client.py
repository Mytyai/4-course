import asyncio
import ssl
import json
import datetime

async def main(host="127.0.0.1", port=8888, cafile=None):
    sslctx = ssl.create_default_context(cafile=cafile) if cafile else ssl._create_unverified_context()
    reader, writer = await asyncio.open_connection(host, port, ssl=sslctx)
    print("Connected to server. Type messages; Ctrl+D/Enter to quit.")

    async def recv_loop():
        try:
            while True:
                header = await reader.readexactly(4)
                length = int.from_bytes(header, "big")
                data = await reader.readexactly(length)
                msg = json.loads(data.decode("utf-8"))
                print("Server:", json.dumps(msg, ensure_ascii=False))
        except asyncio.IncompleteReadError:
            print("Server closed connection")

    recv_task = asyncio.create_task(recv_loop())

    loop = asyncio.get_event_loop()
    try:
        while True:
            user = await loop.run_in_executor(None, input, "> ")
            payload = {"text": user, "ts": datetime.datetime.now().isoformat()}
            b = json.dumps(payload).encode("utf-8")
            writer.write(len(b).to_bytes(4, "big") + b)
            await writer.drain()
    except (EOFError, KeyboardInterrupt):
        print("\nClient exiting")
    finally:
        recv_task.cancel()
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient stopped")
