# 🐍 Mini Python Projects

A curated collection of practical, beginner-friendly, and lightweight Python automation scripts and utilities designed to simplify everyday tasks — from media downloading and audio conversion to network tools and text animation.

[![GitHub Repo](https://img.shields.io/badge/GitHub-Audri--23%2FMini--Python--Projects-blue?logo=github)](https://github.com/Audri-23/Mini-Python-Projects)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Personal%20%26%20Educational%20Use-blue)](#-license--terms-of-use)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Projects Summary](#-projects-summary)
- [Detailed Project Guide](#-detailed-project-guide)
  - [1. Animate Text (`animate_text.py`)](#1-animate-text-animate_textpy)
  - [2. Instagram & X Media Downloader (`instagram_x_media_downloader.py`)](#2-instagram--x-media-downloader-instagram_x_media_downloaderpy)
  - [3. PDF Merger (`merge_pdf.py`)](#3-pdf-merger-merge_pdfpy)
  - [4. Background Remover (`remove_image_background.py`)](#4-background-remover-remove_image_backgroundpy)
  - [5. Text to Speech Converter (`text_to_speech.py`)](#5-text-to-speech-converter-text_to_speechpy)
  - [6. Language Translator (`translator.py`)](#6-language-translator-translatorpy)
  - [7. Wi-Fi Password Getter (`wifi_pass_getter.py`)](#7-wi-fi-password-getter-wifi_pass_getterpy)
  - [8. Wi-Fi Sharing QR Code Generator (`wifi_sharing_qrcode.py`)](#8-wi-fi-sharing-qr-code-generator-wifi_sharing_qrcodepy)
  - [9. Wi-Fi & Internet Speed Checker (`wifi_speed_checker.py`)](#9-wi-fi--internet-speed-checker-wifi_speed_checkerpy)
  - [10. YouTube Music Downloader (`yt_music_downloader.py`)](#10-youtube-music-downloader-yt_music_downloaderpy)
- [Getting Started](#-getting-started)
- [Requirements & Dependencies](#-requirements--dependencies)
- [Platform Compatibility & Notes](#-platform-compatibility--notes)
- [Contributing](#-contributing)
- [License & Terms of Use](#-license--terms-of-use)

---

## 🚀 Overview

Each script in this repository solves a distinct real-world problem in just a few lines of clean, readable code. Many scripts automatically install their required libraries on first run using `pip`, making them extremely quick and convenient to test.

---

## 📊 Projects Summary

| Script | Category | Primary Libraries | Description |
| :--- | :--- | :--- | :--- |
| [`animate_text.py`](animate_text.py) | Animation & Video | `manim` | Renders a high-definition write-on text animation video. |
| [`instagram_x_media_downloader.py`](instagram_x_media_downloader.py) | Media Downloader | `gallery-dl` | Downloads photos and videos from Instagram or X (Twitter) URLs. |
| [`merge_pdf.py`](merge_pdf.py) | Document Processing | `pypdf` | Combines multiple PDF files into a single merged document. |
| [`remove_image_background.py`](remove_image_background.py) | Image Processing | `rembg`, `pillow` | Removes the background from an image using AI and saves as transparent PNG. |
| [`text_to_speech.py`](text_to_speech.py) | Audio & Speech | `gTTS` | Converts user input text into spoken English audio (`.mp3`). |
| [`translator.py`](translator.py) | NLP & Translation | `googletrans` | Translates user input text into another language (default: Spanish). |
| [`wifi_pass_getter.py`](wifi_pass_getter.py) | Network & System | Built-in `subprocess` | Retrieves and displays saved Wi-Fi SSIDs and passwords on Windows. |
| [`wifi_sharing_qrcode.py`](wifi_sharing_qrcode.py) | Network & QR | `qrcode`, `pillow` | Generates a scannable QR code for instant mobile Wi-Fi connection. |
| [`wifi_speed_checker.py`](wifi_speed_checker.py) | Network & Utility | `speedtest-cli` | Measures real-time internet download and upload speeds in Mbps. |
| [`yt_music_downloader.py`](yt_music_downloader.py) | Audio & Video | `yt-dlp`, `static-ffmpeg` | Extracts and downloads audio from YouTube videos directly into high-quality MP3. |

---

## 🛠️ Detailed Project Guide

### 1. Animate Text ([`animate_text.py`](animate_text.py))
- **Description:** Utilizes the [Manim](https://www.manim.community/) animation engine to animate writing custom text on screen with smooth effects in high resolution (`-pqh`).
- **How to run:**
  ```bash
  python animate_text.py
  ```
- **Inputs:** Prompts you for the text string you wish to animate.
- **Output:** Outputs a high-definition video rendering of the animated text.

---

### 2. Instagram & X Media Downloader ([`instagram_x_media_downloader.py`](instagram_x_media_downloader.py))
- **Description:** Uses [`gallery-dl`](https://github.com/mikf/gallery-dl) to extract and download media files (images, clips) from supported social media platforms like Instagram and Twitter/X.
- **How to run:**
  ```bash
  python instagram_x_media_downloader.py
  ```
- **Inputs:** Paste any valid Instagram or X/Twitter post link when prompted.
- **Output:** Media files are saved into the auto-created `gallery-dl/` folder.

---

### 3. PDF Merger ([`merge_pdf.py`](merge_pdf.py))
- **Description:** Merges multiple PDF files into one continuous document using the modern `pypdf` library.
- **How to run:**
  1. Place your target PDFs in the project folder (named `file1.pdf`, `file2.pdf`, `file3.pdf`, or edit the list in the script).
  2. Execute:
     ```bash
     python merge_pdf.py
     ```
- **Output:** Generates `merged.pdf` containing all merged pages.

---

### 4. Background Remover ([`remove_image_background.py`](remove_image_background.py))
- **Description:** Automatically detects and isolates subjects in photos to remove backgrounds with precision using machine learning via `rembg`.
- **How to run:**
  1. Place an image named `remove.jpg` in the script directory (or adjust `input_path`).
  2. Run:
     ```bash
     python remove_image_background.py
     ```
- **Output:** Saves the transparent output image as `removed.png`.

---

### 5. Text to Speech Converter ([`text_to_speech.py`](text_to_speech.py))
- **Description:** Converts plain English text to high-quality synthesized speech using the Google Text-to-Speech (`gTTS`) API.
- **How to run:**
  ```bash
  python text_to_speech.py
  ```
- **Inputs:** Prompts for the text content and desired MP3 file name.
- **Output:** An `.mp3` audio file saved in the current directory.

---

### 6. Language Translator ([`translator.py`](translator.py))
- **Description:** Translates sentences or paragraphs across languages using the Google Translate API wrapper `googletrans`.
- **How to run:**
  ```bash
  python translator.py
  ```
- **Inputs:** Prompts for text input.
- **Output:** Prints the translated text in the terminal (default destination language is Spanish, `es`).

---

### 7. Wi-Fi Password Getter ([`wifi_pass_getter.py`](wifi_pass_getter.py))
- **Description:** Uses Windows native `netsh wlan` shell commands to discover all saved wireless profiles and their cleartext passwords.
- **How to run:**
  ```bash
  python wifi_pass_getter.py
  ```
- **Output:** Displays a formatted table with Wi-Fi network names and their corresponding passwords.
- **Platform:** Windows only.

---

### 8. Wi-Fi Sharing QR Code Generator ([`wifi_sharing_qrcode.py`](wifi_sharing_qrcode.py))
- **Description:** Generates standard WPA/WPA2 Wi-Fi authentication QR codes compatible with iOS and Android camera scanners for instant connection without typing passwords.
- **How to run:**
  ```bash
  python wifi_sharing_qrcode.py
  ```
- **Inputs:** Prompts for Wi-Fi SSID (network name) and password.
- **Output:** Saves `wifi_qr.png` ready for printing or scanning directly on screen.

---

### 9. Wi-Fi & Internet Speed Checker ([`wifi_speed_checker.py`](wifi_speed_checker.py))
- **Description:** Tests internet connection throughput against nearby Speedtest.net servers using `speedtest-cli`.
- **How to run:**
  ```bash
  python wifi_speed_checker.py
  ```
- **Output:** Prints real-time download and upload speeds formatted in Mbps.

---

### 10. YouTube Music Downloader ([`yt_music_downloader.py`](yt_music_downloader.py))
- **Description:** Downloads video streams and extracts top-tier audio tracks converted into MP3 format with embedded `ffmpeg` binaries provided by `static-ffmpeg`.
- **How to run:**
  ```bash
  python yt_music_downloader.py
  ```
- **Inputs:** Prompts for the video URL and desired output filename.
- **Output:** Downloads and converts the audio to `<filename>.mp3`.

---

## 📦 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Audri-23/Mini-Python-Projects.git
cd Mini-Python-Projects
```

### 2. (Optional) Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Run Any Script
Most scripts include self-installing dependency loaders. Simply run the script with Python:
```bash
python <script_name>.py
```

---

## 📋 Requirements & Dependencies

If you prefer to install all dependencies at once rather than letting scripts install them on demand:

```bash
pip install gallery-dl pypdf rembg pillow gTTS googletrans==4.0.0-rc1 qrcode speedtest-cli yt-dlp static-ffmpeg manim
```

### Summary of Third-Party Packages:
- [`manim`](https://pypi.org/project/manim/): Mathematical animation engine
- [`gallery-dl`](https://pypi.org/project/gallery-dl/): Image-gallery and social media downloader
- [`pypdf`](https://pypi.org/project/pypdf/): Pure-Python PDF library
- [`rembg`](https://pypi.org/project/rembg/): Background removal tool using u2net
- [`pillow`](https://pypi.org/project/Pillow/): Python Imaging Library
- [`gTTS`](https://pypi.org/project/gTTS/): Python library and CLI tool to interface with Google Translate text-to-speech API
- [`googletrans`](https://pypi.org/project/googletrans/): Google Translate API client
- [`qrcode`](https://pypi.org/project/qrcode/): QR code generator
- [`speedtest-cli`](https://pypi.org/project/speedtest-cli/): Command-line interface for testing internet bandwidth using speedtest.net
- [`yt-dlp`](https://pypi.org/project/yt-dlp/): Feature-rich audio/video downloader
- [`static-ffmpeg`](https://pypi.org/project/static-ffmpeg/): Bundled static FFmpeg binaries for audio processing

---

## 💡 Platform Compatibility & Notes

- **Python Version**: Recommended **Python 3.10+** (Python 3.12+ recommended for scripts using nested f-strings like `text_to_speech.py`).
- **Windows Only**: `wifi_pass_getter.py` relies on Windows command `netsh`.
- **Manim System Dependencies**: For `animate_text.py`, Manim may require system-level tools such as FFmpeg, LaTeX, and Cairo depending on your OS configuration. See the [Manim Installation Guide](https://docs.manim.community/en/stable/installation.html).
- **Network Access**: Scripts such as `translator.py`, `text_to_speech.py`, `speedtest`, and downloaders require an active internet connection.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/NewMiniProject`).
3. Commit your changes (`git commit -m 'Add new mini project'`).
4. Push to the branch (`git push origin feature/NewMiniProject`).
5. Open a Pull Request.

---

## 📄 License & Terms of Use

This repository is shared publicly for **educational and personal learning purposes only**.

- **Author & Copyright**: Created and maintained by [@Audri-23](https://github.com/Audri-23). All rights reserved.
- **Permitted Use**: You are welcome to view, study, fork, and run the code locally for your own learning and reference.
- **Restrictions**:
  - You **may not** re-upload, republish, or redistribute this repository (in whole or substantial part) and claim it as your own work.
  - Plagiarism, unauthorized re-licensing, or claiming ownership of this project is strictly prohibited.
  - If you reference or share snippets of this code, proper credit and attribution to the original author are required.
