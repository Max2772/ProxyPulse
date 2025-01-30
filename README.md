<h1 align="center">ProxyPulse - Parsing/Checker 🔥</h1>
<p align="center">
<img src="https://img.shields.io/badge/made%20by-TishkaPon-blue.svg" >
<img src="https://img.shields.io/badge/python-3.12.8-green.svg">
<img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103" >
</p>

<p align="center">
<img src="https://media.giphy.com/media/lXUaP7DEl6AZfkKbyZ/giphy.gif">
</p>


# Installation
`pip install -U git+https://github.com/TishkaPon/ProxyPulse.git`

# Requirements
`pip install -r requirements.txt`

# Base code
```python
from FinderProxy import FreeProxy
from CheckProxy import CheckerProxy
import asyncio

# Find
finder = FreeProxy()
proxies = asyncio.run(finder.get_proxy(logging=True))

print("find " + str(len(proxies)) + " proxy !")

# Check
checker = CheckerProxy()
working_proxies = asyncio.run(checker.CheckProxies(proxies, logging=True))

print("find " + str(len(working_proxies)) + " working proxy !")
```

# Attribute
# Class Finder():
```
ass - list
```
# Class Checker():
```
ass - list
```
