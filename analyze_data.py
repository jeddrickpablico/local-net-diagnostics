import sys
import re

INPUT_FILE = "raw_output.txt"

def load_raw_data(filepath):
    # Try to open the file first. If the bash script hasn't run yet, 
    # this stops a massive FileNotFoundError stack trace and just prints a reminder.
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"[ERROR] '{filepath}' was not found.")
        print("[HINT] Run './collect_data.sh' first to generate diagnostic logs.")
        sys.exit(1)

def parse_to_dict(lines):
    results = {}
    current_ip = None
    
    ip_pattern = r"PING\s+([a-zA-Z0-9.-]+)"
    # The optional decimal part (?:\.\d+)? catches both standard 0% and my VirtualBox 0.0% outputs
    loss_pattern = r"(\d+(?:\.\d+)?)%\s*packet loss"
    # Grabs the actual ms value safely.
    latency_pattern = r"time=([\d.]+)\s*ms"
    
    for line in lines:
        ip_match = re.search(ip_pattern, line)
        if ip_match:
            current_ip = ip_match.group(1)
            # Because ping outputs 3 separate lines for latency, assigning it directly just 
            # overwrites itself 3 times. Making it a list so I can collect them and average them later.
            results[current_ip] = {"loss": None, "latencies": [], "status": "unknown"}
            
        if current_ip:
            loss_match = re.search(loss_pattern, line)
            if loss_match:
                loss_val = float(loss_match.group(1))
                results[current_ip]["loss"] = f"{loss_val}%"
                
                # If a host drops 100% of packets, flag it as offline right away
                # so we don't crash trying to do math on an empty latency list.
                if loss_val == 100.0:
                    results[current_ip]["status"] = "offline"
                else:
                    results[current_ip]["status"] = "online"
                
            latency_match = re.search(latency_pattern, line)
            if latency_match:
                # Append the float to the list instead of overwriting the key
                results[current_ip]["latencies"].append(float(latency_match.group(1)))

    print("--- Final Structured Metrics ---")
    for ip, data in results.items():
        # Calculate the average if the list actually has data
        if data["latencies"]:
            avg_lat = sum(data["latencies"]) / len(data["latencies"])
            data["avg_latency"] = f"{avg_lat:.2f}ms"
        else:
            data["avg_latency"] = "N/A"
            
        # Delete the raw list from the dictionary so the final data structure is clean
        del data["latencies"]
        
        print(f"[{data['status'].upper()}] {ip} | Loss: {data['loss']} | Avg Latency: {data['avg_latency']}")

def main():
    print(f"[*] Loading network diagnostics from '{INPUT_FILE}'...")
    raw_lines = load_raw_data(INPUT_FILE)
    print(f"[+] Loaded {len(raw_lines)} lines of raw data.")
    
    parse_to_dict(raw_lines)

if __name__ == "__main__":
    main()