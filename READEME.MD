# 📁 Multilingual File Organizer

A professional, cross-platform desktop application built with Python and PySide6 that automatically organizes messy folders into categorized directories (Documents, Images, Videos, Music, etc.). 

### ✨ Features
- **Automatic Sorting:** Categorizes files based on their extensions.
- **Multilingual UI:** Supports 20 languages with instant Right-to-Left (RTL) rendering for Arabic.
- **Safety First:** Includes a "Preview Only" (dry run) mode and defaults to copying files rather than moving them.
- **Smart Collision Handling:** If a file already exists, it automatically renames the incoming file (e.g., `image_1.jpg`).
- **Persistent Settings:** Remembers your preferred language and last-used folders using a local JSON config.

### 🛠️ Tech Stack
- **Language:** Python 3
- **GUI Framework:** PySide6 (Qt for Python)
- **Packaging:** PyInstaller
- **Localization:** Qt Linguist (`.ts` / `.qm` files)

### 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/file-organizer.git