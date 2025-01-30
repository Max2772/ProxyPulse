import aiohttp
import asyncio
from fake_useragent import UserAgent

ua = UserAgent()


class Proxyfreeonly:
    _list_fields = {"country", "protocol", "port"}

    def __init__(self, country=None, protocol=None, anonymity=None, port=None):
        self.country = country
        self.protocol = protocol
        self.anonymity = anonymity
        self.port = port
        self.proxies = []
        self.semaphore = asyncio.Semaphore(100)  # Ограничиваем число одновременных запросов


    def __setattr__(self, name, value):
        if name in self._list_fields and not isinstance(value, list) and value is not None:
            value = [value]
        super().__setattr__(name, value)


    async def filtered_proxy(self, proxies):
        filtered_proxy = []
        any_in = lambda a, b: any(i in b for i in a)

        for proxy in proxies:
            # Пункты прокси, если все == True, то проходят
            protocol_proxy = False
            port_proxy = False
            anonymity_proxy = False
            geolocation_proxy = False

            if self.protocol is not None:
                if any_in(proxy['protocols'], self.protocol):
                    protocol_proxy = True
            else:
                protocol_proxy = True

            if self.port is not None:
                if proxy["port"] in self.port:
                    port_proxy = True
            else:
                port_proxy = True

            if self.anonymity:
                if proxy['anonymityLevel'] != "transparent":
                    anonymity_proxy = True
            else:
                anonymity_proxy = True

            if self.country is not None:
                if proxy["country"] in self.country:
                    geolocation_proxy = True
            else:
                geolocation_proxy = True

            if protocol_proxy and port_proxy and anonymity_proxy and geolocation_proxy:
                for protocol in proxy['protocols']:
                    proxy_url = f"{protocol}://{proxy['ip']}{proxy['port']}"
                    filtered_proxy.append(proxy_url)


        return filtered_proxy

    async def get_proxy(self):
        url = f"https://proxyfreeonly.com/api/free-proxy-list"
        connector = aiohttp.TCPConnector(ssl=False, limit=0, limit_per_host=100, ttl_dns_cache=300)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                proxies = await self.filtered_proxy(proxies=await response.json())

        return proxies
