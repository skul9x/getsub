import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QTextEdit, QGroupBox,
    QFileDialog, QStatusBar
)
from PySide6.QtCore import Qt, Slot
from core.client import DownSubClient
from ui.worker import Worker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.client = DownSubClient()
        self.worker = None
        self.dl_worker = None

        self.setWindowTitle("YouTube Subtitle Downloader")
        self.resize(800, 600)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 1. Input Section
        input_group = QGroupBox("Input")
        input_layout = QHBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube URL here...")
        self.url_input.setClearButtonEnabled(True)
        
        self.btn_get_subtitles = QPushButton("Get Subtitles")
        self.btn_get_subtitles.setCursor(Qt.PointingHandCursor)
        self.btn_get_subtitles.setStyleSheet("font-weight: bold; padding: 5px 10px;")

        input_layout.addWidget(QLabel("YouTube URL:"))
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.btn_get_subtitles)
        input_group.setLayout(input_layout)
        
        main_layout.addWidget(input_group)

        # 2. Results Section
        results_group = QGroupBox("Available Subtitles")
        results_layout = QVBoxLayout()
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Language", "Code", "Translated", "Action"])
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        results_layout.addWidget(self.result_table)
        results_group.setLayout(results_layout)
        
        main_layout.addWidget(results_group)

        # 3. Logs Section
        logs_group = QGroupBox("Logs")
        logs_layout = QVBoxLayout()
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("font-family: Consolas; font-size: 12px;")
        
        logs_layout.addWidget(self.log_output)
        logs_group.setLayout(logs_layout)
        
        main_layout.addWidget(logs_group)

        # Status Bar
        self.setStatusBar(QStatusBar(self))
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
        # Connect signals
        self.btn_get_subtitles.clicked.connect(self.on_get_subtitles)

    @Slot()
    def on_get_subtitles(self):
        url = self.url_input.text().strip()
        if not url:
            self.log("Error: Please enter a correct URL.")
            self.status_bar.showMessage("Error: Empty URL")
            return

        self.btn_get_subtitles.setEnabled(False)
        self.log(f"Fetching info for: {url}")
        self.status_bar.showMessage("Fetching video info...")
        
        # Start worker
        self.worker = Worker(self.client.get_video_info, url)
        self.worker.finished.connect(self.on_info_received)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    @Slot(object)
    def on_info_received(self, data):
        self.btn_get_subtitles.setEnabled(True)
        self.log("Info received successfully.")
        self.status_bar.showMessage("Info received")
        
        title = data.get("title", "Unknown Title")
        self.current_title = title  # Store for download usage
        self.log(f"Title: {title}")
        
        subtitles = data.get("subtitles", [])
        auto_subs = data.get("subtitlesAutoTrans", []) # Sometimes auto generated are separate if we want them
        
        all_subs = subtitles + auto_subs
        
        self.populate_table(all_subs)
        self.status_bar.showMessage(f"Found {len(all_subs)} subtitles")

    @Slot(str)
    def on_error(self, error_msg):
        self.btn_get_subtitles.setEnabled(True)
        self.log(f"Error: {error_msg}")
        self.status_bar.showMessage("Error occurred")

    def populate_table(self, subtitles):
        self.result_table.setRowCount(0)
        
        for sub in subtitles:
            row_idx = self.result_table.rowCount()
            self.result_table.insertRow(row_idx)
            
            name = sub.get("name", "Unknown")
            code = sub.get("code", "N/A")
            
            self.result_table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.result_table.setItem(row_idx, 1, QTableWidgetItem(code))
            self.result_table.setItem(row_idx, 2, QTableWidgetItem("No" if "auto" in code else "Yes")) # Approximate guess
            
            # Action Button
            btn_download = QPushButton("Download")
            btn_download.setCursor(Qt.PointingHandCursor)
            # Use a closure or lambda to capture the specific sub item
            # Warning: Python loop variable capturing requires default arg hack or partial
            btn_download.clicked.connect(lambda _, s=sub: self.on_download_clicked(s))
            
            self.result_table.setCellWidget(row_idx, 3, btn_download)

    def on_download_clicked(self, sub_entry):
        # Ask user for save location
        # Default filename: Title.LanguageCode.srt
        safe_title = "".join([c for c in self.current_title if c.isalnum() or c in (' ', '-', '_')]).strip()
        lang_code = sub_entry.get("code", "unknown")
        default_name = f"{safe_title}.{lang_code}.srt"
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Subtitle", default_name, "Subtitle Files (*.srt *.txt)")
        
        if file_path:
            self.log(f"Downloading to: {file_path}")
            
            # Use worker for download
            self.dl_worker = Worker(self.client.download_subtitle, sub_entry, self.current_title)
            # Pass file_path via lambda or store it
            # Or better, wrap the client call to also save the file
            
            # Let's verify: client.download_subtitle returns TEXT.
            # So the worker will return TEXT. We save it in on_download_finished.
            
            self.dl_worker.finished.connect(lambda content: self.save_file(file_path, content))
            self.dl_worker.error.connect(self.on_error)
            self.dl_worker.start()

    def save_file(self, path, content):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.log(f"Saved: {path}")
        except Exception as e:
            self.log(f"Error saving file: {e}")
        
    def log(self, message):
        self.log_output.append(f"> {message}")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
