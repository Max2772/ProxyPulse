from ProxyPulse.FinderProxy import FreeProxy
from ProxyPulse.CheckProxy import CheckerProxy
import asyncio

# Find
finder = FreeProxy()
proxies = asyncio.run(finder.get_proxy(logging=True))

print("find " + str(len(proxies)) + " proxy !")

# Check
checker = CheckerProxy()
working_proxies = asyncio.run(checker.CheckProxies(proxies, logging=True, anonymity=True))

print("find " + str(len(working_proxies)) + " working proxy !")
