# ===========> DON'T CHANGE THIS
# SCRIPT : VALIDATOR AMAZON EMAIL & PHONE
# VERSION : 4.0
# TELEGRAM AUTHOR : https://t.me/zlaxtert
# SITE : https://darkxcode.site/
# TEAM : DARKXCODE
# ================> END


import requests
import threading
import time
import os
import configparser
from colorama import *
from termcolor import colored
from queue import Queue
from urllib.parse import quote

#colors
merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
biru = Fore.LIGHTBLUE_EX
kuning = Fore.LIGHTYELLOW_EX
magenta = Fore.LIGHTMAGENTA_EX
cyan = Fore.CYAN
reset = Fore.RESET
bl = Fore.BLUE
wh = Fore.WHITE
gr = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
res = Style.RESET_ALL
yl = Fore.YELLOW
cy = Fore.CYAN
mg = Fore.MAGENTA
bc = Back.GREEN
fr = Fore.RED
sr = Style.RESET_ALL
fb = Fore.BLUE
fc = Fore.LIGHTCYAN_EX
fg = Fore.GREEN
br = Back.RED

# BANNER 

banner = f"""{hijau}
                                 /           /                          
                                /' .,,,,  ./ \                           
                               /';'     ,/  \                                
                              / /   ,,//,'''                         
                             ( ,, '_,  ,,,' ''                 
                             |    /{merah}@{hijau}  ,,, ;' '               
                            /    .   ,''/' ',''       
                           /   .     ./, ',, ' ;                      
                        ,./  .   ,-,',' ,,/''\,'                 
                       |   /; ./,,'',,'' |   |                                               
                       |     /   ','    /    |                                               
                        \___/'   '     |     |                                               
                         ',,'  |      /     '\                                              
                              /  (   |   )    ~\                                            
                             '   \   (    \     \~                                            
                             :    \                \                                                 
                              ; .         \--                                                  
                               :   \         ; {magenta}                                                 
,------.    ,---.  ,------. ,--. ,--.,--.   ,--. ,-----.  ,-----. ,------.  ,------. 
|  .-.  \  /  O  \ |  .--. '|  .'   / \  `.'  / '  .--./ '  .-.  '|  .-.  \ |  .---' 
|  |  \  :|  .-.  ||  '--'.'|  .   '   .'    \  |  |     |  | |  ||  |  \  :|  `--,  
|  '--'  /|  | |  ||  |\  \ |  |\   \ /  .'.  \ '  '--'\ '  '-'  '|  '--'  /|  `---. 
`-------' `--' `--'`--' '--'`--' '--''--'   '--' `-----'  `-----' `-------' `------' {reset}
{fr}       ===================================================================={reset}
                  |{fb} SCRIPT{reset}  :{fg} VALIDATOR AMAZON EMAIL & PHONE {reset} |
                  |{fb} VERSION{reset} :{fg} 4.0{reset}                             |
                  |{fb} AUTHOR {reset} :{fg} https://t.me/zlaxtert{reset}           |
{fr}       ===================================================================={reset}
"""


class AmazonValidator:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.load_config()
        self.lists_queue = Queue()
        self.proxies = []
        self.live_count = 0
        self.die_count = 0
        self.total_count = 0
        self.checked_count = 0
        self.lock = threading.Lock()
        
    def load_config(self):
        """Reading configuration from settings.ini"""
        if not os.path.exists('settings.ini'):
            self.create_default_config()
        self.config.read('settings.ini')
        
        # Validate required settings
        if self.config['SETTINGS']['APIKEY'] == 'PASTE_YOUR_API_KEY_HERE':
            print(f"{res}[{yl}!{res}]{fb} Please configure your API key in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}\n\n")
            exit()
        elif self.config['SETTINGS']['API'] == 'PASTE_YOUR_API_HERE':
            print(f"{res}[{yl}!{res}]{fb} Please configure your API in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}\n\n")
            exit()
        elif self.config['SETTINGS']['PROXY_AUTH'] == 'PASTE_YOUR_PROXY_AUTH_HERE':
            print(f"{res}[{yl}!{res}]{fb} Please configure your PROXY AUTH in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}")
            print(f"{res}[{yl}!{res}]{fb} If your proxy does not use Authentication, then leave the PROXY AUTH section in the {yl}settings.ini{fb} file blank {res}[{yl}!{res}]{fb}\n\n")
            exit()
        
        
    def create_default_config(self):
        """Creating a default configuration file"""
        self.config['SETTINGS'] = {
            'APIKEY': 'PASTE_YOUR_API_KEY_HERE',
            'API': 'PASTE_YOUR_API_HERE',
            'PROXY_AUTH': 'PASTE_YOUR_PROXY_AUTH_HERE',
            'TYPE_PROXY': 'http'
        }
        
        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)
            
        # Create a results folder
        os.makedirs('result', exist_ok=True)
    
    def load_lists(self, filename):
        """Loading email/phone number list from file"""
        if not os.path.exists(filename):
            print(f"{res}[{yl}!{res}]{fb} File {fg}{filename}{res}{fb} not found {res}[{yl}!{res}]{fb}")
            return False
            
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                item = line.strip()
                if item:
                    self.lists_queue.put(item)
                    
        self.total_count = self.lists_queue.qsize()
        print(f"{res}[{yl}!{res}]{fb} Successfully loaded {fg}{self.total_count}{res}{fb} lists from {fc}{filename} {res}[{yl}!{res}]{fb}")
        return True
        
    def load_proxies(self, filename):
        """Loading proxy list from file"""
        if not os.path.exists(filename):
            print(f"{res}[{yl}!{res}]{fb} File {fg}{filename}{res}{fb} not found {res}[{yl}!{res}]{fb}")
            return False
            
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    self.proxies.append(proxy)
                    
        return True
        
    def validate_item(self, item, proxy_index=0):
        """Validate a single item using the API"""
        apikey = self.config['SETTINGS']['APIKEY']
        api_url = self.config['SETTINGS']['API']
        proxy_auth = self.config['SETTINGS']['PROXY_AUTH']
        type_proxy = self.config['SETTINGS']['TYPE_PROXY']
        
        # Encode items for URL
        encoded_item = quote(item)
        
        proxy = self.proxies[proxy_index % len(self.proxies)]
        
        # Set up parameters
        params = {
            'list': item,
            'apikey': apikey,
            'proxy': proxy,
            'type_proxy': type_proxy
        }
        
        # Add auth proxy if available
        if proxy_auth:
            params['proxyAuth'] = proxy_auth
        
        try:
            response = requests.get(api_url + "/validator/amazon/", params=params, timeout=30)
            data = response.json()
            
            if 'data' in data and 'info' in data['data']:
                info = data['data']['info']
                valid = data['data']['valid']
                msg = info.get('msg', 'UNKNOWN')
                
                result_line = f"{item}|{msg}"
                
                # Save results based on status
                if valid and any(x in msg for x in ['VALID PHONE NUMBER', 'VALID EMAIL ADDRESS']):
                    with self.lock:
                        self.live_count += 1
                    self.save_result('result/live.txt', result_line)
                    status = "LIVE"
                else:
                    with self.lock:
                        self.die_count += 1
                    self.save_result('result/die.txt', result_line)
                    status = "DIE"
                
                # Show results
                with self.lock:
                    self.checked_count += 1
                    # Display progress
                    progress = f"{yl}Checked {res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]"
                
                if msg.upper() == "VALID EMAIL ADDRESS" :
                    stats = f"{hijau}{status.upper()}{reset}"
                elif msg.upper() == "VALID PHONE NUMBER" :
                    stats = f"{hijau}{status.upper()}{reset}"
                else :
                    stats = f"{merah}{status.upper()}{reset}" 
                    
                print(f"{progress}{res} -{yl} {item}{res} -> {stats} | {yl}{msg}{res} |{cyan} BY DARKXCODE V4.0{reset}")
                
            else:
                print(f"{res} -{yl} {item}{res} -> {merah}ERROR{reset} | {yl}INVALID RESPONSE{res} |{cyan} BY DARKXCODE V4.0{reset}")
                
                
        except Exception as e:
            print(f"{res} -{yl} {item}{res} -> {merah}VALIDATION ERROR{reset} | {yl}{str(e)}{res} |{cyan} BY DARKXCODE V4.0{reset}")
            
    def save_result(self, filename, data):
        """Save results to file"""
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(data + '\n')
            
    def worker(self):
        """Worker thread to process validation"""
        proxy_index = 0
        while True:
            try:
                item = self.lists_queue.get_nowait()
            except:
                break
                
            self.validate_item(item, proxy_index)
            proxy_index += 1
            self.lists_queue.task_done()
            
    def run(self):
        """Running validation process"""
        # Input file lists
        lists_file = input(f"{res}[{yl}+{res}]{fb} Enter Email lists file{fg} >> {fb}").strip()
        if not self.load_lists(lists_file):
            return
            
        # Input proxy file
        proxy_file = input(f"{res}[{yl}+{res}]{fb} Enter Proxy lists file{fg} >> {fb}").strip()
        if proxy_file and not self.load_proxies(proxy_file):
            return
            
        # Input number of threads
        try:
            threads_count = int(input(f"{res}[{yl}+{res}]{fb} Enter number of Threads (5-50) (Recomended 5-10){fg} >> {fb}").strip())
            threads_count = max(5, min(50, threads_count))  # Limit between 5-50
        except:
            print(f"{res}[{yl}!{res}]{fb} Invalid number of threads, using default 10 threads {res}[{yl}!{res}]{fb}\n\n")
            
            threads_count = 10
            
        # Make sure the result folder exists
        os.makedirs('result', exist_ok=True)
        
        
        print(f"\n{yl}Starting validation with {fg}{threads_count}{yl} threads{res}")
        print(f"{fr}={res}" * 60)
        
        start_time = time.time()
        
        # Create and run threads
        threads = []
        for i in range(threads_count):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
            
        # Wait for all threads to finish
        self.lists_queue.join()
        
        # Wait for all threads to complete completely
        for t in threads:
            t.join()
            
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{fr}={res}" * 60)
        print(f"Checking completed! Live: {fg}{self.live_count}{res} | Die: {fr}{self.die_count}{res}")
        print(f"Time taken: {elapsed_time:.2f} seconds")
        print(f"{res}[{yl}!{res}]{fb} Results saved in 'result' folder {res}[{yl}!{res}]{fb}")
        print(f"{fr}={res}" * 60)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    validator = AmazonValidator()
    validator.run()