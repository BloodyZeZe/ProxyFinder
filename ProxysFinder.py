import requests
from bs4 import BeautifulSoup
import time
import random
import json
import concurrent.futures
import os
from datetime import datetime
import sys
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init()

# ANSI color codes for hacker-style terminal output
class TermColors:
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL
    BRIGHT = Style.BRIGHT

# Advanced User-Agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.89 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Vivaldi/6.6",
    "Mozilla/5.0 (Android 13; Mobile; rv:122.0) Gecko/122.0 Firefox/122.0",
]

def get_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
        "DNT": "1",
        "Pragma": "no-cache",
    }


PROXY_SOURCES = [
    # HTML table-based sources
    "https://free-proxy-list.net/",
    "https://www.sslproxies.org/",
    "https://www.us-proxy.org/",
    "https://free-proxy-list.net/anonymous-proxy.html",
    "https://free-proxy-list.net/uk-proxy.html",
    "https://www.socks-proxy.net/",
    "https://hidemy.name/en/proxy-list/",
    "https://www.proxy-list.download/HTTP",
    "https://www.proxy-list.download/HTTPS",
    "https://www.proxy-list.download/SOCKS4",
    "https://www.proxy-list.download/SOCKS5",
    "https://spys.one/free-proxy-list/",
    "http://www.freeproxylists.net/",
    "https://premproxy.com/list/",
    "http://proxydb.net/",
    "https://www.proxynova.com/proxy-server-list/",
    "https://www.proxyscan.io/",
    "https://openproxy.space/list",
    "https://geonode.com/free-proxy-list",
    "https://proxyhub.me/",
    "https://www.freeproxy.world/",
    "https://proxyservers.pro/",
    "https://proxy-list.download/api/v1/get?type=https",
    "https://proxy-list.download/api/v1/get?type=http",
    "https://proxy-list.download/api/v1/get?type=socks4",
    "https://proxy-list.download/api/v1/get?type=socks5",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=elite",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/proxy-list/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/proxy-list/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/proxy-list/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/proxy-list/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/Coloquium/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/Coloquium/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/Coloquium/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/Coloquium/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/vexxhost/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/vexxhost/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/vexxhost/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/vexxhost/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/proxynova/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/proxynova/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/proxynova/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/proxynova/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/TechNoLogic/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/TechNoLogic/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/proxyscrape/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/proxyscrape/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/proxyscrape/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/proxyscrape/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/http-elite.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/https-elite.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/socks4-elite.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/socks5-elite.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/http-anonymous.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/https-anonymous.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/socks4-anonymous.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/socks5-anonymous.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/http-proxy.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/https-proxy.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/socks4-proxy.txt",
    "https://raw.githubusercontent.com/Proxy-List/proxy-list/master/socks5-proxy.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/zloi-user/hideMe/main/http.txt",
    "https://raw.githubusercontent.com/zloi-user/hideMe/main/https.txt",
    "https://raw.githubusercontent.com/zloi-user/hideMe/main/socks4.txt",
    "https://raw.githubusercontent.com/zloi-user/hideMe/main/socks5.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/http.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks4.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks5.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/https.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/HTTP.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/https.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cnfree.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cr.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/proxyranker.txt",
    "https://raw.githubusercontent.com/iTzPrime/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/iTzPrime/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/iTzPrime/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/TheGalaxyM/proxies/main/http.txt",
    "https://raw.githubusercontent.com/TheGalaxyM/proxies/main/socks4.txt",
    "https://raw.githubusercontent.com/TheGalaxyM/proxies/main/socks5.txt",
    "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/http.txt",
    "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/https.txt",
    "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/socks4.txt",
    "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/socks5.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/archived/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/archived/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/archived/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/archived/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/proxiesmaster/free-proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/proxiesmaster/free-proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/proxiesmaster/free-proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/tahaluindo/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/tahaluindo/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/tahaluindo/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/proxydata/Free-Proxy-List/main/proxy-data/http.txt",
    "https://raw.githubusercontent.com/proxydata/Free-Proxy-List/main/proxy-data/socks4.txt",
    "https://raw.githubusercontent.com/proxydata/Free-Proxy-List/main/proxy-data/socks5.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_geolocation/http.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_geolocation/socks4.txt",
    "https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies_geolocation/socks5.txt",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/socks5.txt",
    "https://proxyspace.pro/http.txt",
    "https://proxyspace.pro/https.txt",
    "https://proxyspace.pro/socks4.txt",
    "https://proxyspace.pro/socks5.txt",
    "https://www.proxy-daily.com/proxy_files/http.txt",
    "https://www.proxy-daily.com/proxy_files/https.txt",
    "https://www.proxy-daily.com/proxy_files/socks4.txt",
    "https://www.proxy-daily.com/proxy_files/socks5.txt",
    "https://rootjazz.com/proxies/proxies.txt",
    "https://openproxylist.xyz/http.txt",
    "https://openproxylist.xyz/socks4.txt",
    "https://openproxylist.xyz/socks5.txt",
    "https://advanced.name/freeproxy/6266536",
    "https://proxy.tgbot.co/txt/http",
    "https://proxy.tgbot.co/txt/https",
    "https://proxy.tgbot.co/txt/socks4",
    "https://proxy.tgbot.co/txt/socks5"
]
# Test URLs to verify proxy functionality
TEST_URLS = [
    "https://www.roblox.com",
    "https://www.google.com",
    "https://www.cloudflare.com",
    "https://httpbin.org/ip",
    "https://www.amazon.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.reddit.com",
    "https://www.github.com",
    "https://www.netflix.com",
]

def print_banner():
    """Display a cool ASCII art banner."""
    banner = f"""
{TermColors.CYAN}{TermColors.BRIGHT}
    ***********++++**+**********#####%#################%%#################**++++++++++++++++++     
     ***********++++**+*********########################%##################%#*+++++++++++++++++     
     ***********++++**+*********######################%%%#################%#%##*+++++++++++++++     
     ***********++++**+********####%##################%%#################%%#%%##*++++++++++++++     
     ***********++*++++*******####%##################%%%#############%%%%#%%%%%%#*+++++++++++++     
     ***********++**++*******####%%#################%%%##########%##%#%%#%%%#%%%%**++++++++++++     
     ***********++**++******#%%%%###################%%######%##%%#%%%%#%%%#%%%%%%#*++++++++++++     
     ***********++**+*******%%%%########%#########%%%%#######%%%%%%%%%%%%%%%%%%%%%#*+++++++++++     
     ***********++***+*****%%%%%#%%%%%%%%%%%%%%##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*+++++++++++     
     ***********+++*++****#%%%%%%%%%%%%%%%%%%%##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*++++++++++     
     ***********++++++++*#%%%%#%%%%%%%%%%%%%%##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*++++++++++     
     ***********+++++++**%%%%#%%%%%%%%##%%%%##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*+++++++++     
     ***********=++***+*#%%%#%%%%%%%%%%%%####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*++++++++     
     ***********=++++**#%%%%%%%@@@@@%%%%%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*++++++++     
     ***********=+++=+#%%%%@@@@@@@@@@@@@@%%%%####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*+++++++     
     ***********==+++*%%%%@@@@@@@@@@@@@@@@@@@%%%###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*+++++++     
     **********+==++*%%%@@@@@@@@@@@@@@@@@@@@@@@@%%%%%#%%%%%%%@%%%%%%%%%%%%%%%%%%%%%%%%%*+++++++     
     **********+==+*%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%@@@@%%@%%%%%%%%%%%%%%%%%%%#+++++++     
     **********+==*%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%@@@%%%%%%%%%%%%%%%%%%%#+++++++     
     ***********=*%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%@@@@%%%%%%%%%%%%%%%%%#++*++++     
     ***********+#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%@@@%%%%%%%%%%%%%%%%#*+++++*     
     ***********+%%%%%%%@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%@@%%%%%%%%%%%%%%%#*++++**     
     ********#**+%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@%%%%%%%%%%%%%%%#++++**#     
     **********++#%%%%%%%%@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@%%%%@%%%%%%%#+++*##*     
     ***********=*%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%@@@@%%%%%%%%%%%%#+******     
     *****###%#*=+%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@%%%%%%%%%%@%#*####**     
     %%%%%%#%%%*==*%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%%%%     
     %%%%%%#%%#*==+%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%@%%%%%%%%     
     %%%%%###%#*-==#@%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%%%%%     
     %%%%%#####*-==*%@@@@@@%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%**#%%%%%%%%     
     ##########+-==*%@@@@@@@@@%%%%##%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%#*=+#%%%%%%%%     
     *#####****+*#%%%@@@@@@@@@@@@@##%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%*==+*########     
     *#*##*****#%%%%%%%@@@@@@@@@@@#*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*#@@@@@@@@%%#*+===***######     
     *******#%%%%%%%%%%%%%%%%%%@@%#*%@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@%*#@@@@@@@@%%%#*===*****####     
     **++*#%#%%%%%%%%%%%%%%%%%%%%%##%%@@@%%@%%%%%%%%%@@@@@@@@@%@@@@%*#@@@@@@@%%%%%#*+=*********     
     **##%%%%%%%%%%%%%%%%%%%%%%%@%##%%@@@@%@%%#*********##%%%@@@@@@%*#%%%%%%%%%%%%%%##**###****     
     ##%#%%%%%%%%%%%%%%%%%%%%%%%%%##%%%%%@@@%@@#******#%%@@@@@@@@@@%****#%%%%%%%%%%%%%%###*##*#     
     ##%%%%%%%%%%%%%%%%%%%%%%%%%%%###%%#**#%%@@%#%#%#%@%%@@@@@@@@@@%#****%%%%%%%%%%%%%%%####*#*     
     #%%%%%%%%%%%%%%%%%%%%%%%%%%%%##%%%#****%%@%#%###%%@@%@@@@@@@@@%#**#%%%%%%%%%%%%%%%%%%##***     
     #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##%%%#***%@@@@%%@%%%%@@@%@@@@@@@%#***%%%%%%%%%%%%%%%%%%###**     
     ##%%%%%%%%%%%%%%%%%@%@@%%@%%@%##@@%%#*%%@@@@@@%@@%%%%%@%%@@@%%%#**#%%%%%%%%%%%%%%%%%%%#%##     
     #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*#%%@#*##%%%%@@%%@@%%%%%@%%@@@%%%#*#%%%%@%%%%%%%%%%%%%%%%#%%     
     %#%%%%%%%%%%%@@@@@@%@%%%%%%%%%##%%%###*%%%%%@%@%%%%%%@@%%%%%%%%#*#%%%%%%%%%%%%%%%%%%%%%%##     
     #%%%%%%%%%%@%%%%%%%%%%%%%%%%%%###%##*##*#%%%%%@%%%%%%@%%%%%%%%%#*#%%%%%@%%%%%%%%%%%%%#%%%%     
     #%#%%%%#%%%%%%%%%%%%%%%%%%%%%#####%####*#%%%%%%#%%#%%%%%%%%%%##**#%%%%%%%%@%%%%%%%%#%%%%%%                                                                                         
{TermColors.MAGENTA}
[+] Owner:bloodyzeze.
[+] Advanced Proxy Scraper v1.0 
[+] Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
[+] Target test sites: Roblox, Google, Cloudflare, and more
[+] Total proxy sources: {len(PROXY_SOURCES)}
{TermColors.RESET}
    """
    print(banner)
    
def create_output_directory():
    """Create directory for results if it doesn't exist."""
    if not os.path.exists("proxy_results"):
        os.makedirs("proxy_results")
    return "proxy_results"

def scrape_html_proxy_table(url):
    """Scrape proxies from websites that use HTML tables."""
    try:
        res = requests.get(url, headers=get_random_headers(), timeout=20)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, "html.parser")
        proxies = []
        
        # Handle tables with ID proxylisttable (common format)
        table = soup.find("table", {"id": "proxylisttable"})
        if table and table.tbody:
            for row in table.tbody.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 7:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    https = cols[6].text.strip().lower()
                    
                    if ip and port:
                        prefix = "https" if https == "yes" else "http"
                        proxies.append(f"{prefix}://{ip}:{port}")
        
        # Additional check for proxynova format
        if "proxynova.com" in url:
            for row in soup.select("tr[data-proxy-id]"):
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip_element = cols[0].select_one("abbr") or cols[0].select_one("script")
                    if ip_element:
                        ip_text = ip_element.get_text().strip()
                        if not ip_text:  # If empty, try to extract from script
                            script_text = cols[0].select_one("script")
                            if script_text:
                                ip_text = script_text.string
                                if ip_text and "document.write" in ip_text:
                                    ip_text = ip_text.split("'")[1]
                        
                        port = cols[1].text.strip()
                        if ip_text and port:
                            proxies.append(f"http://{ip_text}:{port}")
        
        # Fallback to any table with proxy-like content
        if not proxies:
            for table in soup.find_all("table"):
                for row in table.find_all("tr"):
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        # Look for IP:port pattern
                        ip_col = cols[0].text.strip()
                        port_col = None
                        
                        # Find column that could be a port (numeric)
                        for i in range(1, min(4, len(cols))):
                            if cols[i].text.strip().isdigit():
                                port_col = cols[i].text.strip()
                                break
                                
                        if ip_col and port_col and port_col.isdigit():
                            proxies.append(f"http://{ip_col}:{port_col}")
        
        print(f"{TermColors.GREEN}[+] {len(proxies)} proxies extracted from: {url}{TermColors.RESET}")
        return proxies
    except Exception as e:
        print(f"{TermColors.RED}[-] {url} failed: {str(e)}{TermColors.RESET}")
        return []

def scrape_direct_proxy_list(url):
    """Scrape proxies from direct text or API sources."""
    try:
        res = requests.get(url, headers=get_random_headers(), timeout=20)
        res.raise_for_status()
        
        lines = res.text.strip().splitlines()
        proxies = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Handle different formats
            if line.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
                proxies.append(line)
            elif ':' in line:
                # IP:port format without protocol
                ip, port = line.split(':', 1)
                if ip and port and port.isdigit():
                    # Determine protocol from URL or default to http
                    protocol = "http"
                    if "socks4" in url.lower():
                        protocol = "socks4"
                    elif "socks5" in url.lower():
                        protocol = "socks5"
                    elif "https" in url.lower():
                        protocol = "https"
                        
                    proxies.append(f"{protocol}://{ip}:{port}")
        
        print(f"{TermColors.GREEN}[+] {len(proxies)} proxies extracted from: {url}{TermColors.RESET}")
        return proxies
    except Exception as e:
        print(f"{TermColors.RED}[-] {url} failed: {str(e)}{TermColors.RESET}")
        return []

def check_proxy(proxy, test_urls=None):
    """Test if proxy is working with multiple test URLs."""
    if test_urls is None:
        test_urls = [TEST_URLS[0]]  # Default to first test URL if none specified
    
    proxy_protocol = proxy.split('://', 1)[0].lower()
    proxy_dict = {
        "http": proxy if proxy_protocol in ["http", "socks4", "socks5"] else None,
        "https": proxy if proxy_protocol in ["https", "socks4", "socks5"] else None
    }
    
    for test_url in test_urls:
        try:
            start_time = time.time()
            res = requests.get(test_url, proxies=proxy_dict, timeout=10)
            response_time = time.time() - start_time
            
            if res.status_code == 200:
                return {
                    "url": test_url,
                    "status": "working",
                    "response_time": round(response_time, 3),
                    "status_code": res.status_code
                }
        except Exception:
            pass
    
    return {"status": "failed"}

def validate_proxies(proxies, max_workers=100, max_working=200):
    """Validate proxies using concurrent connections."""
    working_proxies = []
    total = len(proxies)
    
    # Progress tracking variables
    processed = 0
    progress_interval = max(1, total // 20)  # Show progress at 5% intervals
    
    print(f"\n{TermColors.YELLOW}[*] Validating {total} proxies (this may take a while)...{TermColors.RESET}\n")
    
    # Shuffle proxies for better distribution
    random.shuffle(proxies)
    
    # Limit concurrent connections to avoid overwhelming resources
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy, [random.choice(TEST_URLS)]): proxy for proxy in proxies}
        
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            processed += 1
            
            # Show progress periodically
            if processed % progress_interval == 0 or processed == total:
                percentage = round((processed / total) * 100)
                print(f"{TermColors.CYAN}[*] Progress: {processed}/{total} ({percentage}%){TermColors.RESET}")
            
            try:
                result = future.result()
                if result["status"] == "working":
                    print(f"{TermColors.GREEN}[+] WORKING: {proxy} (Response: {result.get('response_time', '-')}s){TermColors.RESET}")
                    
                    # Store proxy details
                    proxy_data = {
                        "proxy": proxy,
                        "response_time": result.get("response_time"),
                        "test_url": result.get("url"),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    working_proxies.append(proxy_data)
                    
                    # Stop if we've reached our target of working proxies
                    if len(working_proxies) >= max_working:
                        print(f"\n{TermColors.YELLOW}[!] Reached target of {max_working} working proxies. Stopping validation.{TermColors.RESET}")
                        # Cancel remaining futures
                        for f in future_to_proxy:
                            f.cancel()
                        break
                else:
                    print(f"{TermColors.RED}[-] FAILED: {proxy}{TermColors.RESET}")
            except Exception as e:
                print(f"{TermColors.RED}[-] Exception while checking {proxy}: {str(e)}{TermColors.RESET}")
    
    return working_proxies

def categorize_proxies(working_proxies):
    """Categorize proxies by protocol and speed."""
    categories = {
        "http": [],
        "https": [],
        "socks4": [],
        "socks5": [],
        "fast": [],
        "medium": [],
        "slow": []
    }
    
    for proxy_data in working_proxies:
        proxy = proxy_data["proxy"]
        protocol = proxy.split("://")[0].lower()
        
        # Categorize by protocol
        if protocol in categories:
            categories[protocol].append(proxy_data)
        
        # Categorize by speed
        response_time = proxy_data.get("response_time", float("inf"))
        if response_time < 1.0:
            categories["fast"].append(proxy_data)
        elif response_time < 3.0:
            categories["medium"].append(proxy_data)
        else:
            categories["slow"].append(proxy_data)
    
    return categories

def save_results_to_files(working_proxies, output_dir):
    """Save working proxies to multiple file formats."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as JSON with detailed information
    json_filename = f"{output_dir}/working_proxies_{timestamp}.json"
    json_data = {
        "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_working": len(working_proxies),
        "proxies": working_proxies
    }
    
    with open(json_filename, "w") as f:
        json.dump(json_data, f, indent=2)
    
    # Save as simple text file for easy copying
    txt_filename = f"{output_dir}/working_proxies_{timestamp}.txt"
    with open(txt_filename, "w") as f:
        for proxy_data in working_proxies:
            f.write(f"{proxy_data['proxy']}\n")
    
    # Create a sorted list by response time
    sorted_proxies = sorted(working_proxies, key=lambda x: x.get("response_time", float("inf")))
    
    # Save as sorted list with response times
    sorted_filename = f"{output_dir}/sorted_by_speed_{timestamp}.txt"
    with open(sorted_filename, "w") as f:
        for proxy_data in sorted_proxies:
            response_time = proxy_data.get("response_time", "N/A")
            f.write(f"{proxy_data['proxy']} - Response time: {response_time}s\n")
    
    # Save categorized proxies
    categories = categorize_proxies(working_proxies)
    
    # Save each protocol type to separate file
    for protocol in ["http", "https", "socks4", "socks5"]:
        if categories[protocol]:
            protocol_filename = f"{output_dir}/{protocol}_proxies_{timestamp}.txt"
            with open(protocol_filename, "w") as f:
                for proxy_data in categories[protocol]:
                    f.write(f"{proxy_data['proxy']}\n")
    
    # Save speed-based categories
    for speed in ["fast", "medium", "slow"]:
        if categories[speed]:
            speed_filename = f"{output_dir}/{speed}_proxies_{timestamp}.txt"
            with open(speed_filename, "w") as f:
                for proxy_data in categories[speed]:
                    f.write(f"{proxy_data['proxy']} - {proxy_data.get('response_time', 'N/A')}s\n")
    
    return json_filename, txt_filename, sorted_filename

def remove_duplicates(proxies):
    """Remove duplicate proxies while preserving order."""
    seen = set()
    unique_proxies = []
    
    for proxy in proxies:
        # Normalize proxy format for comparison
        normalized = proxy.lower()
        if normalized not in seen:
            seen.add(normalized)
            unique_proxies.append(proxy)
    
    return unique_proxies

def main():
    """Main function to run the proxy scraper."""
    print_banner()
    
    start_time = time.time()
    output_dir = create_output_directory()
    
    # Scrape proxies from all sources
    print(f"\n{TermColors.CYAN}[*] Scraping proxies from {len(PROXY_SOURCES)} sources...{TermColors.RESET}\n")
    all_proxies = []
    
    # Different handlers for different source types
    for url in PROXY_SOURCES:
        if any(pattern in url for pattern in ["proxy-list.download/api", "proxyscrape", "githubusercontent", "raw.githubusercontent"]):
            proxies = scrape_direct_proxy_list(url)
        else:
            proxies = scrape_html_proxy_table(url)
        all_proxies.extend(proxies)
        
        # Small delay to avoid rate limiting
        time.sleep(random.uniform(0.5, 1.5))
    
    # Convert to list and remove duplicates
    unique_proxies = remove_duplicates(all_proxies)
    print(f"\n{TermColors.MAGENTA}[*] Total unique proxies found: {len(unique_proxies)}{TermColors.RESET}")
    
    # Validate proxies
    working_proxies = validate_proxies(unique_proxies)
    
    # Save results
    if working_proxies:
        json_file, txt_file, sorted_file = save_results_to_files(working_proxies, output_dir)
        
        print(f"\n{TermColors.GREEN}[+] Working proxies saved to:{TermColors.RESET}")
        print(f"{TermColors.CYAN}  - JSON (with details): {json_file}{TermColors.RESET}")
        print(f"{TermColors.CYAN}  - Plain text list: {txt_file}{TermColors.RESET}")
        print(f"{TermColors.CYAN}  - Speed-sorted list: {sorted_file}{TermColors.RESET}")
        
        # Count by protocol
        categories = categorize_proxies(working_proxies)
        protocols = ["http", "https", "socks4", "socks5"]
        for protocol in protocols:
            if categories[protocol]:
                print(f"{TermColors.CYAN}  - {protocol.upper()} proxies: {len(categories[protocol])}{TermColors.RESET}")
        
        # Count by speed
        speeds = ["fast", "medium", "slow"]
        for speed in speeds:
            if categories[speed]:
                print(f"{TermColors.CYAN}  - {speed.capitalize()} proxies: {len(categories[speed])}{TermColors.RESET}")
        
        print(f"\n{TermColors.GREEN}[+] Total working proxies: {len(working_proxies)}/{len(unique_proxies)} ({round(len(working_proxies)/len(unique_proxies)*100, 2)}% success rate){TermColors.RESET}")
    else:
        print(f"\n{TermColors.RED}[-] No working proxies found.{TermColors.RESET}")
    
    elapsed_time = time.time() - start_time
    print(f"\n{TermColors.MAGENTA}[*] Total execution time: {elapsed_time:.2f} seconds{TermColors.RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{TermColors.YELLOW}[!] Process interrupted by user.{TermColors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{TermColors.RED}[CRITICAL ERROR] {str(e)}{TermColors.RESET}")
        sys.exit(1)