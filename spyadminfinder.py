#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import random
import requests
import socket
import socks
import subprocess
import sys
import time
import threading
from tqdm import tqdm
import urllib.request, urllib.error, urllib.parse
from urllib.request import urlopen
from colorama import Fore, Style

try:
    # Change main dir to this (needed for Pentest Box)
    os.path.abspath(__file__)
    from Classes import Credits, SpyAdminFinderClass, MessengerClass

    # Get Messenger class to print information
    messenger = MessengerClass.Messenger()

except ImportError as e:
    sys.exit(f'\n\t[x] Session Cancelled; Module import failed: {e}')

# Get credits and print it
messenger.writeMessage(Credits.getCredits()[0], 'green')

# Get main class object
SpyAdminFinder = SpyAdminFinderClass.SpyAdminFinder()

parser = argparse.ArgumentParser(
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30, width=90)
)
parser.add_argument("-u", "--url", default=False, help="Target URL (e.g. 'www.example.com' or 'example.com')")
parser.add_argument("-t", "--tor", action='store_true', default=False, help="Use Tor anonymity network")
parser.add_argument("-p", "--proxy", default=False, help="Use HTTP Proxy (e.g '127.0.0.1:8080')")
parser.add_argument("-rp", "--random-proxy", action="store_true", default=False, dest="random_proxy", help="Use a randomly selected proxy server")
parser.add_argument("-r", "--random-agent", action='store_true', default=False, dest='rand', help="Use a randomly selected user-agent")
parser.add_argument("-v", "--verbose", action='store_true', default=False, help="Show more detailed information")
parser.add_argument("-U", "--update", action='store_true', default=False, help="Update SpyAdminFinder")
parser.add_argument("-i", "--interactive", action='store_true', default=False, help="Interactive interface" + Fore.RED + Style.BRIGHT + "[other arguments not required]")

args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_usage()
    sys.exit(1)

proxies = ""
headers = {'user-agent': f'SpyAdminFinder/{Credits.getCredits()[1]}'}
SpyAdminFinder.header = headers

def url_scan(site):
    try:
        if SpyAdminFinder.checkUrl(site, proxies):
            messenger.writeMessage(f'\n  Scanning {site}, we hope to find something.\n', 'green')
            urls = tqdm(SpyAdminFinder.getUrls('LinkFile/adminpanellinks.txt'), bar_format="{l_bar}{bar}|{n_fmt}/{total_fmt}{postfix}")
        else:
            messenger.writeMessage('  Something is wrong with the URL', 'red')
            urls = tqdm(SpyAdminFinder.getUrls('LinkFile/adminpanellinks.txt'), bar_format="{bar}")
            sys.exit(1)
        
        totalCount, adminCount = len(urls), 0
        
        for url in urls:
            reqLink = SpyAdminFinder.createReqLink(site, url, proxies)
            urls.set_description(Fore.WHITE + Style.NORMAL + "  Scanning...")
            
            if SpyAdminFinder.checkUrl(reqLink, proxies):
                adminCount += 1
                messenger.writeMessage(f'\n{Fore.CYAN + Style.BRIGHT}[✔] http://{reqLink:<50}{Fore.GREEN + Style.BRIGHT}{"Admin Panel Found!":>30}\n', 'bright')

                if adminCount % 10 == 0:
                    messenger.writeInput('  Press ' + Fore.BLUE + Style.BRIGHT + 'Enter ' + Fore.WHITE + Style.NORMAL + 'to continue or ' + Fore.RED + Style.BRIGHT + 'CTRL+C ' + Fore.WHITE + Style.NORMAL + 'to stop.\n')
            else:
                continue

        messenger.writeMessage(f'\n\n  Scan Complete \n', 'green')
        messenger.writeMessage(f'{adminCount} Admin panels found', 'white')
        messenger.writeMessage(f'{totalCount} Total pages scanned', 'white')
        messenger.writeInput('  [/] Scan complete; Press Enter to exit ', 'green')

    except (KeyboardInterrupt, SystemExit):
        messenger.writeMessage('\n\t[x] Cancelled', 'red')
        urls.close()

    except Exception as e:
        messenger.writeMessage(f'\n\t[x] Cancelled due to unknown error: {e}', 'red')

def random_agent():
    useragent_file = "LinkFile/user-agent.txt"
    with open(useragent_file, 'r') as f:
        ua_list = f.read().splitlines()
    headers = {'user-agent': random.choice(ua_list)}
    SpyAdminFinder.header = headers
    return headers

def random_proxy():
    proxy_list_url = 'https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt'
    proxy_list = requests.get(proxy_list_url).text.splitlines()
    selected_proxy = random.choice(proxy_list)
    ip, port = selected_proxy.rsplit(':', 1)
    
    proxies = {'http': selected_proxy, 'https': selected_proxy}
    
    try:
        s = socks.socksocket()
        s.set_proxy(socks.HTTP, ip, int(port))
        socket.socket = socks.socksocket
        urllib.request.urlopen
    except (IndexError, IndentationError):
        messenger.writeMessage('\n\tSorry, Error 😭 ', 'red')
        sys.exit(0)
    
    return proxies

def tor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, 'localhost', 9050)
    socket.socket = socks.socksocket
    urllib.request.urlopen

def setup_proxy():
    proxies = {'http': args.proxy, 'https': args.proxy}
    try:
        ip, port = args.proxy.split(':')
        s = socks.socksocket()
        s.set_proxy(socks.HTTP, ip, int(port))
        socket.socket = socks.socksocket
        urllib.request.urlopen
    except (IndexError, IndentationError):
        messenger.writeMessage('\n\tCheck proxy format | Example: 127.0.0.1:8080 ', 'red')
        sys.exit(0)
    
    try:
        print(Fore.BLUE + '\tChecking HTTP proxy...', end="\r")
        time.sleep(1)
        requests.get('http://testphp.vulnweb.com', proxies=proxies, timeout=10)
        print(Fore.BLUE + '\tChecking HTTP proxy...', Fore.GREEN + Style.BRIGHT + 'OK\n' + Fore.WHITE + Style.NORMAL)
    except requests.RequestException:
        print(Fore.BLUE + '\tChecking HTTP proxy...', Fore.RED + Style.BRIGHT + 'BAD\n' + Fore.WHITE + Style.NORMAL)
        messenger.writeMessage('\n ╔═══[!] Connection Error', 'red')
        sys.exit(0)
    
    return proxies

def update():
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0].decode("utf-8")
    print(output)

def interactive():
    try:
        useragent_file = "LinkFile/user-agent.txt"
        try:
            print(Fore.BLUE + '\tFetching random user-agent...', end="\r")
            time.sleep(1)
            with open(useragent_file, 'r') as f:
                ua_list = f.read().splitlines()
            headers = {'user-agent': random.choice(ua_list)}
            print(Fore.BLUE + '\tFetching random user-agent...', Fore.GREEN + Style.BRIGHT + 'DONE\n' + Fore.WHITE + Style.NORMAL)
        except FileNotFoundError:
            headers = {'user-agent': f'SpyAdminFinder/{Credits.getCredits()[1]}'}
        
        SpyAdminFinder.header = headers

        proxies = ""
        while True:
            choice = input(Fore.YELLOW + '''    ├╼[1] Tor
    ├╼[2] Proxy
    ├╼[3] Nothing
    └───╼ Please select an option: ''')
            
            if choice == '1':
                tor()
            elif choice == '2':
                proxies = setup_proxy()
            elif choice == '3':
                proxies = ""
            else:
                continue
            break

        ip = requests.get('http://ifconfig.co/ip', proxies=proxies, headers=SpyAdminFinder.header).text.strip()
        cc = requests.get('http://ifconfig.co/country', proxies=proxies, headers=SpyAdminFinder.header).text.strip()
        iso = requests.get('http://ifconfig.co/country-iso', proxies=proxies, headers=SpyAdminFinder.header).text.strip()
        city = requests.get('http://ifconfig.co/city', proxies=proxies, headers=SpyAdminFinder.header).text.strip()

        print(f'''    ┆
    ├───[''' + Fore.CYAN + Style.BRIGHT + '''*''' + Fore.YELLOW + Style.NORMAL + '''] Your external IP: ''' + Fore.CYAN + Style.BRIGHT + f'''{ip}''' + Fore.YELLOW + Style.NORMAL + f'''
    ├───[''' + Fore.CYAN + Style.BRIGHT + '''*''' + Fore.YELLOW + Style.NORMAL + '''] Country Code: ''' + Fore.CYAN + Style.BRIGHT + f'''{cc}''' + Fore.YELLOW + Style.NORMAL + f'''
    ├───[''' + Fore.CYAN + Style.BRIGHT + '''*''' + Fore.YELLOW + Style.NORMAL + '''] ISO Code: ''' + Fore.CYAN + Style.BRIGHT + f'''{iso}''' + Fore.YELLOW + Style.NORMAL + f'''
    └───[''' + Fore.CYAN + Style.BRIGHT + '''*''' + Fore.YELLOW + Style.NORMAL + '''] City: ''' + Fore.CYAN + Style.BRIGHT + f'''{city}''' + Fore.YELLOW + Style.NORMAL + '''\n''' + Fore.WHITE)

        target = input(f'''    ┌───[''' + Fore.CYAN + Style.BRIGHT + '''*''' + Fore.WHITE + Style.NORMAL + '''] Please enter your target URL: ''')

        if SpyAdminFinder.checkUrl(target, proxies):
            messenger.writeMessage(f'\n  Scanning {target}, we hope to find something.\n', 'green')
            urls = tqdm(SpyAdminFinder.getUrls('LinkFile/adminpanellinks.txt'), bar_format="{l_bar}{bar}|{n_fmt}/{total_fmt}{postfix}")
        else:
            messenger.writeMessage('  Something is wrong with the URL', 'red')
            urls = tqdm(SpyAdminFinder.getUrls('LinkFile/adminpanellinks.txt'), bar_format="{bar}")
            sys.exit(1)

        totalCount, adminCount = len(urls), 0
        for url in urls:
            reqLink = SpyAdminFinder.createReqLink(target, url, proxies)
            urls.set_description(Fore.WHITE + Style.NORMAL + "  Scanning...")

            if SpyAdminFinder.checkUrl(reqLink, proxies):
                adminCount += 1
                messenger.writeMessage(f'\n{Fore.CYAN + Style.BRIGHT}[✔] http://{reqLink:<50}{Fore.GREEN + Style.BRIGHT}{"Admin Panel Found!":>30}\n', 'bright')

                if adminCount % 10 == 0:
                    messenger.writeInput('  Press ' + Fore.BLUE + Style.BRIGHT + 'Enter ' + Fore.WHITE + Style.NORMAL + 'to continue or ' + Fore.RED + Style.BRIGHT + 'CTRL+C ' + Fore.WHITE + Style.NORMAL + 'to stop.\n')
            else:
                continue

        messenger.writeMessage(f'\n\n  Scan Complete \n', 'green')
        messenger.writeMessage(f'{adminCount} Admin panels found', 'white')
        messenger.writeMessage(f'{totalCount} Total pages scanned', 'white')
        messenger.writeInput('  [/] Scan complete; Press Enter to exit ', 'green')

    except (KeyboardInterrupt, SystemExit):
        messenger.writeMessage('\n\t[x] Cancelled', 'red')
        urls.close()
    except Exception as e:
        messenger.writeMessage(f'\n\t[x] Cancelled due to unknown error: {e}', 'red')

if args.update:
    update()

if args.rand:
    random_agent()

if args.random_proxy:
    proxies = random_proxy()

if args.tor:
    tor()

if args.proxy:
    proxies = setup_proxy()

if args.interactive:
    interactive()

if args.url:
    url_scan(args.url)
