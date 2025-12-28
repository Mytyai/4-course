import asyncio
import ssl
import json
import datetime

async def echo_server_handler(reader, writer):
    peer = writer.get_extra_info("peername")
    print(f"Connection from {peer}")
    try:
        while True:
            header = await reader.readexactly(4)
            length = int.from_bytes(header, "big")
            data = await reader.readexactly(length)
            msg = json.loads(data.decode("utf-8"))
            print("Received:", msg)
            response = {"echo": msg, "ts": datetime.datetime.now().isoformat()}
            resp_bytes = json.dumps(response).encode("utf-8")
            writer.write(len(resp_bytes).to_bytes(4, "big") + resp_bytes)
            await writer.drain()
    except asyncio.IncompleteReadError:
        print("Client disconnected")
    finally:
        writer.close()
        await writer.wait_closed()

async def main(host="127.0.0.1", port=8888, certfile="server.crt", keyfile="server.key"):
    sslctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslctx.load_cert_chain(certfile=certfile, keyfile=keyfile)
    server = await asyncio.start_server(echo_server_handler, host, port, ssl=sslctx)
    print(f"Serving on {host}:{port} (SSL)")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped")
