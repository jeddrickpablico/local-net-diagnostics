import sys

INPUT_FILE = "raw_output.txt"

def load_raw_data(filepath):
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"[ERROR] '{filepath}' was not found.")
        print("[HINT] Run './collect_data.sh' first to generate diagnostic logs.")
        sys.exit(1)

def extract_metrics_basic(lines):
    print("--- Basic Parsing Output ---")
    for line in lines:
        # Grabbing metrics using string splits.
        # This splits the line at the '%' sign, then grabs the number right before it.
        if "packet loss" in line:
            loss = line.split("%")[0].split(" ")[-1]
            print(f"Loss: {loss}%")
            
        # Split at 'time=' to grab the ms value. 
        if "time=" in line:
            latency = line.split("time=")[1].split(" ")[0]
            print(f"Latency: {latency}ms")

def main():
    print(f"[*] Loading network diagnostics from '{INPUT_FILE}'...")
    raw_lines = load_raw_data(INPUT_FILE)
    print(f"[+] Loaded {len(raw_lines)} lines of raw data.")
    
    extract_metrics_basic(raw_lines)

if __name__ == "__main__":
    main()
