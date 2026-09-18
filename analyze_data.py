# Initial baseline: direct file read
INPUT_FILE = "raw_output.txt"

def load_raw_data(filepath):
    with open(filepath, "r") as file:
        return file.readlines()

def main():
    print(f"Reading {INPUT_FILE}...")
    lines = load_raw_data(INPUT_FILE)
    print(f"Read {len(lines)} lines successfully.")

if __name__ == "__main__":
    main()
