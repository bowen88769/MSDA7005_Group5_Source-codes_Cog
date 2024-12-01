from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QComboBox, QLineEdit, QSlider, QSpinBox,
                            QTextEdit, QPushButton, QFormLayout, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
import json
import os
from pathlib import Path 

class SettingsPanel(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Model Selection - now editable
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.addItems([
            "gpt-3.5-turbo-1106",
            "gpt-4-turbo-2024-04-09",
            "gpt-4o",
            "gpt-4o-mini",
            "claude-3-5-sonnet-20241022",
            "claude-3-haiku-20240307",
            "claude-3-opus-20240229",
            "o1-mini",
            "o1-preview",
            "gemini-1.5-flash",
            "gemini-1.5-pro-exp-0827",
            "Meta-Llama-3.1-405B-Instruct"
        ])
        self.model_combo.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        form_layout.addRow("Model ID:", self.model_combo)

        # API URL
        self.api_url = QLineEdit()
        self.api_url.setPlaceholderText("Enter API endpoint URL")
        form_layout.addRow("API URL:", self.api_url)

        # API Key Selection/Input
        self.api_key_combo = QComboBox()
        self.api_key_combo.setEditable(True)
        self.api_key_combo.setPlaceholderText("Enter your API key")
        form_layout.addRow("API Key:", self.api_key_combo)

        # Temperature Slider
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_slider.setRange(0, 100)
        self.temperature_slider.setValue(70)
        self.temperature_label = QLabel("0.7")
        self.temperature_slider.valueChanged.connect(
            lambda v: self.temperature_label.setText(f"{v/100:.1f}"))
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(self.temperature_slider)
        temp_layout.addWidget(self.temperature_label)
        form_layout.addRow("Temperature:", temp_layout)

        # Max Tokens - using QLineEdit with validator for better number display
        self.max_tokens = QLineEdit()
        validator = QIntValidator(1, 32000)
        self.max_tokens.setValidator(validator)
        self.max_tokens.setText("4096")
        self.max_tokens.setFixedWidth(100)
        form_layout.addRow("Max Tokens:", self.max_tokens)

        # User Pre-Input
        self.pre_input = QTextEdit()
        self.pre_input.setPlaceholderText("Enter default prompt for all requests...")
        self.pre_input.setMaximumHeight(100)
        form_layout.addRow("Default Prompt:", self.pre_input)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def load_settings(self):
        """Load saved settings from file"""
        settings_file = Path("settings.json")
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    
                    # Load model - check if it exists in combo box
                    model = settings.get('model', 'gpt-3.5-turbo-1106')
                    index = self.model_combo.findText(model)
                    if index >= 0:
                        self.model_combo.setCurrentIndex(index)
                    else:
                        self.model_combo.setCurrentText(model)
                    
                    self.api_url.setText(settings.get('api_url', ''))
                    
                    # Load API keys
                    api_keys = settings.get('api_keys', [])
                    self.api_key_combo.clear()
                    self.api_key_combo.addItems(api_keys)
                    
                    self.temperature_slider.setValue(int(float(settings.get('temperature', 0.7)) * 100))
                    self.max_tokens.setText(str(settings.get('max_tokens', 4096)))
                    self.pre_input.setText(settings.get('pre_input', ''))
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save current settings to file"""
        # Validate required fields
        if not self.api_url.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter the API URL.")
            return
            
        if not self.api_key_combo.currentText().strip():
            QMessageBox.warning(self, "Warning", "Please enter your API key.")
            return
            
        # Validate max tokens
        try:
            max_tokens = int(self.max_tokens.text())
            if not (1 <= max_tokens <= 32000):
                raise ValueError("Max tokens must be between 1 and 32000")
        except ValueError as e:
            QMessageBox.warning(self, "Warning", str(e))
            return

        settings = {
            'model': self.model_combo.currentText().strip(),
            'api_url': self.api_url.text().strip(),
            'api_keys': [self.api_key_combo.currentText().strip()],
            'temperature': self.temperature_slider.value() / 100,
            'max_tokens': max_tokens,
            'pre_input': self.pre_input.toPlainText()
        }

        try:
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
                
            # Notify parent window to reload API config
            if self.parent() and hasattr(self.parent(), 'api_client'):
                self.parent().api_client.load_config()
                
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
