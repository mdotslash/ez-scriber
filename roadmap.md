# 🗺️ EzScriber Roadmap

Welcome to the future development roadmap for **EzScriber**. This document outlines planned features, performance optimizations, and architectural upgrades designed to make this tool even more powerful for archivists, researchers, and oral historians.

---

## 🌟 Phase 1: Expanded Configurations & Accuracy (High Priority)
The next immediate updates will focus on giving users more control over their source files and the AI's transcription accuracy.

### 1. Local Archive Support
* **Feature:** Add a configuration toggle to process a local directory instead of a Google Drive URL.
* **Use Case:** For archivists working with highly sensitive files that cannot be uploaded to the cloud, or for users working entirely offline. 

### 2. Cultural Context & Custom Glossaries
* **Feature:** Implement a `--language` selector and a Custom Glossary loader (`.txt` or `.csv`).
* **Use Case:** Oral histories often contain specific regional slang, indigenous names, or highly specific historical terminology. By feeding a custom vocabulary list into the Whisper engine's `initial_prompt`, the AI can be biased to recognize and correctly spell non-standard words, significantly reducing manual editing.

### 3. "HQ Mode" (Maximum Accuracy)
* **Feature:** A simple `[H]Q` toggle at the start menu that overrides standard speed optimizations.
* **Use Case:** For final archival preservation where time is not an issue, but absolute accuracy is.
* **Technical Implementation:**
  * Upgrade the active model from `base` to `large-v3`.
  * Increase the `beam_size` (e.g., from 5 to 10) for deeper AI contextual searching.
  * Adjust the `compute_type` to leverage maximum M1 memory for precision rather than speed.

---

## 🛠️ Phase 2: Resilience & Architecture
These updates focus on the stability and efficiency of the pipeline, especially when handling massive, multi-hour archival files.

### 1. Mid-File Checkpointing (The "Safety Net")
* **Feature:** Periodically write transcription progress to the local disk every 5–10 minutes instead of waiting for the entire audio file to finish.
* **Use Case:** Prevents catastrophic data loss if a computer goes to sleep, loses battery, or crashes at minute 119 of a 120-minute tape.

### 2. The "Warm Cache" Test Pipeline
* **Feature:** Retain the downloaded audio file when running a "Test" (5-minute clip). If the user subsequently chooses to run the "Full" transcription of that same file, the script will process the local file instead of re-downloading it from the cloud.
* **Use Case:** Saves time and internet bandwidth, creating a seamless bridge between QA testing and full production.

### 3. Advanced VAD (Voice Activity Detection) Tuning
* **Feature:** Expose VAD parameters (like `min_silence_duration_ms`) to the user.
* **Use Case:** Archival tape often features long stretches of analog hiss or room tone. Aggressive VAD tuning allows the AI to rapidly skip over these dead zones, drastically reducing processing time on older field recordings.

---

## 🚀 Phase 3: High-Performance Processing
Optimizations meant specifically for Apple Silicon (M-series) and multi-core machines.

### 1. Asynchronous Pipelining (Producer-Consumer)
* **Feature:** Separate the download and transcription processes into separate threads. 
* **Use Case:** While the AI is busy transcribing "Track 1", the script will silently download "Track 2" in the background. Once Track 1 is finished, Track 2 is immediately ready for the AI, eliminating internet-bottleneck waiting periods.

---

*Want to contribute to any of these features? Reach out through my website MayowaTomori.com*