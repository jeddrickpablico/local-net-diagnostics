import sys
import re
import json

INPUT_FILE = "raw_output.txt"
OUTPUT_FILE = "metrics.json"

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
    # Restructured the main dictionary so it can hold both our ping targets 
    # and the local listening ports we gather from the ss command.
    results = {
        "local_ports": [],
        "targets": {}
    }
    current_ip = None
    
    # Regex patterns
    ip_pattern = r"PING\s+([a-zA-Z0-9.-]+)"
    loss_pattern = r"(\d+(?:\.\d+)?)%\s*packet loss"
    latency_pattern = r"time=([\d.]+)\s*ms"
    
    # Looks for lines starting with LISTEN, skips the IP, and grabs the port number after the colon
    port_pattern = r"LISTEN\s+\d+\s+\d+\s+\S+:(\d+)"
    
    for line in lines:
        # Check for open ports first
        port_match = re.search(port_pattern, line)
        if port_match:
            port = int(port_match.group(1))
            # Don't add duplicate ports if they show up on both IPv4 and IPv6
            if port not in results["local_ports"]:
                results["local_ports"].append(port)
                
        ip_match = re.search(ip_pattern, line)
        if ip_match:
            current_ip = ip_match.group(1)
            results["targets"][current_ip] = {"loss": None, "latencies": [], "status": "unknown"}
            
        if current_ip:
            loss_match = re.search(loss_pattern, line)
            if loss_match:
                loss_val = float(loss_match.group(1))
                results["targets"][current_ip]["loss"] = f"{loss_val}%"
                
                # Flag 100% loss as offline so we don't crash doing math on an empty list
                if loss_val == 100.0:
                    results["targets"][current_ip]["status"] = "offline"
                else:
                    results["targets"][current_ip]["status"] = "online"
                
            latency_match = re.search(latency_pattern, line)
            if latency_match:
                results["targets"][current_ip]["latencies"].append(float(latency_match.group(1)))

    # Console Output
    print(f"--- Found {len(results['local_ports'])} Active Local Ports ---")
    print(results['local_ports'])
    
    print("\n--- Final Structured Metrics ---")
    for ip, data in results["targets"].items():
        if data["latencies"]:
            avg_lat = sum(data["latencies"]) / len(data["latencies"])
            data["avg_latency"] = f"{avg_lat:.2f}ms"
        else:
            data["avg_latency"] = "N/A"
            
        del data["latencies"]
        print(f"[{data['status'].upper()}] {ip} | Loss: {data['loss']} | Avg Latency: {data['avg_latency']}")
        
    return results

def main():
    print(f"[*] Loading network diagnostics from '{INPUT_FILE}'...")
    raw_lines = load_raw_data(INPUT_FILE)
    print(f"[+] Loaded {len(raw_lines)} lines of raw data.")
    
    parsed_data = parse_to_dict(raw_lines)
    
    # Dumping the dictionary to a JSON file. 
    # Added indent=4 because without it, the file was just one massive unreadable line of text.
    with open(OUTPUT_FILE, "w") as f:
        json.dump(parsed_data, f, indent=4)
    print(f"\n[+] Exported nicely formatted metrics to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()