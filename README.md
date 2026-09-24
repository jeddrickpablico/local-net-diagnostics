# local-net-diagnostics

A small tool to track ping latency, packet loss, and listening ports across VMs in my home lab. A Bash script gathers the raw diagnostic output, and a Python script reads, parses, and structures the data.

## Todo / Roadmap

- [x] Initial repo setup and target host inventory
- [x] Bash collector with timeout flags and comment filtering (`collect_data.sh`)
- [x] Active socket checks (`ss -tln`) and log reset logic
- [x] Safe log ingestion and missing-file handling (`analyze_data.py`)
- [x] Parse ping stats and open ports using regex (handle edge-case outputs)
- [x] Clean up metrics and export to structured JSON
- [ ] Automate periodic runs using cron
- [ ] Add basic alerting for dropped hosts

## How to Run

```bash
# 1. Run the collector
chmod +x collect_data.sh
./collect_data.sh

# 2. Run the parser
python3 analyze_data.py
```

## Issues Encountered & Fixes

Notes on real-world bugs hit during testing and how they were resolved:

| Area | What Happened | The Fix |
| :--- | :--- | :--- |
| **Target Parsing** (`collect_data.sh`) | A basic `for target in $(cat targets.txt)` loop split lines on spaces, trying to ping individual words in comments (like `#` and `Local`) and throwing DNS errors. | Switched to `while read -r` and used `awk '{print $1}'` to isolate the IP address and skip comment lines. |
| **Ping Hangs** (`collect_data.sh`) | The script took too long on offline or firewalled lab IPs because the default ping waited too long for dropped packets. | Added `-W 1` to enforce a 1-second timeout per probe so the loop moves along quickly. |
| **Log Growth** (`raw_output.txt`) | Using `>>` for every command caused test data to stack up on every run, making the log file huge. | Changed the first timestamp write to `>` so the file clears fresh on every new execution. |
| **Port Visibility** (`collect_data.sh`) | The script only tested reachability, leaving zero visibility into what was actually running on the machine. | Added `ss -tln` to dump active local TCP sockets without waiting on reverse DNS lookups. |
| **Missing Log File** (`analyze_data.py`) | Running the Python script before running the Bash collector threw an unhandled `FileNotFoundError` crash. | Wrapped the file open in `try / except FileNotFoundError` to print a reminder to run `collect_data.sh` first, then cleanly exited with `sys.exit(1)`. |
| **Metric Extraction** (`analyze_data.py`) | Basic string splitting (`.split("%")` and `.split("time=")`) broke when VirtualBox VMs returned decimal packet loss (`0.0%` instead of `0%`) and threw `IndexError` crashes on offline hosts where `time=` never appeared in the output. | Swapped string splitting for `re.search()`. Used `r"(\d+(?:\.\d+)?)%\s*packet loss"` to catch both integer and decimal loss, and matched latency safely so missing strings on offline targets evaluate to `None` instead of crashing. |
