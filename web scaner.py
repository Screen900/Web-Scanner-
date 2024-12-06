import requests
import re
import pyfiglet
import socket
from datetime import datetime
import os
import json

# تعريف الألوان
class bcolors:
    GREEN = '\033[32m'
    CYAN = '\033[36m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    RED = '\033[31m'
    RESET = '\033[0m'

class VulnerabilityScanner:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.vulnerabilities = []

    def check_internet(self):
        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            return False

    def is_valid_url(self, url):
        # التحقق من صحة الرابط باستخدام تعبير منتظم
        pattern = re.compile(
            r"^(http://|https://)"
            r"((([a-zA-Z0-9\-_]+\.)+[a-zA-Z]{2,})|"
            r"localhost|"
            r"(\d{1,3}\.){3}\d{1,3})"
            r"(:\d+)?(/.*)?$"
        )
        return bool(pattern.match(url))

    def check_sql_injection(self):
        payload = "' OR '1'='1"
        try:
            response = requests.get(f"{self.url}?test={payload}")
            if "syntax error" in response.text.lower() or response.status_code == 500:
                self.vulnerabilities.append("SQL Injection")
        except requests.RequestException:
            pass

    def check_xss(self):
        payload = "<script>alert('XSS')</script>"
        try:
            response = requests.get(f"{self.url}?q={payload}")
            if payload in response.text:
                self.vulnerabilities.append("Cross-Site Scripting (XSS)")
        except requests.RequestException:
            pass

    def check_lfi(self):
        payload = "/../../../../etc/passwd"
        try:
            response = requests.get(f"{self.url}{payload}")
            if "root:" in response.text:
                self.vulnerabilities.append("Local File Inclusion (LFI)")
        except requests.RequestException:
            pass

    def check_rfi(self):
        payload = "?file=http://example.com/malicious.txt"
        try:
            response = requests.get(f"{self.url}{payload}")
            if "malicious.txt" in response.text:
                self.vulnerabilities.append("Remote File Inclusion (RFI)")
        except requests.RequestException:
            pass

    def check_ssrf(self):
        payload = "?url=http://localhost:80"
        try:
            response = requests.get(f"{self.url}{payload}")
            if "localhost" in response.text:
                self.vulnerabilities.append("Server-Side Request Forgery (SSRF)")
        except requests.RequestException:
            pass

    def save_report(self):
        report = {
            "url": self.url,
            "vulnerabilities": self.vulnerabilities,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open("vulnerability_report.json", "w") as file:
            json.dump(report, file, indent=4)
        print(f"{bcolors.YELLOW}✅ Report saved to 'vulnerability_report.json'{bcolors.RESET}")

    def display_results(self):
        if self.vulnerabilities:
            print(f"\n{bcolors.GREEN}Detected Vulnerabilities:{bcolors.RESET}")
            for vuln in self.vulnerabilities:
                print(f"{bcolors.RED}- {vuln}{bcolors.RESET}")
        else:
            print(f"\n{bcolors.GREEN}No vulnerabilities detected.{bcolors.RESET}")

    def run_scanner(self):
        print(f"\n{bcolors.YELLOW}Starting scan...{bcolors.RESET}")
        self.check_sql_injection()
        self.check_xss()
        self.check_lfi()
        self.check_rfi()
        self.check_ssrf()
        print(f"\n{bcolors.CYAN}Scan completed!{bcolors.RESET}")
        self.display_results()
        save = input(f"\n{bcolors.YELLOW}Do you want to save the report? (yes/no): {bcolors.RESET}").strip().lower()
        if save == "yes":
            self.save_report()


def main():
    os.system("clear" if os.name == "posix" else "cls")
    ascii_art = pyfiglet.figlet_format("w s")
    print(f"{bcolors.MAGENTA}{ascii_art}{bcolors.RESET}")
    print(f"{bcolors.CYAN}[INFO] Advanced Vulnerability Scanner by Screen{bcolors.RESET}\n")
    print(2*"========================")
    print()

    while True:
        url = input(f"{bcolors.YELLOW}Enter website URL (e.g., http://example.com): {bcolors.RESET}").strip()
        scanner = VulnerabilityScanner(url)

        if not scanner.is_valid_url(url):
            print(f"{bcolors.RED}❌ Invalid URL. Please enter a valid URL.{bcolors.RESET}")
            continue 
        if not scanner.check_internet():
            print(f"{bcolors.RED}❌ No internet connection. Please check your connection.{bcolors.RESET}")
            return

        scanner.run_scanner()
        break


if __name__ == "__main__":
    main()