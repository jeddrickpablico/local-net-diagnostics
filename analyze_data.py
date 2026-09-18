import sys

INPUT_FILE = "raw_output.txt"

def load_raw_data(filepath):
    """
    Safely reads raw network output.
    Exits cleanly if the collector has not yet been executed.
    """
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"[ERROR] '{filepath}' was not found.")
        print("[HINT] Run './collect_data.sh' first to generate diagnostic logs.")
        sys.exit(1)

def main():
    print(f"[*] Loading network diagnostics from '{INPUT_FILE}'...")
    raw_lines = load_raw_data(INPUT_FILE)
    print(f"[+] Loaded {len(raw_lines)} lines of raw data.")
    print("[*] Ready for metric parsing.")

if __name__ == "__main__":
    main()
