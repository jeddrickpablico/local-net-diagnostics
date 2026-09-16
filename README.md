# Local Network Diagnostic Pipeline

A lightweight Bash and Python project to check host reachability and open ports across my virtual lab machines. 

The goal is to collect raw network test data using a shell script, then use Python to parse the results and highlight connection drops.

## Current Progress & Next Steps
- [x] Initialize repository and configure `.gitignore`
- [x] Create Bash probe to ping lab IPs and handle timeout/comment issues (`collect_data.sh`)
- [ ] Add local listening port checks with `ss -tln`
- [ ] Build Python parser to extract latency and packet loss (`analyze_data.py`)
- [ ] Generate structured JSON reports and log unreachable hosts

## How to Run (Work in Progress)
```bash
# Make collector executable and run
chmod +x collect_data.sh
./collect_data.sh
