import asyncio
import aiohttp
import asyncpg
import json
import datetime

WEB_SERVER_URL = "https://rnacentral.org/api/v1/rna/"
DB_CONNECTION_STRING = "postgres://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"

async def fetch_rna(session, rna_id):
    async with session.get(WEB_SERVER_URL + rna_id) as resp:
        text = await resp.text()
        try:
            return json.dumps(json.loads(text), indent=2, ensure_ascii=False)
        except Exception:
            return text[:400]

async def query_db():
    conn = await asyncpg.connect(DB_CONNECTION_STRING)
    try:
        rows = await conn.fetch("SELECT now() AS now")
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def main(rna_id="URS00007553"):
    async with aiohttp.ClientSession() as session:
        http_coro = fetch_rna(session, rna_id)
        db_coro = query_db()
        http_res, db_res = await asyncio.gather(http_coro, db_coro)
        print("HTTP result:", http_res[:1000])
        print("DB result:", db_res)

if __name__ == "__main__":
    asyncio.run(main())
