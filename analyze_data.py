import sys
import re

INPUT_FILE = "raw_output.txt"

def load_raw_data(filepath):
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"[ERROR] '{filepath}' was not found.")
        print("[HINT] Run './collect_data.sh' first to generate diagnostic logs.")
        sys.exit(1)

def parse_to_dict_basic(lines):
    # I need to tie these metrics to the actual IPs.
    # Setting up an empty dictionary to hold everything.
    results = {}
    current_ip = None
    
    # Grab the IP from the standard "PING 192.168.1.1" header line
    ip_pattern = r"PING\s+([a-zA-Z0-9.-]+)"
    loss_pattern = r"(\d+(?:\.\d+)?)%\s*packet loss"
    latency_pattern = r"time=([\d.]+)\s*ms"
    
    for line in lines:
        ip_match = re.search(ip_pattern, line)
        if ip_match:
            current_ip = ip_match.group(1)
            # Create a new blank dictionary for this specific IP
            results[current_ip] = {}
            
        # Only start looking for metrics if we actually found an IP first
        if current_ip:
            loss_match = re.search(loss_pattern, line)
            if loss_match:
                results[current_ip]["loss"] = f"{loss_match.group(1)}%"
                
            latency_match = re.search(latency_pattern, line)
            if latency_match:
                # Assign the latency to the dictionary
                results[current_ip]["latency"] = f"{latency_match.group(1)}ms"

    # Print the raw dictionary to see what we got
    print("--- Dictionary Dump ---")
    for ip, data in results.items():
        print(f"Host: {ip} -> {data}")

def main():
    print(f"[*] Loading network diagnostics from '{INPUT_FILE}'...")
    raw_lines = load_raw_data(INPUT_FILE)
    print(f"[+] Loaded {len(raw_lines)} lines of raw data.")
    
    parse_to_dict_basic(raw_lines)

if __name__ == "__main__":
    main()
