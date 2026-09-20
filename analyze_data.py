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

def extract_metrics(lines):
    print("--- Regex Parsing Output ---")
    
    # Standard ping returns whole numbers like 0%, but some of my VirtualBox VMs 
    # return 0.0% packet loss instead. 
    # The (?:\.\d+)? part in this regex makes the decimal optional so it catches both.
    loss_pattern = r"(\d+(?:\.\d+)?)%\s*packet loss"
    
    # Grabs the actual ms value from the ping response.
    latency_pattern = r"time=([\d.]+)\s*ms"
    
    for line in lines:
        loss_match = re.search(loss_pattern, line)
        if loss_match:
            print(f"Packet Loss: {loss_match.group(1)}%")
            
        # Switching to re.search here instead of my old string splits.
        # If a host in my targets.txt is completely offline, the 'time=' string 
        # won't even exist in the log. Since re.search just returns None if it fails, 
        # this stops the script from crashing.
        latency_match = re.search(latency_pattern, line)
        if latency_match:
            print(f"Latency: {latency_match.group(1)}ms")

def main():
    print(f"[*] Loading network diagnostics from '{INPUT_FILE}'...")
    raw_lines = load_raw_data(INPUT_FILE)
    print(f"[+] Loaded {len(raw_lines)} lines of raw data.")
    
    extract_metrics(raw_lines)

if __name__ == "__main__":
    main()
