import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector
import requests

class CheckerProxy:
    def __init__(self):
        self.savedProxy = None

    async def _check_socks(self, proxy: str, timeout: float, anonymity: bool):
        ip = proxy.split("//")[-1].split(":")[0]
        if anonymity:
            CHECK_URL = 'http://httpbin.org/ip'
        else:
            CHECK_URL = 'http://httpbin.io/ip'

        try:
            connector = ProxyConnector.from_url(proxy, ssl=False)  # SOCKS4/SOCKS5 прокси

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(CHECK_URL, timeout=timeout) as response:
                    if response.status == 200:
                        result = await response.json()
                        if anonymity:
                            if ip in result['origin'] and "," not in result['origin']:
                                return proxy
                        else:
                            return proxy


        except Exception as e:
            return None

    async def _check_http(self, session, proxy, timeout, anonymity):
        ip = proxy.split("//")[-1].split(":")[0]
        if anonymity:
            CHECK_URL = 'http://httpbin.org/ip'
        else:
            CHECK_URL = 'http://httpbin.io/ip'
        try:
            async with session.get(CHECK_URL, proxy=proxy, timeout=timeout) as response:
                if response.status == 200:
                    result = await response.json()

                    if anonymity:
                        if ip in result['origin'] and "," not in result['origin']:
                            return proxy
                    else:
                        return proxy


        except Exception as e:
            pass
        return None

    async def CheckProxies(self, proxies, timeout=3, anonymity=False, saved=False):
        tasks = []
        session_http = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        session_http._ssl = False
        for proxy in proxies:
            if proxy.startswith("http"):
                tasks.append(self._check_http(session=session_http, proxy=proxy, timeout=timeout, anonymity=anonymity))
            elif proxy.startswith("socks"):
                tasks.append(self._check_socks(proxy=proxy, timeout=timeout, anonymity=anonymity))

        results = await asyncio.gather(*tasks)
        await session_http.close()

        working_proxies = [proxy for proxy in results if proxy]
        if saved:
            self.savedProxy = working_proxies
        return working_proxies
