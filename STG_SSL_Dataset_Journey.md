# STG-SSL Dataset Collection Journey — Full Summary

## What This Project Is About
Building a labeled network traffic dataset to train the **STG-SSL model** — a research paper that classifies network traffic using:
- **Graph structure** (flows connected by shared endpoints)
- **Temporal dynamics** (how traffic changes over time)
- **Semi-supervised learning** (works with very few labels)

No previous research combined all three. STG-SSL fills that gap.

---

## Tools Used
| Tool | Purpose |
|---|---|
| **Wireshark** | Capture raw network traffic as .pcapng files |
| **Python 3.10** | Run the conversion script |
| **Scapy** | Read pcapng files and extract flow features |
| **Pandas** | Combine and save data as CSV |
| **VS Code** | Write and run Python scripts |

---

## Step 1 — Captured 6 Labeled Traffic Sessions with Wireshark

For each session:
1. Opened Wireshark → selected Wi-Fi interface
2. Double clicked Wi-Fi to start capture
3. Performed one activity at a time
4. Stopped capture → saved as .pcapng file

### Sessions Collected
| # | Activity | File Name | Label |
|---|---|---|---|
| 1 | Watched YouTube | youtube_session1.pcapng | YouTube |
| 2 | Zoom/Meet call | zoom_session1.pcapng | Zoom |
| 3 | Normal browsing | browsing_session1.pcapng | Browsing |
| 4 | Speedtest.net (3-4 runs) | download_session1.pcapng | Download |
| 5 | Browser game (poki.com) | gaming_session1.pcapng | Gaming |
| 6 | PC idle, no activity | idle_session1.pcapng | Idle |

**Rules followed:**
- Each session = 5+ minutes
- One activity at a time (no mixing)
- All files saved in one folder: `C:\Users\midya\Desktop\Dataset\`

---

## Step 2 — Converted Packets to Flow Features Using Python

### Why Scapy (not nfstream or CICFlowMeter)
- nfstream had a DLL error on both Python 3.13 and 3.10 (Windows issue)
- CICFlowMeter requires complex setup
- Scapy is pure Python — works perfectly on Windows, no DLL issues

### Install Command Used
```
py -3.10 -m pip install scapy pandas
```

### Script Created
File: `create_dataset.py` inside the `Dataset` folder

The script:
1. Reads each .pcapng file using Scapy
2. Groups packets into flows (by 5-tuple: src IP, dst IP, src port, dst port, protocol)
3. Extracts flow features for each flow
4. Adds the correct label
5. Combines all 6 sessions into one CSV file

### Run Command
```
py -3.10 create_dataset.py
```

### To Stop Script Anytime
```
Ctrl + C
```

---

## Step 3 — Final Dataset: my_dataset.csv

Location: `C:\Users\midya\Desktop\Dataset\my_dataset.csv`

### Features Extracted Per Flow
| Feature | Description |
|---|---|
| src_ip | Source IP address |
| dst_ip | Destination IP address |
| src_port | Source port number |
| dst_port | Destination port number |
| protocol | TCP / UDP / OTHER |
| packet_count | Number of packets in flow |
| total_bytes | Total bytes transferred |
| mean_packet_size | Average packet size |
| min_packet_size | Smallest packet |
| max_packet_size | Largest packet |
| flow_duration | How long the flow lasted (seconds) |
| mean_iat | Average time between packets |
| min_iat | Minimum inter-arrival time |
| max_iat | Maximum inter-arrival time |
| start_time | When the flow started (timestamp) |
| label | YouTube / Zoom / Browsing / Download / Gaming / Idle |

---

## What Comes Next (Remaining Steps)

### Step 2 — Build Temporal Traffic Graph
From `my_dataset.csv`, build the graph as described in the STG-SSL paper:
- **Spatial edges** — connect flows that share common endpoints within a time window
- **Temporal edges** — connect same endpoint pairs across consecutive time windows
- Time window = 60 seconds each

### Step 3 — Train STG-SSL Model
- Spatial GNN layer (GATv2 with attention)
- Temporal attention layer (across windows)
- Gated fusion (combine spatial + temporal)
- Three semi-supervised mechanisms:
  1. Graph-based label propagation
  2. Pseudo-labeling
  3. Temporal consistency regularization

---

## Key Lessons Learned
- Always capture one activity at a time for clean labels
- Python 3.10 is the safest version for ML libraries on Windows
- Scapy is the most reliable pcapng reader on Windows
- `start_time` column is critical for building temporal graph later
- Collect 500-1000+ flows per label for good training results

---

## Quick Reference — Folder Structure
```
C:\Users\midya\Desktop\Dataset\
├── youtube_session1.pcapng
├── zoom_session1.pcapng
├── browsing_session1.pcapng
├── download_session1.pcapng
├── gaming_session1.pcapng
├── idle_session1.pcapng
├── create_dataset.py
└── my_dataset.csv  ← FINAL DATASET
```
