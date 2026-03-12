import os
import gdown
import csv
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
# "base" is a great balance of speed and accuracy for most laptops.
MODEL_SIZE = "base"

def run_ezscriber_archive():
    print("--- EZSCRIBER: STARTING ARCHIVAL TRANSCRIPTION ---")
    
    # Initialize M1-Optimized / CPU-Optimized Model
    # "int8" compute type saves memory and runs efficiently on CPUs without needing a dedicated GPU.
    print(f"Loading '{MODEL_SIZE}' model...")
    model = WhisperModel(
        MODEL_SIZE, 
        device="cpu", 
        compute_type="int8", 
        cpu_threads=8
    )
    
    print("Scanning Google Drive folder structure...")
    try:
        # gdown fetches the file list without downloading the actual audio yet
        files = gdown.download_folder(FOLDER_URL, quiet=True, skip_download=True)
    except Exception as e:
        print(f"Error accessing Google Drive: {e}")
        print("Please ensure the folder is shared publically ('Anyone with the link can view').")
        return

    output_dir = "Transcripts_Raw_Archive"
    os.makedirs(output_dir, exist_ok=True)
    
    # Filter for standard audio formats
    audio_files = [f for f in files if f.path.lower().endswith(('.wav', '.mp3', '.m4a'))]
    total_files = len(audio_files)
    
    if total_files == 0:
        print("No audio files found in the provided folder.")
        return

    # MASTER PROGRESS BAR
    master_pbar = tqdm(total=total_files, desc="OVERALL ARCHIVE", unit="file", position=0)
    summary_data = []

    for i, f_info in enumerate(audio_files):
        file_id = f_info.id
        parent_folder = os.path.basename(os.path.dirname(f_info.path))
        raw_filename = os.path.basename(f_info.path)
        
        # Create a clean name for the text file
        clean_base = f"{parent_folder}_{os.path.splitext(raw_filename)[0]}"
        transcript_path = os.path.join(output_dir, f"{clean_base}.txt")

        # Skip if we already transcribed this file (useful if the script gets interrupted)
        if os.path.exists(transcript_path):
            master_pbar.update(1)
            continue

        local_path = None
        try:
            master_pbar.set_description(f"Working: {parent_folder}/{raw_filename}")
            
            # Step 1: Download the single audio file
            local_path = gdown.download(id=file_id, output=raw_filename, quiet=True)

            # Step 2: Transcribe with Voice Activity Detection (VAD)
            # VAD filters out long silences and tape hiss to speed up processing
            segments, info = model.transcribe(
                local_path, 
                beam_size=5, 
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            # Sub-progress bar for the current file being transcribed
            file_pbar = tqdm(total=round(info.duration), unit="sec", desc=" > Processing", position=1, leave=False)
            
            lines = []
            for segment in segments:
                file_pbar.update(round(segment.end - segment.start))
                # Format timestamps as [HH:MM:SS]
                m, s = divmod(int(segment.start), 60)
                h, m = divmod(m, 60)
                lines.append(f"[{h:02d}:{m:02d}:{s:02d}] {segment.text.strip()}")
            file_pbar.close()

            # Step 3: Save the Transcript
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(f"SOURCE FOLDER: {parent_folder}\n")
                f.write(f"SOURCE FILE: {raw_filename}\n")
                f.write("="*40 + "\n\n")
                f.write("\n".join(lines))

            # Log data for the final CSV manifest
            summary_data.append([parent_folder, raw_filename, f"{round(info.duration/60, 2)} mins"])

            # Step 4: Delete the audio file immediately to save disk space
            if os.path.exists(local_path):
                os.remove(local_path)
            
            master_pbar.update(1)

        except Exception as e:
            print(f"\n!! Error on {parent_folder}/{raw_filename}: {e}")
            # Ensure cleanup happens even if transcription fails
            if local_path and os.path.exists(local_path):
                os.remove(local_path)

    # Step 5: Generate the Final CSV Manifest
    csv_path = os.path.join(output_dir, "_Archive_Manifest.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Folder", "Filename", "Audio Duration"])
        writer.writerows(summary_data)

    master_pbar.close()
    print(f"\n✅ DONE. {total_files} files processed.")
    print(f"Results are saved in the '{output_dir}' folder.")

if __name__ == "__main__":
    run_ezscriber_archive()