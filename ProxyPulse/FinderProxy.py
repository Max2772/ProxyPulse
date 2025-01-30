from service.hidexh import Hidexh
from service.github_proxifly import Proxifly
from service.proxyfreeonly import Proxyfreeonly
import numpy as np
from tqdm.asyncio import tqdm
import asyncio

TypeHttps = "https"
TypeHttp = "http"
TypeSocks4 = "socks4"
TypeSocks5 = "socks5"

class FreeProxy:
    def __init__(self):
        self.saved = None

    async def get_proxy(self, country=None, protocol=None, anonymity=None, port=None, logging=False):
        hidexh = Hidexh(country=country, protocol=protocol, anonymity=anonymity, port=port, ReadPage=16)
        proxifly = Proxifly(country=country, protocol=protocol, anonymity=anonymity, port=port)
        proxyfreeonly = Proxyfreeonly(country=country, protocol=protocol, anonymity=anonymity, port=port)

        tasks = [
            hidexh.get_proxy(),
            proxifly.get_proxy(),
            proxyfreeonly.get_proxy()
        ]

        if logging:
            proxies = await tqdm.gather(*tasks)
        else:
            proxies = await asyncio.gather(*tasks)

        self.saved = proxies

        return list(set(np.hstack(proxies)))



