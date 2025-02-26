import requests
import json
import random
import time
from typing import Dict, List
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

GLOBAL_HEADERS = {
    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,id;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://agents.testnet.gokite.ai',
    'Referer': 'https://agents.testnet.gokite.ai/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

AI_ENDPOINTS = {
    "https://deployment-htmtbvzpc0vboktahrrv1b7f.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_htmTBVZpC0vbOkTAHRrv1b7F",
        "name": "Professor",
        "questions": [
            "What is Kite AI's core technology?",
            "How does Kite AI improve developer productivity?",
            "What are the key features of Kite AI's platform?",
            "How does Kite AI handle data security?",
            "What makes Kite AI different from other AI platforms?",
            "How does Kite AI integrate with existing systems?",
            "What programming languages does Kite AI support?",
            "How does Kite AI's API work?",
            "What are Kite AI's scalability features?",
            "How does Kite AI help with code quality?",
            "What is Kite AI's approach to machine learning?",
            "How does Kite AI handle version control?",
            "What are Kite AI's deployment options?",
            "How does Kite AI assist with debugging?",
            "What are Kite AI's code completion capabilities?",
            "How does Kite AI handle multiple projects?",
            "What is Kite AI's pricing structure?",
            "How does Kite AI support team collaboration?",
            "What are Kite AI's documentation features?",
            "How does Kite AI implement code reviews?",
            "What is Kite AI's update frequency?",
            "How does Kite AI handle error detection?",
            "What are Kite AI's testing capabilities?",
            "How does Kite AI support microservices?",
            "What is Kite AI's cloud infrastructure?",
            "How does Kite AI handle API documentation?",
            "What are Kite AI's code analysis features?",
            "How does Kite AI support continuous integration?",
            "What is Kite AI's approach to code optimization?",
            "How does Kite AI handle multilingual support?",
            "What are Kite AI's security protocols?",
            "How does Kite AI manage user permissions?",
            "What is Kite AI's backup system?",
            "How does Kite AI handle code refactoring?",
            "What are Kite AI's monitoring capabilities?",
            "How does Kite AI support remote development?",
            "What is Kite AI's approach to technical debt?",
            "How does Kite AI handle code dependencies?",
            "What are Kite AI's performance metrics?",
            "How does Kite AI support code documentation?",
            "What is Kite AI's approach to API versioning?",
            "How does Kite AI handle load balancing?",
            "What are Kite AI's debugging tools?",
            "How does Kite AI support code generation?",
            "What is Kite AI's approach to data validation?",
            "How does Kite AI handle error logging?",
            "What are Kite AI's testing frameworks?",
            "How does Kite AI support code deployment?",
            "What is Kite AI's approach to code maintenance?",
            "How does Kite AI handle system integration?"
        ]
    },
    "https://deployment-nfkj10q1reqxkm4crtrlzmt9.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_nfkj10Q1ReqxkM4crtrlZMt9",
        "name": "Crypto Buddy",
        "questions": [
            "What is Bitcoin's current price?",
            "Show me Ethereum price",
            "What's the price of BNB?",
            "Current Solana price?",
            "What's AVAX trading at?",
            "Show me MATIC price",
            "Current price of DOT?",
            "What's the XRP price now?",
            "Show me ATOM price",
            "What's the current LINK price?",
            "Show me ADA price",
            "What's NEAR trading at?",
            "Current price of FTM?",
            "What's the ALGO price?",
            "Show me DOGE price",
            "What's SHIB trading at?",
            "Current price of UNI?",
            "What's the AAVE price?",
            "Show me LTC price",
            "What's ETC trading at?",
            "Show me the price of SAND",
            "What's MANA's current price?",
            "Current price of APE?",
            "What's the GRT price?",
            "Show me BAT price",
            "What's ENJ trading at?",
            "Current price of CHZ?",
            "What's the CAKE price?",
            "Show me VET price",
            "What's ONE trading at?",
            "Show me the price of GALA",
            "What's THETA's current price?",
            "Current price of ICP?",
            "What's the FIL price?",
            "Show me EOS price",
            "What's XTZ trading at?",
            "Show me the price of ZIL",
            "What's WAVES current price?",
            "Current price of KSM?",
            "What's the DASH price?",
            "Show me NEO price",
            "What's XMR trading at?",
            "Show me the price of IOTA",
            "What's EGLD's current price?",
            "Current price of COMP?",
            "What's the SNX price?",
            "Show me MKR price",
            "What's CRV trading at?",
            "Show me the price of RUNE",
            "What's 1INCH current price?"
        ]
    },
    "https://deployment-zs6oe0edbuquit8kk0v10djt.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_zs6OE0EdBuQuit8KK0V10dJT",
        "name": "Sherlock",
        "questions": []
    }
}

SHERLOCK_ENDPOINT = "https://deployment-zs6oe0edbuquit8kk0v10djt.stag-vxzy.zettablock.com/main"

class KiteAIAutomation:
    def __init__(self, wallet_addresses: List[str], proxies: List[str], max_iterations: int = 20):
        self.wallet_addresses = wallet_addresses
        self.proxies = proxies
        self.current_wallet_index = 0
        self.daily_points = 0
        self.start_time = datetime.now()
        self.next_reset_time = self.start_time + timedelta(hours=24)
        self.MAX_DAILY_POINTS = 200
        self.POINTS_PER_INTERACTION = 10
        self.MAX_DAILY_INTERACTIONS = self.MAX_DAILY_POINTS // self.POINTS_PER_INTERACTION
        self.current_day_transactions = []
        self.last_transaction_fetch = None
        self.max_iterations = max_iterations
        self.iteration_count = 0
        
        # Initialize a list to track iterations per wallet
        self.wallet_iterations = [0] * len(wallet_addresses)

    def reset_daily_points(self):
        current_time = datetime.now()
        if current_time >= self.next_reset_time:
            print(f"{self.print_timestamp()} {Fore.GREEN}Resetting points for new 24-hour period{Style.RESET_ALL}")
            self.daily_points = 0
            self.next_reset_time = current_time + timedelta(hours=24)
            self.current_day_transactions = []
            self.last_transaction_fetch = None
            return True
        return False

    def should_wait_for_next_reset(self):
        if self.daily_points >= self.MAX_DAILY_POINTS:
            wait_seconds = (self.next_reset_time - datetime.now()).total_seconds()
            if wait_seconds > 0:
                print(f"{self.print_timestamp()} {Fore.YELLOW}Daily point limit reached ({self.MAX_DAILY_POINTS}){Style.RESET_ALL}")
                print(f"{self.print_timestamp()} {Fore.YELLOW}Waiting until next reset at {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
                time.sleep(wait_seconds)
                self.reset_daily_points()
            return True
        return False

    def print_timestamp(self):
        return f"{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{Style.RESET_ALL}"

    def get_recent_transactions(self, for_sherlock=False) -> List[str]:
        current_day = datetime.now().date()
        
        if self.last_transaction_fetch and self.last_transaction_fetch.date() == current_day and self.current_day_transactions:
            if for_sherlock:
                print(f"{self.print_timestamp()} {Fore.BLUE}Using cached transactions for today{Style.RESET_ALL}")
            return self.current_day_transactions
            
        if for_sherlock:
            print(f"{self.print_timestamp()} {Fore.BLUE}Fetching new transactions for today{Style.RESET_ALL}")
        
        url = 'https://testnet.kitescan.ai/api/v2/transactions'
        params = {
            'filter': 'validated',
            'age': '1m'
        }        
        headers = GLOBAL_HEADERS.copy()
        headers['accept'] = '*/*'
        
        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            hashes = [item['hash'] for item in data.get('items', [])]
            self.current_day_transactions = hashes
            self.last_transaction_fetch = datetime.now()
            if for_sherlock:
                print(f"{self.print_timestamp()} {Fore.MAGENTA}Successfully fetched {len(hashes)} transactions{Style.RESET_ALL}")
            return hashes
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error fetching transactions: {e}{Style.RESET_ALL}")
            return []

    def send_ai_query(self, endpoint: str, message: str, wallet_address: str, proxy: str) -> tuple:
        headers = GLOBAL_HEADERS.copy()
        headers['Accept'] = 'text/event-stream'
        
        data = {
            "message": message,
            "stream": True
        }
        
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        
        ttft = 0
        total_time = 0
        
        print(f"{self.print_timestamp()} {Fore.BLUE}Sending question to AI Agent: {Fore.MAGENTA}{message}{Style.RESET_ALL}\n")
        start_time = time.time()
        first_token_received = False
        
        try:
            response = requests.post(endpoint, headers=headers, json=data, stream=True, proxies=proxies)
            accumulated_response = ""
            
            print(f"{Fore.CYAN}AI Agent Response: {Style.RESET_ALL}", end='', flush=True)
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        try:
                            json_str = line[6:]
                            if json_str == '[DONE]':
                                break
                            
                            json_data = json.loads(json_str)
                            content = json_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                            if content:
                                if not first_token_received:
                                    ttft = (time.time() - start_time) * 1000
                                    first_token_received = True
                                
                                accumulated_response += content
                                print(Fore.MAGENTA + content + Style.RESET_ALL, end='', flush=True)
                        except json.JSONDecodeError:
                            continue
            
            total_time = (time.time() - start_time) * 1000
            print() 
            return accumulated_response.strip(), ttft, total_time
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error in AI query: {e}{Style.RESET_ALL}")
            return "", 0, 0

    def report_usage(self, endpoint: str, message: str, response: str, ttft: float, total_time: float, wallet_address: str) -> bool:
        print(f"{self.print_timestamp()} {Fore.BLUE}Reporting usage...{Style.RESET_ALL}")
        url = 'https://quests-usage-dev.prod.zettablock.com/api/report_usage'
        
        headers = GLOBAL_HEADERS.copy()
        
        data = {
            "wallet_address": wallet_address,
            "agent_id": AI_ENDPOINTS[endpoint]["agent_id"],
            "request_text": message,
            "response_text": response,
            "ttft": ttft,
            "total_time": total_time,
            "request_metadata": {}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 200
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error reporting usage: {e}{Style.RESET_ALL}")
            return False

    def check_stats(self, wallet_address: str) -> Dict:
        url = f'https://quests-usage-dev.prod.zettablock.com/api/user/{wallet_address}/stats'
        
        headers = GLOBAL_HEADERS.copy()
        headers['accept'] = '*/*'
        
        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error checking stats: {e}{Style.RESET_ALL}")
            return {}

    def print_stats(self, stats: Dict):
        print(f"\n{Fore.CYAN}=== Current Statistics ==={Style.RESET_ALL}")
        print(f"Total Interactions: {Fore.GREEN}{stats.get('total_interactions', 0)}{Style.RESET_ALL}")
        print(f"Total Agents Used: {Fore.GREEN}{stats.get('total_agents_used', 0)}{Style.RESET_ALL}")
        print(f"First Seen: {Fore.YELLOW}{stats.get('first_seen', 'N/A')}{Style.RESET_ALL}")
        print(f"Last Active: {Fore.YELLOW}{stats.get('last_active', 'N/A')}{Style.RESET_ALL}")

    def interact_with_ai(self, wallet_address: str, proxy: str):
        """Function to handle interaction with AI for a specific wallet and proxy."""
        endpoint = random.choice(list(AI_ENDPOINTS.keys()))
        question = random.choice(AI_ENDPOINTS[endpoint]["questions"])
        
        print(f"{self.print_timestamp()} {Fore.CYAN}Using Wallet Address: {Fore.MAGENTA}{wallet_address}{Style.RESET_ALL}")
        print(f"{self.print_timestamp()} {Fore.CYAN}Using Proxy: {Fore.MAGENTA}{proxy}{Style.RESET_ALL}")
        
        initial_stats = self.check_stats(wallet_address)
        initial_interactions = initial_stats.get('total_interactions', 0)
        
        response, ttft, total_time = self.send_ai_query(endpoint, question, wallet_address, proxy)
        
        print(f"{self.print_timestamp()} {Fore.BLUE}TTFT: {ttft:.2f}ms | Total Time: {total_time:.2f}ms{Style.RESET_ALL}")
        
        if self.report_usage(endpoint, question, response, ttft, total_time, wallet_address):
            print(f"{self.print_timestamp()} {Fore.GREEN}Usage reported successfully{Style.RESET_ALL}")
            time.sleep(2)
            final_stats = self.check_stats(wallet_address)
            final_interactions = final_stats.get('total_interactions', 0)
            if final_interactions > initial_interactions:
                print(f"{self.print_timestamp()} {Fore.GREEN}Interaction successfully recorded!{Style.RESET_ALL}")
                self.daily_points += self.POINTS_PER_INTERACTION
                self.print_stats(final_stats)
            else:
                print(f"{self.print_timestamp()} {Fore.RED}Warning: Interaction may not have been recorded{Style.RESET_ALL}")
        else:
            print(f"{self.print_timestamp()} {Fore.RED}Failed to report usage{Style.RESET_ALL}")

    def run(self):
        while True:
            print(f"{self.print_timestamp()} {Fore.GREEN}Starting AI interaction script with 24-hour limits (Press Ctrl+C to stop){Style.RESET_ALL}")
            print(f"{self.print_timestamp()} {Fore.CYAN}Daily Point Limit: {self.MAX_DAILY_POINTS} points ({self.MAX_DAILY_INTERACTIONS} interactions){Style.RESET_ALL}")
            print(f"{self.print_timestamp()} {Fore.CYAN}First reset will be at: {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
            
            with ThreadPoolExecutor(max_workers=len(self.wallet_addresses)) as executor:
                for wallet_index in range(len(self.wallet_addresses)):
                    wallet_address = self.wallet_addresses[wallet_index]
                    proxy = self.proxies[wallet_index % len(self.proxies)]
                    
                    for _ in range(20):  # 20 iterations per wallet
                        executor.submit(self.interact_with_ai, wallet_address, proxy)

                executor.shutdown(wait=True)

            print(f"{self.print_timestamp()} {Fore.YELLOW}All wallets have completed their iterations. Waiting for the next cycle...{Style.RESET_ALL}")
            self.wait_until_next_run()  # Wait until 9 AM WIB

    def wait_until_next_run(self):
        """Wait until the next run time (9 AM WIB)."""
        now = datetime.now()
        next_run_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now > next_run_time:
            next_run_time += timedelta(days=1)  # Move to the next day if it's already past 9 AM

        wait_seconds = (next_run_time - now).total_seconds()
        print(f"{self.print_timestamp()} {Fore.YELLOW}Waiting for {wait_seconds:.0f} seconds until next run at {next_run_time.strftime('%Y-%m-%d %H:%M:%S')} (WIB){Style.RESET_ALL}")
        time.sleep(wait_seconds)

def read_file_to_list(filename: str) -> List[str]:
    """Read a file and return a list of non-empty lines."""
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: {filename} not found.{Style.RESET_ALL}")
        return []

def main():
    print_banner = """
╔══════════════════════════════════════════════╗
║               KITE AI AUTOMATE               ║
║     Github: https://github.com/im-hanzou     ║
╚══════════════════════════════════════════════╝
    """
    print(Fore.CYAN + print_banner + Style.RESET_ALL)
    
    # Read wallet addresses from wallet.txt
    wallet_addresses = read_file_to_list('wallet.txt')
    if not wallet_addresses:
        print(f"{Fore.RED}No wallet addresses found. Exiting...{Style.RESET_ALL}")
        return
    
    # Read proxies from proxies.txt
    proxies = read_file_to_list('proxies.txt')
    if not proxies:
        print(f"{Fore.RED}No proxies found. Exiting...{Style.RESET_ALL}")
        return
    
    automation = KiteAIAutomation(wallet_addresses, proxies, max_iterations=20)
    automation.run()

if __name__ == "__main__":
    main()
