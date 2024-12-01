from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QTextEdit, QLineEdit, QDoubleSpinBox, QPushButton,
                            QProgressBar, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
import json
from datetime import datetime
from pathlib import Path
from src.api.client import APIClient

class BatchRequestDialog(QDialog):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.responses = []
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Batch Request")
        self.setModal(True)
        layout = QVBoxLayout(self)
        
        # Prompt input
        prompt_label = QLabel("Batch Prompt:")
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter the prompt to be used for all batch requests...")
        self.prompt_input.setMaximumHeight(100)
        layout.addWidget(prompt_label)
        layout.addWidget(self.prompt_input)
        
        # Request count and interval controls
        params_layout = QHBoxLayout()
        
        # Request count with numeric validation
        count_layout = QVBoxLayout()
        count_label = QLabel("Number of Requests:")
        self.request_count = QLineEdit()
        validator = QIntValidator(1, 1000)
        self.request_count.setValidator(validator)
        self.request_count.setText("5")
        self.request_count.setFixedWidth(100)
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.request_count)
        params_layout.addLayout(count_layout)
        
        # Interval spinbox
        interval_layout = QVBoxLayout()
        interval_label = QLabel("Interval (seconds):")
        self.request_interval = QDoubleSpinBox()
        self.request_interval.setRange(0.5, 60.0)
        self.request_interval.setValue(2.0)
        self.request_interval.setSingleStep(0.5)
        self.request_interval.setFixedWidth(100)
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.request_interval)
        params_layout.addLayout(interval_layout)
        
        layout.addLayout(params_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Batch")
        self.start_button.clicked.connect(self.start_batch)
        self.save_button = QPushButton("Save Results")
        self.save_button.clicked.connect(self.save_results)
        self.save_button.setEnabled(False)
        self.cancel_button = QPushButton("Close")
        self.cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
    def start_batch(self):
        """Start the batch request process"""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Warning", "Please enter a prompt.")
            return
            
        try:
            request_count = int(self.request_count.text())
            if not (1 <= request_count <= 1000):
                raise ValueError("Number of requests must be between 1 and 1000")
        except ValueError as e:
            QMessageBox.warning(self, "Warning", str(e))
            return
            
        self.start_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, request_count)
        self.progress_bar.setValue(0)
        
        try:
            self.responses = self.api_client.send_batch_requests(
                prompt=prompt,
                count=request_count,
                interval=self.request_interval.value(),
                progress_callback=self.update_progress
            )
            self.save_button.setEnabled(True)
            QMessageBox.information(self, "Success", "Batch requests completed successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to complete batch requests: {str(e)}")
            
        finally:
            self.start_button.setEnabled(True)
            
    def update_progress(self, current, total):
        """Update the progress bar during batch processing"""
        self.progress_bar.setValue(current)
        
    def save_results(self):
        """Save batch results to a file"""
        if not self.responses:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"batch_results_{timestamp}.json"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Batch Results",
            default_filename,
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                # Prepare results with metadata
                results = {
                    "timestamp": timestamp,
                    "settings": {
                        "model": self.api_client.config.model,
                        "temperature": self.api_client.config.temperature,
                        "max_tokens": self.api_client.config.max_tokens,
                        "pre_input": self.api_client.config.pre_input
                    },
                    "batch_config": {
                        "prompt": self.prompt_input.toPlainText(),
                        "request_count": int(self.request_count.text()),
                        "request_interval": self.request_interval.value()
                    },
                    "responses": self.responses
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=4, ensure_ascii=False)
                    
                QMessageBox.information(
                    self,
                    "Success",
                    f"Results saved successfully to {file_path}"
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save results: {str(e)}"
                )
