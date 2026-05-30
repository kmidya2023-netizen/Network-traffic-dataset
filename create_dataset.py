from scapy.all import rdpcap, IP, TCP, UDP
import pandas as pd
import os
from collections import defaultdict

sessions = {
    "youtube_session1.pcapng":  "YouTube",
    "meet_session1.pcapng":     "Meet",
    "browsing_session1.pcapng": "Browsing",
    "download_session1.pcapng": "Download",
    "gaming_session1.pcapng":   "Gaming",
    "idle_session1.pcapng":     "Idle",
}

def extract_flows(filepath, label):
    print(f"Reading {filepath}...")
    packets = rdpcap(filepath)
    flows = defaultdict(list)

    for pkt in packets:
        if IP not in pkt:
            continue
        proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "OTHER"
        src = pkt[IP].src
        dst = pkt[IP].dst
        sport = pkt[TCP].sport if TCP in pkt else (pkt[UDP].sport if UDP in pkt else 0)
        dport = pkt[TCP].dport if TCP in pkt else (pkt[UDP].dport if UDP in pkt else 0)
        key = (src, dst, sport, dport, proto)
        flows[key].append((float(pkt.time), len(pkt)))

    rows = []
    for (src, dst, sport, dport, proto), pkts in flows.items():
        times = [t for t, _ in pkts]
        sizes = [s for _, s in pkts]
        iats = [times[i+1]-times[i] for i in range(len(times)-1)] or [0]
        rows.append({
            "src_ip": src, "dst_ip": dst,
            "src_port": sport, "dst_port": dport,
            "protocol": proto,
            "packet_count": len(pkts),
            "total_bytes": sum(sizes),
            "mean_packet_size": round(sum(sizes)/len(sizes), 2),
            "min_packet_size": min(sizes),
            "max_packet_size": max(sizes),
            "flow_duration": round(max(times)-min(times), 4),
            "mean_iat": round(sum(iats)/len(iats), 6),
            "min_iat": round(min(iats), 6),
            "max_iat": round(max(iats), 6),
            "start_time": min(times),
            "label": label
        })
    return rows

all_rows = []
for filename, label in sessions.items():
    if not os.path.exists(filename):
        print(f"WARNING: {filename} not found, skipping...")
        continue
    rows = extract_flows(filename, label)
    all_rows.extend(rows)
    print(f"  {label}: {len(rows)} flows extracted")

df = pd.DataFrame(all_rows)
df.to_csv("my_dataset.csv", index=False)
print(f"\nDataset saved as my_dataset.csv")
print(f"Total flows: {len(df)}")
print(df["label"].value_counts())