from service.hidexh import Hidexh
from service.github_proxifly import Proxifly
from service.proxyfreeonly import Proxyfreeonly
import numpy as np

TypeHttps = "https"
TypeHttp = "http"
TypeSocks4 = "socks4"
TypeSocks5 = "socks5"


class FreeProxy:
    def __init__(self):
        self.saved = None

    async def get_proxy(self, country=None, protocol=None, anonymity=None, port=None, logging=True):
        hidexh = Hidexh(country=country, protocol=protocol, anonymity=anonymity, port=port, ReadPage=16, logging=logging)
        proxifly = Proxifly(country=country, protocol=protocol, anonymity=anonymity, port=port, logging=logging)
        proxyfreeonly = Proxyfreeonly(country=country, protocol=protocol, anonymity=anonymity, port=port, logging=logging)

        proxies = []

        proxies.append(await hidexh.get_proxy())
        proxies.append(await proxifly.get_proxy())
        proxies.append(await proxyfreeonly.get_proxy())

        self.saved = proxies
        if logging:
            print("----- Парсинг прокси завершен -----")


        return np.hstack(proxies)
