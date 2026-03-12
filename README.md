# EzScriber

**EzScriber** is a batch-processing tool designed to automate the transcription of audio archives stored on Google Drive. It is optimized for efficiency, accuracy, and low-resource environments, making it ideal for oral history projects and community archives focused on "animating" cultural heritage.

## 🛠️ Quick Start
1. **Repository**: `https://github.com/mdotslash/ez-scriber`
2. **Setup**: 
   ```bash
   pip install -r requirements.txt
   
---

## 🚀 Key Features

* **Cloud-to-Local Workflow**: Automatically scans Google Drive folder structures to identify and process audio files in `.wav`, `.mp3`, and `.m4a` formats.
* **M1 Max & CPU Optimization**: Utilizes the **Faster-Whisper** engine with `int8` quantization for high-speed transcription without requiring a dedicated GPU.
* **Smart Silence Filtering**: Employs **Voice Activity Detection (VAD)** to intelligently skip periods of silence or background hiss, which is essential for processing old field recordings or tape archives.
* **Disk-Space Preservation**: Built specifically for systems with limited storage (e.g., 3GB), it uses a "Download-Process-Delete" cycle to ensure only one audio file exists locally at any given time.
* **Automated Archival Manifest**: Generates a master `_Archive_Manifest.csv` alongside timestamped `.txt` transcripts to provide a searchable index of the entire collection.

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mdotslash/ez-scriber.git
   cd ez-scriber
   ```

2. **Install dependencies:**
   It is recommended to use a [virtual environment](https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-virtualenv-with-Python-3). I honestly don't know why, but like this is how I got it to work on my ancient MacBook. 
   
You can install all required libraries (Faster-Whisper, gdown, tqdm) using the provided requirements.txt file:

   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

1. **Configure the script:** Open EzScriber.py and update the FOLDER_URL variable with your Google Drive folder link.

2. **Set Google Drive Permissions:** Ensure the Google Drive folder is shared with "Anyone with the link" set to "Viewer".

3. **Run EzScriber:** 
   ```bash
   python EzScriber.py
   ```

All finished transcripts and the master `_Archive_Manifest.csv` will be saved in a directory named "Transcripts_Raw_Archive".

## ⚖️ License
This project is released under the **EzScriber: Social Equity & Reparations License (v1.1)**.

**The Reparations Clause:** If you identify as white (or as a person of proximity to systemic whiteness) and choose to remix or redistribute this code, you are required to make a one-time donation of at least $40 (USD) to an organization supporting Black women in technology, media, or the arts.

**Attribution:** You must credit the original project and the Shirley Ann Griffin-Martin Archive.

**Non-Commercial:** This code may not be used for commercial profit without express written consent.

**ShareAlike:** All adaptations must be released under this same license.

See the full _LICENSE.txt_ file for complete terms and suggested organizations for donations.

