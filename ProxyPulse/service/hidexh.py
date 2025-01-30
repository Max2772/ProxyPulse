import aiohttp
import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()


class Hidexh:
    _list_fields = {"country", "protocol", "port"}

    def __init__(self, country=None, protocol=None, anonymity=None, port=None, ReadPage=1):
        self.country = country
        self.protocol = protocol
        self.anonymity = anonymity
        self.port = port
        self.ReadPage = ReadPage
        self.proxies = []
        self.semaphore = asyncio.Semaphore(100)  # Ограничиваем число одновременных запросов

    def __setattr__(self, name, value):
        if name in self._list_fields and not isinstance(value, list) and value is not None:
            value = [value]
        super().__setattr__(name, value)

    async def create_url(self, start):
        params = {
            "country": ''.join(self.country) if self.country else '',
            "ports": ','.join(map(str, self.port)) if self.port else '',
            "type": ''.join(self.protocol) if self.protocol else '',
            "anon": "234" if self.anonymity is True else "1" if self.anonymity is False else None,
            "start": start
        }
        url = "https://hidexh.name/proxy-list/?" + '&'.join(f"{key}={value}" for key, value in params.items() if value)
        return url + "#list"

    async def fetch_page(self, session, url):
        async with self.semaphore:
            headers = {'User-Agent': ua.random, "Accept-Encoding": "gzip"}
            async with session.get(url, headers=headers, timeout=10) as response:
                html = await response.text()

                return html

    async def parse_proxies(self, html):
        soup = BeautifulSoup(html, 'lxml')
        rows = soup.select('tbody tr')

        proxies = []
        for row in rows:
            columns = row.find_all('td')

            ip = columns[0].text.strip()
            port = columns[1].text.strip()
            protocol = columns[4].text.strip().lower()

            proxies.append(f"{protocol}://{ip}:{port}")


        return proxies


    async def get_proxy(self):
        tasks = []
        connector = aiohttp.TCPConnector(ssl=False, limit=0, limit_per_host=100, ttl_dns_cache=300)
        async with aiohttp.ClientSession(connector=connector) as session:
            for page in range(self.ReadPage):
                url = await self.create_url(page * 64)
                tasks.append(asyncio.create_task(self.fetch_page(session, url)))


            responses = await asyncio.gather(*tasks)

            proxy_lists = await asyncio.gather(*(self.parse_proxies(html) for html in responses))

            proxies = [proxy for sublist in proxy_lists for proxy in sublist]
            return proxies

