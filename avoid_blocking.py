import random
import time

def get_random_delay():
    return random.randint(3, 10)  # فترات عشوائية بين 3-10 دقائق

def get_random_proxy():
    proxies = [
        {"server": "http://proxy1.example.com:8080"},
        {"server": "http://proxy2.example.com:8080"},
        None  # لا استخدام Proxy
    ]
    return random.choice(proxies)
