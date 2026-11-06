import sys
import os
import subprocess
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QFileDialog,
    QProgressBar, QMessageBox, QCheckBox
)
from PySide6.QtCore import QThread, Signal
from organizer.sorter import organize_files
from organizer.config import load_settings, save_settings

class Worker(QThread):
    progress = Signal(int, int, str)
    finished_with = Signal(dict)
    failed = Signal(str)

    def __init__(self, source, dest, move, dry_run):
        super().__init__()
        self.source, self.dest, self.move, self.dry_run = source, dest, move, dry_run

    def run(self):
        try:
            report = organize_files(
                self.source, self.dest,
                move=self.move, dry_run=self.dry_run,
                progress_cb=lambda i, t, n: self.progress.emit(i, t, n)
            )
            self.finished_with.emit(report)
        except Exception as e:
            self.failed.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()

        self.setWindowTitle(self.tr("Multilingual File Organizer"))
        self.resize(600, 400)

        central = QWidget()
        layout = QVBoxLayout(central)

        # Language selector
        lang_row = QHBoxLayout()
        lang_row.addWidget(QLabel(self.tr("Language:")))
        self.lang_combo = QComboBox()
        
        self.languages = [
            ("English", "en"), ("Español", "es"), ("Français", "fr"), 
            ("Deutsch", "de"), ("中文", "zh"), ("العربية", "ar"), 
            ("हिन्दी", "hi"), ("Português", "pt"), ("Русский", "ru"), ("日本語", "ja")
        ]
        for name, code in self.languages:
            self.lang_combo.addItem(name, code)
            
        saved_lang = self.settings.get("language", "en")
        index = self.lang_combo.findData(saved_lang)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
            
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_row.addWidget(self.lang_combo)
        layout.addLayout(lang_row)

        # Source folder
        self.source_edit = QLineEdit()
        self.source_edit.setPlaceholderText(self.tr("Source folder..."))
        self.source_edit.setText(self.settings.get("source", ""))
        src_btn = QPushButton(self.tr("Browse"))
        src_btn.clicked.connect(self.pick_source)
        src_row = QHBoxLayout()
        src_row.addWidget(self.source_edit)
        src_row.addWidget(src_btn)
        layout.addWidget(QLabel(self.tr("Source folder:")))
        layout.addLayout(src_row)

        # Destination folder
        self.dest_edit = QLineEdit()
        self.dest_edit.setPlaceholderText(self.tr("Destination folder..."))
        self.dest_edit.setText(self.settings.get("destination", ""))
        dest_btn = QPushButton(self.tr("Browse"))
        dest_btn.clicked.connect(self.pick_dest)
        dest_row = QHBoxLayout()
        dest_row.addWidget(self.dest_edit)
        dest_row.addWidget(dest_btn)
        layout.addWidget(QLabel(self.tr("Destination folder:")))
        layout.addLayout(dest_row)

        # Options
        self.move_check = QCheckBox(self.tr("Move files (uncheck = copy)"))
        self.move_check.setChecked(self.settings.get("move_files", False))
        self.dry_run_check = QCheckBox(self.tr("Preview only (dry run)"))
        layout.addWidget(self.move_check)
        layout.addWidget(self.dry_run_check)

        # Progress + start
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        self.start_btn = QPushButton(self.tr("Start Sorting"))
        self.start_btn.clicked.connect(self.start_sorting)
        layout.addWidget(self.start_btn)

        self.setCentralWidget(central)
        self.worker = None

    def change_language(self):
        new_lang = self.lang_combo.currentData()
        if new_lang != self.settings.get("language"):
            self.settings["language"] = new_lang
            save_settings(self.settings)
            
            # The bulletproof restart method
            if getattr(sys, 'frozen', False):
                # Running as .exe
                subprocess.Popen([sys.executable])
            else:
                # Running as .py
                subprocess.Popen([sys.executable] + sys.argv)
            
            sys.exit(0)

    def pick_source(self):
        d = QFileDialog.getExistingDirectory(self, self.tr("Select source folder"))
        if d: self.source_edit.setText(d)

    def pick_dest(self):
        d = QFileDialog.getExistingDirectory(self, self.tr("Select destination folder"))
        if d: self.dest_edit.setText(d)

    def start_sorting(self):
        src = os.path.normpath(self.source_edit.text())
        dst = os.path.normpath(self.dest_edit.text())
        
        if not src or not dst or not os.path.isdir(src):
            QMessageBox.warning(self, self.tr("Missing info"), self.tr("Please select valid folders."))
            return

        self.settings["source"] = src
        self.settings["destination"] = dst
        self.settings["move_files"] = self.move_check.isChecked()
        save_settings(self.settings)

        self.start_btn.setEnabled(False)
        self.progress.setValue(0)
        self.worker = Worker(src, dst, self.move_check.isChecked(), self.dry_run_check.isChecked())
        self.worker.progress.connect(lambda i, t, n: self.progress.setValue(int(i / t * 100)))
        self.worker.finished_with.connect(self.on_finished)
        self.worker.failed.connect(self.on_failed)
        self.worker.start()

    def on_finished(self, report):
        self.start_btn.setEnabled(True)
        msg = self.tr("Done!\n\nMoved: {}\nSkipped: {}").format(report['moved'], report['skipped'])
        if report["errors"]:
            msg += self.tr("\nErrors: {}").format(len(report["errors"]))
        QMessageBox.information(self, self.tr("Finished"), msg)

    def on_failed(self, err):
        self.start_btn.setEnabled(True)
        QMessageBox.critical(self, self.tr("Error"), err)