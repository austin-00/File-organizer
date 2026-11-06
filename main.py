import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator
from ui.main_window import MainWindow
from organizer.config import load_settings

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("FileOrganizer")

    settings = load_settings()
    lang_code = settings.get("language", "en")

    translator = QTranslator()
    
    # Find the correct path for .py or .exe
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    translation_path = os.path.join(base_path, "ui", "translations", f"app_{lang_code}.qm")
    
    if os.path.exists(translation_path):
        if translator.load(translation_path):
            app.installTranslator(translator)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()