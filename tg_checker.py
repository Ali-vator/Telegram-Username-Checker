import asyncio
import random
import string
import sys
import os
import re
import aiohttp
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class TelegramChecker:
    def __init__(self):
        self.base_url = "https://t.me/"
        self.output_file = "available_usernames.txt"
        self.chars = string.ascii_lowercase + string.digits + "_"
        self.edge_chars = string.ascii_lowercase + string.digits
        self.validator_pattern = re.compile(r'^[a-z0-9][a-z0-9_]{3,}[a-z0-9]$')

    def clear_screen(self):
        """Clears the terminal screen based on OS."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def validate_format(self, username: str) -> bool:
        """Checks strict syntax rules (min 5 chars, valid symbols)."""
        if len(username) < 5:
            return False
        return bool(self.validator_pattern.match(username))

    def generate_username(self, length: int) -> str:
        """Generates a random valid username."""
        if length < 5: length = 5
        middle_len = length - 2
        middle = ''.join(random.choice(self.chars) for _ in range(middle_len))
        start = random.choice(self.edge_chars)
        end = random.choice(self.edge_chars)
        return f"{start}{middle}{end}"

    async def check_username(self, session: aiohttp.ClientSession, username: str) -> str:
        """
        Advanced check:
        - 404 -> Available
        - 200 -> Checks Page Title. 
          If Title is generic 'Telegram: Contact @...', it is likely AVAILABLE.
          If Title is a user display name, it is TAKEN.
        """
        url = f"{self.base_url}{username}"
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 404:
                    return "available"
                
                elif response.status == 200:
                    # READ content to detect "False Taken"
                    text = await response.text()
                    
                    # Heuristic: If the page title is exactly the generic string, 
                    # Telegram is likely showing a placeholder for an unused/available username.
                    # We check for the specific meta tag content or title tag.
                    generic_title = f'<title>Telegram: Contact @{username}</title>'
                    
                    # Also check for the "tgme_page_extra" div which usually contains 
                    # "X subscribers" or "X members" or online status for REAL accounts.
                    has_extra_info = 'tgme_page_extra' in text

                    if generic_title in text and not has_extra_info:
                        return "available" # Corrected from False Taken
                    else:
                        return "taken"

                elif response.status == 429:
                    return "rate_limit"
                else:
                    return f"status_{response.status}"
        except Exception as e:
            return f"error: {str(e)}"

    def log_available(self, username: str):
        with open(self.output_file, "a") as f:
            f.write(f"{username}\n")

    async def process_queue(self, session, username, delay):
        status = await self.check_username(session, username)

        if status == "available":
            print(f"{Fore.GREEN}[AVAILABLE] {username}")
            self.log_available(username)
        elif status == "taken":
            print(f"{Fore.RED}[TAKEN]     {username}")
        elif status == "rate_limit":
            print(f"{Fore.YELLOW}[429] Rate limited. Sleeping for 15s...")
            await asyncio.sleep(15)
            return await self.process_queue(session, username, delay)
        else:
            print(f"{Fore.WHITE}[ERROR]     {username} ({status})")
        
        await asyncio.sleep(delay)

    async def run(self):
        self.clear_screen()
        print(Fore.CYAN + "=== Telegram Username Checker (Fixed Logic) ===\n")
        # 1. Global Config
        try:
            delay = float(input(Fore.WHITE + "Enter delay (rec. 1.0): "))
        except ValueError:
            delay = 1.0

        # 2. Mode Selection
        print(Fore.MAGENTA + "\nSelect Mode:")
        print(Fore.MAGENTA + "[1] Generate Random Usernames")
        print(Fore.MAGENTA + "[2] Check from a .txt File")
        mode = input(Fore.WHITE + "Choice (1 or 2): ").strip()

        async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
            
            # --- MODE 1: GENERATOR ---
            if mode == "1":
                try:
                    length = int(input(Fore.WHITE + "Enter length (min 5): "))
                    count_input = input(Fore.WHITE + "Count (or 'infinite'): ").strip().lower()
                    infinite = count_input == 'infinite'
                    count = 0 if infinite else int(count_input)
                except ValueError:
                    return

                print(Fore.YELLOW + f"\nStarting Generator... Saving to {self.output_file}\n")
                checked = 0
                while infinite or checked < count:
                    username = self.generate_username(length)
                    await self.process_queue(session, username, delay)
                    checked += 1

            # --- MODE 2: FILE CHECKER ---
            elif mode == "2":
                file_path = input(Fore.WHITE + "Enter file path: ").strip()
                if not os.path.exists(file_path):
                    print(Fore.RED + "File not found.")
                    return

                print(Fore.YELLOW + f"\nReading file... Saving to {self.output_file}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    for line in lines:
                        username = line.strip().split()[0].lower() # Handle lines with extra spaces
                        username = username.replace("@", "") # Remove @ if present
                        
                        if not self.validate_format(username):
                            print(f"{Fore.WHITE}[SKIPPED]   {username} (Invalid)")
                            continue

                        await self.process_queue(session, username, delay)
                        
                except Exception as e:
                    print(Fore.RED + f"Error: {e}")

        print(Fore.CYAN + "\nDone.")

if __name__ == "__main__":
    checker = TelegramChecker()
    try:
        asyncio.run(checker.run())
    except KeyboardInterrupt:
        sys.exit(0)