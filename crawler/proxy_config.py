# crawler/proxy_config.py
import os

def get_proxy():
    # Priority: explicit env HTTP_PROXY/HTTPS_PROXY, else custom provider
    proxy = os.getenv('HTTPS_PROXY') or os.getenv('HTTP_PROXY')
    if proxy:
        return proxy
    # Fallback example: rotate from a small static list (for demo only)
    proxies = [
        "http://user:pass@proxy1:10000",
        "http://user:pass@proxy2:10000",
    ]
    # simple rotation
    from random import choice
    return choice(proxies)