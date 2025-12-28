import asyncio
import aiohttp
import json

class AsyncScraperCtx:
    def __init__(self, max_concurrency=5, timeout=10):
        self.max_concurrency = max_concurrency
        self.timeout = timeout
        self._session = None
        self._sem = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        self._sem = asyncio.Semaphore(self.max_concurrency)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._session.close()
        self._session = None
        self._sem = None

    async def _fetch(self, url):
        async with self._sem:
            try:
                async with self._session.get(url, timeout=self.timeout) as resp:
                    text = await resp.text()
                    return {"url": url, "status": resp.status, "len": len(text), "snippet": text[:200]}
            except Exception as e:
                return {"url": url, "error": str(e)}

    async def crawl(self, urls):
        tasks = [asyncio.create_task(self._fetch(u)) for u in urls]
        return await asyncio.gather(*tasks)

async def main(file_path="urls.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return

    async with AsyncScraperCtx(max_concurrency=4) as scraper:
        results = await scraper.crawl(urls)
        for r in results:
            print(json.dumps(r, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())