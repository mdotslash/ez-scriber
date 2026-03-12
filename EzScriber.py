"""
EZSCRIBER: Automated Archival Transcription
Repository: https://github.com/mdotslash/ez-scriber

This script automates the transcription of audio files stored in Google Drive.
It is optimized for Apple Silicon (M1/M2/M3) using Faster-Whisper with 
int8 quantization and multi-threading.
"""

import os
import gdown
import csv
import time
import traceback
import re
from tqdm import tqdm
from faster_whisper import WhisperModel

# ==========================================
# EZSCRIBER: CONFIGURATION
# ==========================================

# 1. PASTE YOUR GOOGLE DRIVE FOLDER URL HERE.
# IMPORTANT: The folder must be set to "Anyone with the link can view".
FOLDER_URL = "YOUR_GOOGLE_DRIVE_FOLDER_URL_HERE"

# 2. CHOOSE YOUR MODEL SIZE. 
# Options: "tiny", "base", "small", "medium", "large-v3".
# "base" is recommended for M1/M2/M3 Macs for optimal speed.
MODEL_SIZE = "base"

# 3. DIRECTORY SETTINGS
OUTPUT_DIR = "Transcripts_Raw_Archive"
TEST_DIR = os.path.join(OUTPUT_DIR, "TEST_SAMPLES")
TEST_LIMIT_SEC = 300 

def clean_filename(name):
    """Removes special characters to ensure filesystem compatibility."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def run_ezscriber_production_v3():
    print("\n" + "="*55)
    print("       EZSCRIBER v3: PRODUCTION ARCHIVAL ENGINE")
    print("="*55)
    
    # --- STEP 1: SCAN AND AUDIT ---
    try:
        print("Checking Google Drive and local archive status...")
        files = gdown.download_folder(FOLDER_URL, quiet=True, skip_download=True)
        audio_files = [f for f in files if f.path.lower().endswith(('.wav', '.mp3', '.m4a'))]
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEST_DIR, exist_ok=True)
    
    pending_files = []
    for f in audio_files:
        parent_folder = clean_filename(os.path.basename(os.path.dirname(f.path)))
        raw_filename = clean_filename(os.path.basename(f.path))
        clean_base = f"{parent_folder}_{os.path.splitext(raw_filename)[0]}"
        
        # RESUME LOGIC: Skip if transcript already exists
        if not os.path.exists(os.path.join(OUTPUT_DIR, f"{clean_base}.txt")):
            pending_files.append(f)

    print(f"📊 STATUS: {len(audio_files)} files in cloud | {len(pending_files)} pending.")
    
    if not pending_files:
        print("\n✅ All files are already transcribed.")
        return

    # --- STEP 2: USER INTERACTION ---
    choice = input(f"\n[T]est (5 min samples) | [F]ull (Transcribe Archive): ").strip().lower()
    is_test = choice == 't'

    # --- STEP 3: INITIALIZE AI MODEL ---
    print(f"\nLoading '{MODEL_SIZE}' AI engine...")
    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8", cpu_threads=8)

    # --- STEP 4: PROCESSING LOOP ---
    files_to_process = pending_files[:2] if is_test else pending_files
    master_pbar = tqdm(total=len(files_to_process), desc="TOTAL PROGRESS", unit="file", position=0)
    
    for f_info in files_to_process:
        file_id = f_info.id
        raw_filename = clean_filename(os.path.basename(f_info.path))
        parent_folder = clean_filename(os.path.basename(os.path.dirname(f_info.path)))
        clean_base = f"{parent_folder}_{os.path.splitext(raw_filename)[0]}"
        
        transcript_path = os.path.join(TEST_DIR if is_test else OUTPUT_DIR, f"{'_PARTIAL_' if is_test else ''}{clean_base}.txt")

        local_path = None
        try:
            if os.path.exists(raw_filename): os.remove(raw_filename)

            # A. DOWNLOAD
            local_path = gdown.download(id=file_id, output=raw_filename, quiet=True)
            if not local_path or not os.path.exists(local_path):
                master_pbar.update(1)
                continue

            # B. TRANSCRIBE
            transcribe_args = {"beam_size": 5, "vad_filter": True, "vad_parameters": dict(min_silence_duration_ms=500)}
            if is_test: transcribe_args["clip_timestamps"] = [0, TEST_LIMIT_SEC]

            segments, info = model.transcribe(local_path, **transcribe_args)
            
            duration = min(info.duration, TEST_LIMIT_SEC) if is_test else info.duration
            file_pbar = tqdm(total=round(duration), unit="sec", desc=f" > Scribing: {raw_filename[:15]}", position=1, leave=False)
            
            lines = []
            for segment in segments:
                if is_test and segment.start > TEST_LIMIT_SEC: break
                file_pbar.update(round(segment.end - segment.start))
                m, s = divmod(int(segment.start), 60)
                h, m = divmod(m, 60)
                lines.append(f"[{h:02d}:{m:02d}:{s:02d}] {segment.text.strip()}")
            file_pbar.close()

            # C. SAVE
            with open(transcript_path, "w", encoding="utf-8") as f:
                header = "--- EZSCRIBER TEST ---" if is_test else "--- EZSCRIBER FULL ---"
                f.write(f"{header}\nSOURCE: {parent_folder}/{raw_filename}\n" + "="*45 + "\n\n")
                f.write("\n".join(lines))

            # D. CLEANUP
            if os.path.exists(local_path): os.remove(local_path)
            master_pbar.update(1)

        except Exception:
            traceback.print_exc() 
            if local_path and os.path.exists(local_path): os.remove(local_path)

    master_pbar.close()
    print(f"\n✅ DONE. View results in: {TEST_DIR if is_test else OUTPUT_DIR}")

if __name__ == "__main__":
    run_ezscriber_production_v3()
