# PHANTOM-IG CORE v18.6: THE SENTINEL

### Autonomous Media Extraction and Neural Activity Monitoring System

**Developer:** cappiavi

**Engine:** v18.6 Sentinel

**License:** MIT

---

## 1. Project Overview

Phantom-IG Core is a specialized Python-based archival tool designed for high-resilience media extraction. Unlike basic scrapers that often trigger security flags, the Sentinel engine focuses on stealth and data integrity. It is built to handle large-scale profile backups while maintaining a low-profile footprint on target servers.

Standard tools fail when network conditions fluctuate or when platforms update their security headers. This project was developed to provide a resilient alternative that self-corrects in real-time.

---

## 2. Key Features

* **Adaptive Jitter:** Uses Gaussian distribution for delays, making requests appear human-like and non-patterned.
* **SQL Manifest System:** A local SQLite3 database tracks every download. This ensures zero redundancy as the script does not download the same file twice.
* **Neural Activity Feed:** A high-speed, live-updating dashboard that monitors success rates and server latency.
* **Heartbeat Sentinel:** Automatically pauses extraction if internet connectivity is lost, resuming only when the uplink is verified.
* **Automated Metadata Purge:** Keeps storage clean by removing temporary JSON and TXT bloat after verification.

---

## 3. Technical Architecture

The system operates on a multi-layer logic gate:

1. **Validation Layer:** Performs a handshake with the target profile to ensure accessibility.
2. **Manifest Layer:** Queries citadel_manifest.db to skip existing shortcodes.
3. **Extraction Layer:** Pulls high-resolution media using injected X-IG-App-ID headers.
4. **Verification Layer:** Confirms file integrity and logs the success to the side panel.

---

## 4. Setup Instructions

### Prerequisites

* Python 3.10 or higher
* Pip package manager

### Installation

Open the terminal and run the following command to install the required dependencies:

```bash
pip install instaloader rich requests

```

### Running the Engine

1. Navigate to the project folder.
2. Launch the script:
```bash
python sentinel.py

```


3. Enter the Target Username when prompted.

---

## 5. Side Panel Diagnostics

The Core Monitor provides real-time stats to help manage long sessions:

| Statistic | Description |
| --- | --- |
| **Net Health** | Real-time uplink status. Red indicates the engine is in Cryostasis waiting for network. |
| **Success Rate** | Calculated percentage of successful pulls versus errors. |
| **Server Latency** | Response time from the host. High latency indicates potential throttling. |
| **Throttle Risk** | A calculated risk level based on server response patterns. |

---

## 6. Troubleshooting

* **Throttling (429):** If the log shows LIMIT REACHED, the Sentinel will automatically initiate a backoff timer. Leave the script running as it will resume once the cooldown expires.
* **Database Locked:** Ensure only one instance of the script is running. The SQLite manifest can only be accessed by one engine at a time.
* **Network Offline:** The script will pause. Check the router or VPN connection.

---

## 7. MIT License

Copyright (c) 2026 cappiavi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."# PHANTOM-IG-CORE" 
