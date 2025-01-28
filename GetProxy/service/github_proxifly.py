import aiohttp
import asyncio
from fake_useragent import UserAgent
from rich.progress import Progress

ua = UserAgent()


class Proxifly:
    _list_fields = {"country", "protocol", "port"}

    def __init__(self, country=None, protocol=None, anonymity=None, port=None, logging=False):
        self.country = country
        self.protocol = protocol
        self.anonymity = anonymity
        self.port = port
        self.proxies = []
        self.semaphore = asyncio.Semaphore(100)  # Ограничиваем число одновременных запросов
        self.logging = logging

        if self.logging:
            self.progress = Progress()
            self.task = self.progress.add_task("GitHub-Proxifly", total=1)

    def __setattr__(self, name, value):
        if name in self._list_fields and not isinstance(value, list) and value is not None:
            value = [value]
        super().__setattr__(name, value)


    async def filtered_proxy(self, proxies):
        filtered_proxy = []

        for proxy in proxies:
            if proxy["protocol"] == "http":
                if proxy["https"]:
                    proxy["protocol"] = "https"

            # Пункты прокси, если все == True, то проходят
            protocol_proxy = False
            port_proxy = False
            anonymity_proxy = False
            geolocation_proxy = False

            if self.protocol is not None:
                if proxy["protocol"] in self.protocol:
                    protocol_proxy = True
            else:
                protocol_proxy = True

            if self.country is not None:
                if proxy["geolocation"]["country"] in self.country:
                    geolocation_proxy = True
            else:
                geolocation_proxy = True

            if self.port is not None:
                if proxy["port"] in self.port:
                    port_proxy = True
            else:
                port_proxy = True

            if self.anonymity:
                if proxy["anonymity"] != "transparent":
                    anonymity_proxy = True
            else:
                anonymity_proxy = True

            if protocol_proxy and port_proxy and anonymity_proxy and geolocation_proxy:
                filtered_proxy.append(proxy['proxy'])


        return filtered_proxy

    async def get_proxy(self):
        url = f"https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.json"
        connector = aiohttp.TCPConnector(ssl=False, limit=0, limit_per_host=100, ttl_dns_cache=300)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                proxies = await self.filtered_proxy(proxies=await response.json())
                if self.logging:
                    with self.progress:
                        self.progress.update(self.task, advance=1)

        return proxies
